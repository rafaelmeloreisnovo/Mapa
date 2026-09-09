#!/usr/bin/env python3
import json, sys

def fail(msg):
    print('FAIL:', msg)
    raise SystemExit(1)

p = sys.argv[1] if len(sys.argv) > 1 else 'contracts/omega177/omega177_r1_local_contracts_v1.json'
d = json.load(open(p, encoding='utf-8'))

if d.get('schema') != 'rafaelia.omega177.r1-local-contracts/v1': fail('schema')
if d.get('claim_allowed') is not False: fail('claim_allowed must be false')
g = d.get('gaps', {})
for gid in ('G074', 'G094', 'G097'):
    if gid not in g: fail('missing ' + gid)

g74 = g['G074']
if g74['integer']['signed_overflow'] != 'FORBIDDEN': fail('G074 signed overflow')
if g74['integer']['unsigned_overflow'] != 'EXPLICIT_MODULO_ONLY': fail('G074 unsigned overflow')
if 'shift < bit_width' not in g74['integer']['shift_count_rule']: fail('G074 shift rule')
if g74['floating_point']['comparison'] != 'ABS_OR_REL_TOLERANCE_REQUIRED': fail('G074 float tolerance')
if g74['rational']['zero'] != '0/1': fail('G074 rational zero')

g94 = g['G094']
req = set(g94['required_binding_fields'])
need = {'claim_id','paper_ref','code_ref','data_ref','receipt_ref','version_or_hash','sync_state'}
if req != need: fail('G094 required fields')
if g94['mismatch_rule'] != 'mismatch => CLAIM_BLOCKED': fail('G094 mismatch rule')

g97 = g['G097']
if g97['history'] != 'IMMUTABLE_APPEND_ONLY': fail('G097 history')
if not g97['deletion_policy'].startswith('NO_DESTRUCTIVE_DELETE'): fail('G097 deletion')
if g97['retention_action'] != 'TOMBSTONE_OR_SUPERSESSION_EDGE': fail('G097 retention')

r = d.get('rounds', {})
if r['R1']['promotion_rule'] != 'contract closed != population closed': fail('R1 promotion rule')
if r['R2']['promotion_rule'] != 'bytes observed before cryptographic root': fail('R2 promotion rule')

print('PASS: G074 G094 G097 contracts valid; claim_allowed=false; R1->R2 gate valid')
