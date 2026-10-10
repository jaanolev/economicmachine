# Climb library

Machine schema: `schema.json`.
Human schema and rules: `../climber.md`.

| file | what |
|---|---|
| `schema.json` | node/edge field list, version 1 |
| `seed_boundedgaps_2012.json` | known results at year 2012 (GPY era, no 2013 theorems) |
| `seed_landau_2026.json` | known results for Landau IV (open) |
| `grown_boundedgaps_2012.json` | seed + generator starts + sketches + checks |
| `grown_landau_2026.json` | same for Landau |

Regenerate:

```
PYTHONPATH=math/reframing-engine/src python3 math/reframing-engine/src/run_climber.py
```

Nodes merge on `claim.equiv_key`. The grown files are a DAG, not a tree:
partial climbs from different attempts join when the claim fields match.
