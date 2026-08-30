#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path

PATH=Path('data/formulas/SESSION_FORMULA_REGISTRY_53_V1.json')
obj=json.loads(PATH.read_text(encoding='utf-8'))
items=obj.get('items',[])
errors=[]
if obj.get('exact_count')!=53: errors.append('DECLARED_COUNT_NE_53')
if len(items)!=53: errors.append(f'ACTUAL_COUNT_NE_53:{len(items)}')
expected=[f'F{i:02d}' for i in range(1,54)]
ids=[x.get('id') for x in items]
if ids!=expected: errors.append('ID_SEQUENCE_MUST_BE_F01_TO_F53')
if len(set(ids))!=53: errors.append('DUPLICATE_IDS')
for item in items:
    for key in ('id','title','formula','class','routes'):
        if key not in item or item[key] in ('',None,[]): errors.append(f'MISSING_{key}:{item.get("id","TOKEN_VAZIO")}')
    if 'Mapa' not in item.get('routes',[]): errors.append(f'MAPA_ROUTE_MISSING:{item.get("id")}')
if obj.get('claim_allowed') is not False: errors.append('CLAIM_ALLOWED_MUST_BE_FALSE')
if obj.get('invariant')!='FORMULA_COUNT_MUST_EQUAL_53': errors.append('COUNT_INVARIANT_MISSING')
if errors:
    print('\n'.join(errors))
    raise SystemExit(2)
print('PASS exact_count=53 ids=F01..F53 claim_allowed=false')
