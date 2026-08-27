#!/usr/bin/env python3
"""RAFAELIA E1-CONTRACT-v1 deterministic fail-closed parser.

Boundary: syntax only. No algebraic simplification, variable renaming, domain/unit
inference, E2 equivalence, or global-total promotion.
"""

from __future__ import annotations
import hashlib
import json
import re
import unicodedata
from dataclasses import dataclass

CONTRACT_VERSION = "E1-CONTRACT-v1"
IMPLEMENTATION_VERSION = "E1-PARSER-v1"
FAILURES = {
    "UNBALANCED_DELIMITER",
    "AMBIGUOUS_RADICAL_EXTENT",
    "AMBIGUOUS_IMPLICIT_MULTIPLICATION",
    "UNSUPPORTED_OPERATOR",
    "UNSUPPORTED_NOTATION",
    "MALFORMED_NUMBER",
    "MISSING_OPERAND",
    "TOKENIZATION_FAILURE",
    "PARSER_INTERNAL_ERROR",
}

class ParseFailure(Exception):
    def __init__(self, code: str):
        if code not in FAILURES:
            code = "PARSER_INTERNAL_ERROR"
        self.code = code
        super().__init__(code)

@dataclass(frozen=True)
class Tok:
    kind: str
    value: str

_TOKEN = re.compile(
    r"""
    (?P<NUMBER>(?:\d+\.\d+|\d+))
  | (?P<ID>[^\W\d]\w*)
  | (?P<REL><=|>=|!=|=|<|>)
  | (?P<OP>[+\-*/^(),|√])
  | (?P<WS>\s+)
  | (?P<OTHER>.)
    """,
    re.VERBOSE | re.UNICODE,
)

def _nfc(s: str) -> str:
    return unicodedata.normalize("NFC", s.strip())

def tokenize(s: str) -> list[Tok]:
    s = _nfc(s)
    if not s:
        raise ParseFailure("MISSING_OPERAND")
    out: list[Tok] = []
    for m in _TOKEN.finditer(s):
        kind, value = m.lastgroup, m.group()
        if kind == "WS":
            continue
        if kind == "OTHER":
            raise ParseFailure("UNSUPPORTED_NOTATION")
        if kind == "NUMBER":
            if value.count(".") > 1:
                raise ParseFailure("MALFORMED_NUMBER")
            out.append(Tok("NUMBER", value))
        elif kind == "ID":
            out.append(Tok("ID", value))
        elif kind == "REL":
            out.append(Tok("REL", value))
        else:
            out.append(Tok(value, value))
    _reject_implicit_multiplication(out)
    return out

def _is_atom_end(t: Tok) -> bool:
    return t.kind in {"NUMBER", "ID", ")"}

def _is_atom_start(t: Tok) -> bool:
    return t.kind in {"NUMBER", "ID", "(", "√"}

def _reject_implicit_multiplication(tokens: list[Tok]) -> None:
    # Function call ID(...) is explicit syntax under this grammar.
    for a, b in zip(tokens, tokens[1:]):
        if a.kind == "ID" and b.kind == "(":
            continue
        if _is_atom_end(a) and _is_atom_start(b):
            raise ParseFailure("AMBIGUOUS_IMPLICIT_MULTIPLICATION")

def ast(kind: str, *args):
    return [kind, *args]

class Parser:
    def __init__(self, tokens: list[Tok]):
        self.t = tokens
        self.i = 0

    def peek(self, kind: str | None = None):
        if self.i >= len(self.t):
            return None if kind is None else False
        return self.t[self.i] if kind is None else self.t[self.i].kind == kind

    def take(self, kind: str | None = None) -> Tok:
        if self.i >= len(self.t):
            raise ParseFailure("MISSING_OPERAND")
        tok = self.t[self.i]
        if kind is not None and tok.kind != kind:
            raise ParseFailure("UNSUPPORTED_OPERATOR")
        self.i += 1
        return tok

    def parse(self):
        node = self.relation()
        if self.i != len(self.t):
            if any(x.kind in {"(", ")", "|"} for x in self.t[self.i:]):
                raise ParseFailure("UNBALANCED_DELIMITER")
            raise ParseFailure("UNSUPPORTED_NOTATION")
        return node

    def relation(self):
        left = self.expr()
        if self.peek() and self.peek().kind == "REL":
            op = self.take("REL").value
            right = self.expr()
            kind = "equality" if op == "=" else "relation"
            node = ast(kind, left, right) if op == "=" else ast(kind, op, left, right)
            if self.peek() and self.peek().kind == "REL":
                raise ParseFailure("UNSUPPORTED_NOTATION")
            return node
        return left

    def expr(self):
        node = self.term()
        while self.peek() and self.peek().kind in {"+", "-"}:
            op = self.take().kind
            rhs = self.term()
            node = ast("add" if op == "+" else "subtract", node, rhs)
        return node

    def term(self):
        node = self.power()
        while self.peek() and self.peek().kind in {"*", "/"}:
            op = self.take().kind
            rhs = self.power()
            node = ast("multiply" if op == "*" else "divide", node, rhs)
        return node

    def power(self):
        node = self.unary()
        if self.peek("^"):
            self.take("^")
            node = ast("power", node, self.power())
        return node

    def unary(self):
        if self.peek("-"):
            self.take("-")
            return ast("unary_minus", self.unary())
        if self.peek("√"):
            self.take("√")
            # Radical applies to exactly one syntactic atom.
            if self.peek() is None or self.peek().kind in {"+", "-", "*", "/", "^", "REL", ",", ")", "|"}:
                raise ParseFailure("AMBIGUOUS_RADICAL_EXTENT")
            return ast("sqrt", self.primary())
        return self.primary()

    def primary(self):
        tok = self.peek()
        if tok is None:
            raise ParseFailure("MISSING_OPERAND")
        if tok.kind == "NUMBER":
            v = self.take("NUMBER").value
            return ast("decimal_literal" if "." in v else "integer", v)
        if tok.kind == "ID":
            name = self.take("ID").value
            if self.peek("("):
                self.take("(")
                args = []
                if self.peek(")"):
                    raise ParseFailure("MISSING_OPERAND")
                args.append(self.relation())
                while self.peek(","):
                    self.take(",")
                    args.append(self.relation())
                if not self.peek(")"):
                    raise ParseFailure("UNBALANCED_DELIMITER")
                self.take(")")
                if name == "sqrt":
                    if len(args) != 1:
                        raise ParseFailure("UNSUPPORTED_NOTATION")
                    return ast("sqrt", args[0])
                return ast("function_call", name, args)
            return ast("symbol", name)
        if tok.kind == "(":
            self.take("(")
            node = self.relation()
            if not self.peek(")"):
                raise ParseFailure("UNBALANCED_DELIMITER")
            self.take(")")
            return node
        if tok.kind == "|":
            self.take("|")
            if self.peek("|"):
                raise ParseFailure("MISSING_OPERAND")
            node = self.relation()
            if not self.peek("|"):
                raise ParseFailure("UNBALANCED_DELIMITER")
            self.take("|")
            return ast("absolute_value", node)
        if tok.kind in {")", "|"}:
            raise ParseFailure("UNBALANCED_DELIMITER")
        raise ParseFailure("UNSUPPORTED_OPERATOR")

