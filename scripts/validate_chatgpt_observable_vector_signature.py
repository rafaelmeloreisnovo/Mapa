#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path
from urllib.parse import urlparse

CONTRACT = Path('data/control-plane/CHATGPT_OBSERVABLE_VECTOR_SIGNATURE_V1_20260829.json')
FIXTURE = Path('fixtures/chatgpt_observable_vector_signature.sample.v1.json')
EXPECTED_INVARIANT = 'SIMILARITY_NE_EVIDENCE_AND_VECTOR_WEIGHT_CANNOT_UPGRADE_EVIDENCE_CLASS'
CONTENT_DIMENSIONS = 16
EVIDENCE_DIMENSIONS = 10
FORBIDDEN_KEYS = {'raw_private_content','private_payload','raw_prompt','raw_image','raw_text'}


def load(path: Path):
    with path.open('r', encoding='utf-8') as fh:
        return json.load(fh)


def valid_vector(values, size):
    if not isinstance(values, list) or len(values) != size:
        return False
    for value in values:
        if value == 'TOKEN_VAZIO':
            continue
        if not isinstance(value, (int, float)) or isinstance(value, bool) or not 0.0 <= float(value) <= 1.0:
            return False
    return True


def scan_forbidden_keys(obj, path='root'):
    errors = []
    if isinstance(obj, dict):
        for key, value in obj.items():
            if key in FORBIDDEN_KEYS:
                errors.append(f'forbidden private key at {path}.{key}')
            errors.extend(scan_forbidden_keys(value, f'{path}.{key}'))
    elif isinstance(obj, list):
        for idx, value in enumerate(obj):
            errors.extend(scan_forbidden_keys(value, f'{path}[{idx}]'))
    return errors


def validate(contract, fixture):
    errors = []
    req = lambda cond, msg: errors.append(msg) if not cond else None

    req(contract.get('schema') == 'rafaelia.chatgpt_observable_vector_signature.v1', 'contract schema mismatch')
    req(contract.get('claim_allowed') is False, 'contract claim_allowed must remain false')
    req(contract.get('invariant') == EXPECTED_INVARIANT, 'vector/evidence invariant mismatch')

    boundary = contract.get('transformer_boundary', {})
    for field in ('hidden_activations_accessible','attention_weights_accessible','provider_internal_logits_accessible','provider_internal_embedding_required'):
        req(boundary.get(field) is False, f'{field} must be false')

    vector = contract.get('vector_contract', {})
    content_dims = vector.get('content_dimensions', [])
    evidence_dims = vector.get('evidence_dimensions', [])
    req(len(content_dims) == CONTENT_DIMENSIONS and len(set(content_dims)) == CONTENT_DIMENSIONS, 'content dimensions must be 16 unique axes')
    req(len(evidence_dims) == EVIDENCE_DIMENSIONS and len(set(evidence_dims)) == EVIDENCE_DIMENSIONS, 'evidence dimensions must be 10 unique axes')
    req(vector.get('missing_value') == 'TOKEN_VAZIO', 'missing value must be TOKEN_VAZIO')

    bridge = contract.get('private_hash_bridge', {})
    req(bridge.get('raw_private_content') == 'FORBIDDEN_IN_PUBLIC_ARTIFACT', 'private raw boundary regression')
    req(bridge.get('recommended_commitment') == 'BLAKE3-256-KEYED', 'private commitment recommendation regression')

    adapters = contract.get('public_source_adapters', [])
    req(bool(adapters), 'at least one public source adapter is required')
    for adapter in adapters:
        url = adapter.get('url', '')
        req(urlparse(url).scheme == 'https' and bool(urlparse(url).netloc), f'invalid adapter URL: {url}')
        req(adapter.get('source_class') == 'PROVIDER_PRIMARY', f'adapter {adapter.get("adapter_id")} must stay provider-primary in this fixture')

    req(fixture.get('fixture_only') is True, 'fixture must be explicitly synthetic')
    req(fixture.get('public_safe') is True, 'fixture must be public_safe')
    req(fixture.get('claim_allowed') is False, 'fixture claim_allowed must remain false')
    errors.extend(scan_forbidden_keys(fixture))

    nodes = fixture.get('nodes', [])
    req(len(nodes) >= 2, 'fixture needs at least two nodes')
    site_fields = set(contract.get('site_condition_contract', {}).get('required_fields', []))
    ids = set()
    for node in nodes:
        node_id = node.get('node_id')
        req(isinstance(node_id, str) and node_id and node_id not in ids, 'node_id must be unique and non-empty')
        ids.add(node_id)
        site = node.get('site_condition', {})
        req(site_fields <= set(site.keys()), f'{node_id}: incomplete site condition')
        req(valid_vector(node.get('content_vector', {}).get('values'), CONTENT_DIMENSIONS), f'{node_id}: invalid content vector')
        req(valid_vector(node.get('evidence_vector', {}).get('values'), EVIDENCE_DIMENSIONS), f'{node_id}: invalid evidence vector')

    for rel in fixture.get('relations', []):
        req(rel.get('from') in ids and rel.get('to') in ids, 'relation endpoints must reference known nodes')
        req(rel.get('semantic_score') == 'TOKEN_VAZIO' or isinstance(rel.get('semantic_score'), (int,float)), 'semantic score must be numeric or TOKEN_VAZIO')
        req('SAME_AUTHOR_PROOF' not in str(rel.get('claim','')) or str(rel.get('claim','')).startswith('RELATED_'), 'similarity must not promote same-author proof')

    forbidden = set(contract.get('forbidden_promotions', []))
    req('HIGH_SEMANTIC_SIMILARITY_TO_SAME_AUTHOR' in forbidden, 'same-author promotion guard missing')
    req('EMBEDDING_COSINE_TO_CAUSALITY' in forbidden, 'cosine-to-causality guard missing')
    req('PRIVATE_COMMITMENT_TO_PRIVATE_CONTENT_DISCLOSURE' in forbidden, 'private disclosure guard missing')
    return errors


def main():
    try:
        contract, fixture = load(CONTRACT), load(FIXTURE)
    except Exception as exc:
        print(f'FAIL load: {exc}', file=sys.stderr)
        return 2
    errors = validate(contract, fixture)
    if errors:
        print('FAIL: ChatGPT observable vector signature')
        for err in errors:
            print(' -', err)
        return 1
    print('PASS: ChatGPT observable vector signature')
    print(' - 16 content axes + 10 evidence axes preserved')
    print(' - hidden Transformer state claims remain forbidden')
    print(' - public site conditions are explicit')
    print(' - private raw content is forbidden')
    print(' - similarity cannot upgrade evidence or authorship claims')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
