# RAFAELIA GPT Layout and Workflows V1

**Date:** 2026-08-23

**State:** `IMPLEMENTED_PROPOSED`

**Claim state:** `REFERENCE`

## Objective

Use ChatGPT as a federated cognitive interface and contextual router.
Do not use the prompt or a single session as a monolithic state store.

The canonical chain is:

```text
objective
-> bootstrap
-> authority
-> route
-> evidence
-> gate
-> execution
-> receipt
-> delta
-> index feedback
-> F_ok / F_gap / F_next
```

## Canonical pointers

- Bootstrap: `bootstrap/RAFAELIA_CHATGPT_BOOTSTRAP_V1.md`.
- Authority: `governance/AUTHORITY_MATRIX_V1.yaml`.
- Activation: `governance/ACTIVATION_REGISTRY_V1.json`.
- Navigation: `navigation/INDEX.md`.
- Machine navigation: `navigation/RAFAELIA_MASTER_REGISTRY.v1.json`.
- Machine GPT layout: `governance/GPT_LAYOUT_WORKFLOW_V1.json`.
- Drive GPT layout: `SRC:DRIVE:1tKGN2zBCaIuqTPJbIBEgjD6WjNO28YYyVn6ZDDfGYsA`.

## Custom instructions contract

Custom instructions should keep only stable operating rules:

- operational identity;
- response style;
- epistemic invariants;
- bootstrap pointer;
- `F_ok / F_gap / F_next` closure.

Mutable state stays outside custom instructions:

- repository inventories;
- pull request states;
- CI states;
- mutable hashes;
- historical checkpoints;
- domain formula corpora.

Recommended compact bootstrap:

```text
RAFAELIA_BOOTSTRAP:
Use rafaelmeloreisnovo/Mapa ->
bootstrap/RAFAELIA_CHATGPT_BOOTSTRAP_V1.md as the initial contract.
Resolve objective -> authority -> route -> evidence -> gate -> delta -> index.
Read connected GitHub/Drive authority when current state matters.
Do not reconstruct private current state from memory when the source is readable.
Preserve VISAO != ARTEFATO != EXECUCAO != EVIDENCIA != CLAIM.
TOKEN_VAZIO is a valid unresolved state; do not fill it by imagination.
Keep claim_allowed=false without the applicable evidence gate.
Close significant work with F_ok / F_gap / F_next and DELTA after writes.
```

## Seven layers

### L0 Human interface

Input is current objective, requested format, authorization and urgency.
Output is a bounded objective.

### L1 Bootstrap

Load the canonical bootstrap and its pointers.
Do not load the entire corpus by default.

### L2 Authority

Resolve the canonical owner and write boundary before mutation.
A higher-scope component does not replace missing evidence.

### L3 Navigation

Recover only the minimum context needed for the objective.
Preserve source identity, provenance and known gaps.

### L4 Activation

Activate components only when they add material value by resolving a gap,
increasing evidence or provenance, providing a falsifier, or enabling execution.

### L5 Execution and evidence

The authorized producer or tool performs the bounded action.
Execution must remain distinct from implementation and claim.
Receipt or equivalent evidence controls the claim ceiling.

### L6 Retrofeedback

Close the cycle with:

```text
F_ok   = what is established by evidence
F_gap  = gap, conflict, uncertainty or TOKEN_VAZIO
F_next = highest-value verifiable next action
DELTA  = destination plus commit/revision/receipt after a write
```

## Workflow: new session

1. Capture one operational objective.
2. Read the bootstrap.
3. Resolve authority and write boundary.
4. Retrieve only necessary context.
5. Recover already known gaps.
6. Execute the highest-value gate available in the turn.
7. Record evidence after execution or mutation.
8. Update only relevant indices.
9. Close with R3.

## Workflow: research or paper

Route through Mapa to the source or producer.
Use RLL or Papers when their authority applies.

Promotion requires:

- method;
- evidence;
- falsifier;
- applicable gate;
- receipt.

Internal coherence alone cannot promote a scientific claim.

## Workflow: code or repository

Route:

```text
Mapa
-> producer repository
-> AGENTS or local index
-> bounded change
-> test or CI
-> receipt
-> index feedback
```

Before writing, resolve `repo/ref/path/hash`, boundary and expected test.
`IMPLEMENTED_UNTESTED` is not `PASS`.

## Workflow: memory or sessions

The invariant is:

```text
SESSION != LONGITUDINAL_MEMORY != EVIDENCE
```

The transformation route is:

```text
session
-> semantic block
-> concept
-> typed relation
-> longitudinal index
-> evidence or falsifier
-> decision
-> artifact or receipt
```

Corrections use append-only supersession or errata.
They do not silently erase provenance.

## Workflow: current status

Questions such as "what changed?" require a current authority read.
Compare commit, PR, run or Drive revision rather than relying on memory alone.

Separate:

- material change;
- observed evidence;
- gate result;
- claims still blocked;
- safest `F_next`.

## Roles

```text
MASCOTE != AGENTE != AUTORIDADE != EXECUTOR
```

Mascote is a semantic interface.
Agent is a bounded capability.
Authority governs the object.
Executor performs the authorized action.
None of these replaces human authorship or evidence.

## GPT role

```text
GPT = interface cognitiva + roteador contextual + sintetizador
```

Execution is added only when an available tool, resolved authority and gate allow it.

Mapa remains the federated navigation and state authority.
Drive remains longitudinal and editorial memory.
The producer repository remains implementation authority.
A receipt remains the bridge from execution to a possible claim.

## What changed

Before this contract, long custom instructions could mix style and mutable state.
Session context could compete with connected current authority.
Tool activation could remain implicit and workflows could be recreated case by case.

After this contract:

- custom instructions become a short stable bootstrap;
- current state is read from Mapa and Drive on demand;
- authority is resolved before execution;
- activation is an auditable state machine;
- workflows have explicit inputs, gates, outputs and TOKEN_VAZIO fallbacks;
- session, longitudinal memory and evidence remain separate;
- GPT becomes a federated interface instead of a monolithic context store.

## Evidence boundary

This repository contract can validate its own structure and invariants.
It cannot prove hidden model behavior or all future ChatGPT runtime behavior.
Such claims remain outside this artifact until separately evidenced.

## R3

**F_ok:** GPT layout and workflows are addressable in human and machine form.

**F_gap:** runtime behavior is not proven merely by repository consistency.

**F_next:** run the dedicated CI contract gate and preserve any failure as evidence.
