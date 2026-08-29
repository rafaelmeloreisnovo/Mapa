# Runtime reconciliation — conversation pair binding — 2026-08-29

state: `SOURCE_ROOT_OBSERVED / SHARD000_BOUND / BINDER_CI_PASS / FULL_CORPUS_OPEN`  
claim_allowed: `false`

## Source authority

Google Drive NOVOexport is the durable producer for the current exported conversation corpus.

```yaml
NOVOexport_root_id: 1P7hJq5R4fgYGEQIVNgRvllAad2lGxWEv
conversation_corpus_folder_id: 1S0DaA9ByFeL9wdPmvDgd3CCEe3Jcj7c2
nominal_range: conversations-000.json .. conversations-050.json
observable_shards: 50
missing_observed_object: conversations-018.json
```

Important:

```text
missing object != empty shard
```

`018` remains `TOKEN_VAZIO_PROVIDER_OBJECT` until an actual object or custody record resolves it.

## Physical execution checkpoint

`conversations-000.json` was retrieved from Drive and parsed.

```yaml
drive_file_id: 1VfP3u2BUBJ7aByrHh-PUfo4cW1jj3SBZ
bytes: 28152659
sha256: 27b3ebe900dcf811e648f0bcb8da02cc5e1e1230049567cdd1a83a6df317ee06
conversations: 100
message_objects: 9850
user: 4761
assistant: 5089
bound_pairs: 4906
```

Pair binding follows mapping ancestry, not adjacency guesses.

## Feedback source

`message_feedback.json`:

```yaml
drive_file_id: 1MP4yedkHcZdFQ8iSrnCyhPvqTS6cXVaB
records: 50
conversations: 49
thumbs_up: 32
thumbs_down: 18
observed_scope: conversation_id
response_message_id_observed: false
```

Therefore feedback can annotate a conversation context but cannot be assigned to a specific assistant pair without new evidence.

## Binder authority

```yaml
repo: rafaelmeloreisnovo/RafPolimata
script: scripts/conversation_pair_binder.py
script_commit: 4bea3b0e40ed155da0b3cd6860743ad7e2c51f3c
test_commit: 50ebf659b911025c034b066252a69368899ff47a
workflow_commit: 97648a153f1ba541ebc4b19e20a7ab5df04a571f
workflow_run: 33235947546
job_id: 99056844937
conclusion: success
binder_state: VERIFIED_LIMITED_CI
```

Observed CI steps include checkout, Python setup and `Run binder tests`, all successful.

## Receipts / memory

```yaml
physical_receipt: 7b968a389b9ae420ec26e41f44053f8c97cafff0
CI_successor_receipt: c311dcdbe414d9a4f2b7b79e47354a2dff762766
longitudinal_record: 7ba00e606067e36399f10b1970347b8f1edf86e9
```

## Relationship to permutation feedback

The earlier feedback engine remains separate:

```text
source pairing = conversation_pair_binder
operational scheduling = conversation_permutation_feedback
```

The binder does not invent `evidence/gap/risk/urgency`. The scheduler accepts those metrics only after another explicit protocol supplies them.

```text
thumbs_up/down != evidence/gap/risk/urgency
```

## Coverage state

```yaml
source_root: OBSERVED
inventory: OBSERVED_LIMITED
shard000: BOUND_AND_MEASURED
binder_CI: PASS_OBSERVED
remaining_observable_shards: TOKEN_VAZIO_NOT_EXECUTED
shard018: TOKEN_VAZIO_PROVIDER_OBJECT
full_interaction_by_interaction_coverage: false
operational_metrics: TOKEN_VAZIO_UNDERIVED
```

## P0 route

```text
1 resolve or formally preserve missing 018
2 execute binder shard-by-shard on the 49 remaining observable objects
3 emit source digest + counts + pair counts per shard
4 reconcile duplicate conversation/message identities across shards
5 only then derive per-interaction VERIFY/GAP/RISK/URGENCY under a declared protocol
6 feed those metrics into the S4 scheduler
```

No percentage of full-corpus semantic review is promoted from this checkpoint alone.
