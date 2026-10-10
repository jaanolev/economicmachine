"""Run the gut-feeling climber. Known-answer first, then Landau."""

from __future__ import annotations

import ast
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from climb_gold import evaluate_known_answer
from climb_seeds import seed_boundedgaps_2012, seed_landau_2026
from climber import climb
from library import SCHEMA_VERSION


ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
LIBRARY = ROOT / "library"
SRC = Path(__file__).resolve().parent

WINNER_STRINGS = (
    "zhang",
    "maynard",
    "wiles",
    "perelman",
    "taniyama",
    "frey curve",
    "green-tao",
)


def leakage_scan() -> dict:
    hits = []
    for name in (
        "climber.py",
        "climb_moves.py",
        "climb_check.py",
        "climb_seeds.py",
        "library.py",
    ):
        text = (SRC / name).read_text(encoding="utf-8")
        low = text.lower()
        tree = ast.parse(text)
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if alias.name.split(".")[0] == "climb_gold":
                        hits.append(f"{name} imports climb_gold")
            if isinstance(node, ast.ImportFrom):
                if node.module and node.module.split(".")[0] == "climb_gold":
                    hits.append(f"{name} imports climb_gold")
        for s in WINNER_STRINGS:
            if s in low:
                hits.append(f"{name} contains {s!r}")
    return {"ok": not hits, "hits": hits}


def dump_seeds() -> None:
    LIBRARY.mkdir(parents=True, exist_ok=True)
    seed_boundedgaps_2012().save(LIBRARY / "seed_boundedgaps_2012.json")
    seed_landau_2026().save(LIBRARY / "seed_landau_2026.json")
    schema = {
        "schema_version": SCHEMA_VERSION,
        "description": (
            "DAG of lemma-shaped claims. Nodes merge on claim.equiv_key. "
            "Edges are cheap moves. Status is seed|sketched|checked_*."
        ),
        "node": {
            "id": "sha1(equiv_key)[:12]",
            "claim": {
                "pred": "target|weighted_detector|level_of_distribution|implication_open_hyp|almost_primes|heuristic|heuristic_target|prime_values|translation|relative_density|sketch_start",
                "weight_family": "na|none|indicator|selberg_1d|richer",
                "moduli": "na|all|smooth",
                "level_demand": "na|gt_half|half|any_positive",
                "level_have": "na|none|half|gt_half_smooth|eh",
                "extra_var": "na|yes|no",
                "conditional": "bool",
                "barrier": "na|parity|no_extra_variable",
                "family": "na|twins|n2plus1|x2y4|two_squares|linear",
            },
            "kind": "seed|sketch|target|start",
            "status": "seed|sketched|checked_hold|checked_fail|checked_barrier|checked_unknown|checked_translation",
            "confidence": "float 0-1",
        },
        "edge": {
            "id": "sha1(src|move|dst)[:12]",
            "move": "ENRICH_DETECTOR|CHANGE_SUPPORT|COMBINE|ASSUME_OPEN|TYPE_I_ONLY|HEURISTIC_CLOSE|SPECIALIZE|ENLARGE|TRANSLATE|RELATIVE_AMBIENT",
        },
    }
    (LIBRARY / "schema.json").write_text(json.dumps(schema, indent=2), encoding="utf-8")


def main() -> int:
    RESULTS.mkdir(parents=True, exist_ok=True)
    dump_seeds()
    leak = leakage_scan()

    ka = climb("boundedgaps_2012")
    lib = ka.pop("library")
    lib.save(LIBRARY / "grown_boundedgaps_2012.json")
    gates = evaluate_known_answer(lib, ka["top_paths"] if False else _all_paths(lib), ka["checks"])
    # evaluate on all paths, not just top 15
    ka_out = {k: v for k, v in ka.items() if k != "library"}
    ka_out["gates"] = gates
    ka_out["C4_no_leakage"] = leak["ok"]
    ka_out["leakage_hits"] = leak["hits"]
    ka_out["PASS"] = bool(gates["PASS"] and leak["ok"])
    (RESULTS / "climber_known_answer.json").write_text(
        json.dumps(ka_out, indent=2), encoding="utf-8"
    )

    landau = climb("landau_2026")
    llib = landau.pop("library")
    llib.save(LIBRARY / "grown_landau_2026.json")
    landau_out = {k: v for k, v in landau.items()}
    landau_out["honesty"] = (
        "No progress on Landau. High path scores are gut feelings after a "
        "cheap barrier check. Do not treat a surviving path as a proof."
    )
    (RESULTS / "climber_landau.json").write_text(
        json.dumps(landau_out, indent=2), encoding="utf-8"
    )

    print(json.dumps({"known_answer": {k: ka_out[k] for k in ("PASS", "gates", "C4_no_leakage", "n_nodes", "n_edges", "n_merges")}, "landau": {k: landau_out[k] for k in ("n_nodes", "n_edges", "n_paths")}}, indent=2))
    print("KA PASS" if ka_out["PASS"] else "KA FAIL")
    print("top landau paths:")
    for p in landau_out["top_paths"][:5]:
        print(f"  {p['score']:.3f} {p['moves']} -> {p['end_pred']} {p['end_status']}")
    return 0 if ka_out["PASS"] else 1


def _all_paths(lib) -> list:
    from climber import enumerate_paths, path_record

    recs = [path_record(lib, p) for p in enumerate_paths(lib)]
    recs.sort(key=lambda r: (-r["score"], r["node_ids"][0]))
    return recs


if __name__ == "__main__":
    raise SystemExit(main())