def canonical_json(node) -> str:
    return json.dumps(node, ensure_ascii=False, separators=(",", ":"), sort_keys=False)

def parse_expression(expression: str) -> dict:
    normalized = _nfc(expression)
    input_digest = hashlib.sha256(normalized.encode("utf-8")).hexdigest()
    try:
        node = Parser(tokenize(normalized)).parse()
        ser = canonical_json(node)
        return {
            "contract_version": CONTRACT_VERSION,
            "implementation_version": IMPLEMENTATION_VERSION,
            "input_expression_digest": input_digest,
            "disposition": "AST_DIGEST",
            "ast_serialization": ser,
            "ast_digest": hashlib.sha256(ser.encode("utf-8")).hexdigest(),
            "typed_failure_code": None,
        }
    except ParseFailure as exc:
        return {
            "contract_version": CONTRACT_VERSION,
            "implementation_version": IMPLEMENTATION_VERSION,
            "input_expression_digest": input_digest,
            "disposition": "TYPED_PARSE_FAILURE",
            "ast_serialization": None,
            "ast_digest": None,
            "typed_failure_code": exc.code,
        }
    except Exception:
        return {
            "contract_version": CONTRACT_VERSION,
            "implementation_version": IMPLEMENTATION_VERSION,
            "input_expression_digest": input_digest,
            "disposition": "TYPED_PARSE_FAILURE",
            "ast_serialization": None,
            "ast_digest": None,
            "typed_failure_code": "PARSER_INTERNAL_ERROR",
        }

def run_preflight() -> dict:
    cases = []
    a = parse_expression("q = sqrt(3)/2")
    b = parse_expression("q=√3/2")
    cases.append({
        "fixture_id": "E1-FX-001",
        "pass": a["disposition"] == b["disposition"] == "AST_DIGEST" and a["ast_digest"] == b["ast_digest"],
        "left": a,
        "right": b,
    })
    c = parse_expression("|m|=42")
    cases.append({
        "fixture_id": "E1-FX-002",
        "pass": c["ast_serialization"] == '["equality",["absolute_value",["symbol","m"]],["integer","42"]]',
        "result": c,
    })
    d = parse_expression("A=u")
    cases.append({
        "fixture_id": "E1-FX-003",
        "pass": d["ast_serialization"] == '["equality",["symbol","A"],["symbol","u"]]',
        "result": d,
    })
    e = parse_expression("1/2x")
    cases.append({
        "fixture_id": "E1-FX-NEG-001",
        "pass": e["typed_failure_code"] == "AMBIGUOUS_IMPLICIT_MULTIPLICATION",
        "result": e,
    })
    f = parse_expression("|x=1")
    cases.append({
        "fixture_id": "E1-FX-NEG-002",
        "pass": f["typed_failure_code"] == "UNBALANCED_DELIMITER",
        "result": f,
    })
    return {
        "contract_version": CONTRACT_VERSION,
        "implementation_version": IMPLEMENTATION_VERSION,
        "fixture_count": len(cases),
        "pass_count": sum(1 for x in cases if x["pass"]),
        "all_pass": all(x["pass"] for x in cases),
        "fixtures": cases,
    }

if __name__ == "__main__":
    print(json.dumps(run_preflight(), ensure_ascii=False, sort_keys=True, separators=(",", ":")))
