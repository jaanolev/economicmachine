"""Run the frozen known-answer protocol. Prints JSON and writes results/.

PASS criteria (frozen before scores were computed):
  For each official card:
    (G1) every gold candidate scores strictly above every known-bad
    (G2) the best gold rank among all generated candidates is
         <= max(5, ceil(0.15 * n_generated))
    (G3) at least one known-bad is at or below the median generated score
  Suite:
    (S1) all official cards pass G1
    (S2) at least 3 of 5 official cards pass G2
    (S3) all official cards pass G3
    (S4) scorer.py and generator.py do not import gold and contain no
         winner-bonus strings
The suite PASSES only if S1-S4 all hold. Diagnostic card poincare_1995
is reported and does not enter S1-S3.
"""

from __future__ import annotations

import json
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from cards import CARDS, OFFICIAL_KNOWN_ANSWER_IDS, ProblemCard
from catalog import by_id
from generator import generate
from gold import GOLD, bads_for, is_gold
from scorer import score_pair
from templates import TEMPLATES


ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
WINNER_BONUS_STRINGS = (
    "wiles",
    "perelman",
    "green-tao",
    "green_tao",
    "taniyama",
    "frey curve",
    "maynard",
    "zhang 2013",
    "hamilton program bonus",
)


def _score_one(card: ProblemCard, object_id: str, template_id: str) -> int:
    obj = by_id()[object_id]
    tmpl = TEMPLATES[template_id]
    return score_pair(card, obj, tmpl).total


