#!/usr/bin/env python3
"""Validate a scoped route, optionally matching producer files; no claim promotion."""
import argparse
import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]

def check(route, producer=None):
    if route.get('schema') != 'rafaelia.reconstruction-v3-route/v1' or route.get('claim_allowed') is not False:
        raise ValueError('route schema or claim boundary invalid')
    p = route['producer']
    if p['repository'] != 'instituto-Rafael/relativity-living-light' or not re.fullmatch(r'[0-9a-f]{40}', p['commit']):
        raise ValueError('producer authority or immutable commit invalid')
    if p['merged'] is not False or route['evidence']['corpus_execution'] != 'NOT_RUN':
        raise ValueError('this receipt must preserve unmerged/corpus-not-run boundaries')
    if route['evidence']['scope'].find('fixtures') < 0 or not route['gaps']:
        raise ValueError('fixture scope and gaps required')
    for field in ('kernel','contract','hosted_scanner','hosted_database','gate','receipt'):
        rel = Path(p['paths'][field])
        if rel.is_absolute() or '..' in rel.parts:
            raise ValueError('invalid producer path')
    hashes = dict(p['source_sha256'])
    hashes[p['paths']['receipt']] = p['receipt_sha256']
    for rel, digest in hashes.items():
        if not re.fullmatch(r'[0-9a-f]{64}', digest):
            raise ValueError('invalid SHA-256')
        path = Path(rel)
        if path.is_absolute() or '..' in path.parts:
            raise ValueError('unsafe hash path')
        if producer is not None:
            target = (producer.resolve() / path).resolve()
            if not target.is_relative_to(producer.resolve()):
                raise ValueError('producer file escapes root')
            if hashlib.sha256(target.read_bytes()).hexdigest() != digest:
                raise ValueError('producer hash mismatch: ' + rel)

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--producer-root',type=Path)
    args = ap.parse_args()
    route = json.loads((ROOT/'data/control-plane/RECONSTRUCTION_V3_RLL_ROUTE.v1.json').read_text())
    check(route,args.producer_root)
    print(json.dumps({'route_structure':'PASS','producer_hashes':'PASS' if args.producer_root else 'NOT_RUN',
                      'scope':'route metadata and optional byte matching only','claim_allowed':False}))

if __name__ == '__main__':
    main()
