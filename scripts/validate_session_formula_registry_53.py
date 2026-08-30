#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path

REGISTRY=Path('data/formulas/SESSION_FORMULA_REGISTRY_53_V1.json')
ROUTES=Path('data/integration/SESSION_FORMULAS_53_REPO_ROUTES_V1.json')
obj=json.loads(REGISTRY.read_text(encoding='utf-8'))
routes=json.loads(ROUTES.read_text(encoding='utf-8'))
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

repo_routes=routes.get('routes',[])
repos=[x.get('repo') for x in repo_routes]
if routes.get('formula_count')!=53: errors.append('ROUTE_MANIFEST_FORMULA_COUNT_NE_53')
if routes.get('minimum_repository_routes')!=10: errors.append('MINIMUM_REPOSITORY_ROUTES_NE_10')
if len(repo_routes)<10: errors.append(f'REPOSITORY_ROUTE_COUNT_LT_10:{len(repo_routes)}')
if len(set(repos))!=len(repos): errors.append('DUPLICATE_REPOSITORY_ROUTES')
if routes.get('actual_repository_routes')!=len(repo_routes): errors.append('DECLARED_REPOSITORY_ROUTE_COUNT_MISMATCH')
if routes.get('claim_allowed') is not False: errors.append('ROUTE_MANIFEST_CLAIM_ALLOWED_MUST_BE_FALSE')
if 'rafaelmeloreisnovo/Mapa' not in repos: errors.append('CANONICAL_MAPA_ROUTE_MISSING')
for route in repo_routes:
    for key in ('repo','role','branch','head'):
        if not route.get(key): errors.append(f'MISSING_ROUTE_{key}:{route.get("repo","TOKEN_VAZIO")}')

if errors:
    print('\n'.join(errors))
    raise SystemExit(2)
print(f'PASS exact_count=53 ids=F01..F53 repository_routes={len(repo_routes)} claim_allowed=false')