def evaluate_card(card: ProblemCard) -> dict:
    cands = generate(card)
    scored = []
    for c in cands:
        obj = by_id()[c.object_id]
        sc = score_pair(card, obj, TEMPLATES[c.template_id])
        scored.append(
            {
                "id": c.id,
                "object_id": c.object_id,
                "template_id": c.template_id,
                "score": sc.total,
                "is_gold": is_gold(card.id, c.object_id, c.template_id),
                "features": sc.as_dict()["features"],
            }
        )
    scored.sort(key=lambda r: (-r["score"], r["id"]))
    n = len(scored)
    gold_rows = [r for r in scored if r["is_gold"]]
    gold_scores = [r["score"] for r in gold_rows]
    gold_ranks = [i + 1 for i, r in enumerate(scored) if r["is_gold"]]

    bad_rows = []
    for b in bads_for(card.id):
        # Prefer the generated row if present; otherwise score the pair anyway.
        match = next(
            (
                r
                for r in scored
                if r["object_id"] == b.object_id and r["template_id"] == b.template_id
            ),
            None,
        )
        if match is None:
            sc = _score_one(card, b.object_id, b.template_id)
            match = {
                "id": f"{card.id}::{b.object_id}::{b.template_id}",
                "object_id": b.object_id,
                "template_id": b.template_id,
                "score": sc,
                "is_gold": False,
                "injected_bad": True,
            }
            # keep ranking among generated only; injected extras do not join the list
        bad_rows.append(
            {
                "id": match["id"],
                "object_id": b.object_id,
                "template_id": b.template_id,
                "score": match["score"],
                "why_bad": b.why_bad,
            }
        )

    best_gold = max(gold_scores) if gold_scores else None
    worst_bad = min((r["score"] for r in bad_rows), default=None)
    best_bad = max((r["score"] for r in bad_rows), default=None)
    g1 = bool(gold_scores and bad_rows and best_gold > best_bad)
    cutoff_rank = max(5, math.ceil(0.15 * n)) if n else 5
    best_gold_rank = min(gold_ranks) if gold_ranks else None
    g2 = bool(best_gold_rank is not None and best_gold_rank <= cutoff_rank)
    generated_scores = [r["score"] for r in scored]
    median = sorted(generated_scores)[n // 2] if n else 0
    g3 = bool(bad_rows and min(r["score"] for r in bad_rows) <= median)

    return {
        "card_id": card.id,
        "year_cutoff": card.year_cutoff,
        "n_generated": n,
        "cutoff_rank": cutoff_rank,
        "gold_count": len(gold_rows),
        "gold_scores": gold_scores,
        "gold_ranks": gold_ranks,
        "best_gold_score": best_gold,
        "best_gold_rank": best_gold_rank,
        "bad_rows": bad_rows,
        "best_bad_score": best_bad,
        "worst_bad_score": worst_bad,
        "median_generated_score": median,
        "G1_gold_above_all_bads": g1,
        "G2_gold_in_top_band": g2,
        "G3_some_bad_at_or_below_median": g3,
        "top10": [
            {
                "rank": i + 1,
                "id": r["id"],
                "score": r["score"],
                "is_gold": r["is_gold"],
            }
            for i, r in enumerate(scored[:10])
        ],
        "all_gold": gold_rows,
        "prestate_honesty": card.prestate_honesty,
        "unsure": card.unsure,
    }


def leakage_scan() -> dict:
    src_dir = Path(__file__).resolve().parent
    scorer_src = (src_dir / "scorer.py").read_text(encoding="utf-8").lower()
    gen_src = (src_dir / "generator.py").read_text(encoding="utf-8").lower()
    catalog_src = (src_dir / "catalog.py").read_text(encoding="utf-8").lower()
    hits = []
    for name, text in (
        ("scorer.py", scorer_src),
        ("generator.py", gen_src),
    ):
        if "from gold" in text or "import gold" in text:
            hits.append(f"{name} imports gold")
        for s in WINNER_BONUS_STRINGS:
            if s in text:
                hits.append(f"{name} contains winner-bonus string {s!r}")
    # catalog may name objects (ricci_flow) but not winner-bonus slogans
    for s in WINNER_BONUS_STRINGS:
        if s in catalog_src:
            hits.append(f"catalog.py contains winner-bonus string {s!r}")
    return {"ok": not hits, "hits": hits}


def main() -> int:
    RESULTS.mkdir(parents=True, exist_ok=True)
    official = []
    for cid in OFFICIAL_KNOWN_ANSWER_IDS:
        official.append(evaluate_card(CARDS[cid]))
    diagnostic = evaluate_card(CARDS["poincare_1995"])
    leak = leakage_scan()
    s1 = all(r["G1_gold_above_all_bads"] for r in official)
    s2 = sum(1 for r in official if r["G2_gold_in_top_band"]) >= 3
    s3 = all(r["G3_some_bad_at_or_below_median"] for r in official)
    s4 = leak["ok"]
    suite = {
        "S1_all_G1": s1,
        "S2_at_least_3_G2": s2,
        "S3_all_G3": s3,
        "S4_no_leakage_strings": s4,
        "PASS": bool(s1 and s2 and s3 and s4),
        "n_official_G2": sum(1 for r in official if r["G2_gold_in_top_band"]),
    }
    payload = {
        "protocol": "frozen_v1",
        "official": official,
        "diagnostic_poincare_1995": diagnostic,
        "leakage_scan": leak,
        "suite": suite,
        "gold_notes": {k: v.note for k, v in GOLD.items()},
    }
    out = RESULTS / "known_answer_results.json"
    out.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(json.dumps({"suite": suite, "leakage_scan": leak}, indent=2))
    for r in official:
        print(
            f"{r['card_id']}: G1={r['G1_gold_above_all_bads']} "
            f"G2={r['G2_gold_in_top_band']} G3={r['G3_some_bad_at_or_below_median']} "
            f"best_gold_rank={r['best_gold_rank']}/{r['n_generated']} "
            f"best_gold={r['best_gold_score']} best_bad={r['best_bad_score']}"
        )
    print(
        "diagnostic poincare_1995: "
        f"G1={diagnostic['G1_gold_above_all_bads']} "
        f"G2={diagnostic['G2_gold_in_top_band']} "
        f"best_gold_rank={diagnostic['best_gold_rank']}"
    )
    return 0 if suite["PASS"] else 1


if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    raise SystemExit(main())
