"""Generate and score Landau reframings. Writes results/landau_results.json."""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from cards import CARDS
from catalog import by_id
from generator import generate
from landau_shadows import (
    bateman_horn_truncated,
    census_n2plus1,
    gaussian_line_counts,
    odd_prime_factors_mod4,
    omega_parity,
    predicted_count,
)
from scorer import score_pair
from templates import TEMPLATES


ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"


def main() -> int:
    RESULTS.mkdir(parents=True, exist_ok=True)
    card = CARDS["landau_2026"]
    cands = generate(card)
    rows = []
    for c in cands:
        obj = by_id()[c.object_id]
        sc = score_pair(card, obj, TEMPLATES[c.template_id])
        d = c.as_dict()
        d["score"] = sc.total
        d["features"] = sc.as_dict()["features"]
        d["flags"] = sc.flags
        rows.append(d)
    rows.sort(key=lambda r: (-r["score"], r["id"]))
    for i, r in enumerate(rows, start=1):
        r["rank"] = i

    # Finite shadows actually computed in this process.
    census = census_n2plus1(300)
    omega = omega_parity(80)
    c_b = bateman_horn_truncated(500)
    pred = predicted_count(300, c_b)
    lines = gaussian_line_counts(200, 4)
    factors_ok = odd_prime_factors_mod4(80)

    shadows = {
        "census_n_max": census.n_max,
        "prime_values_n_le_300": census.prime_values,
        "first_n": list(census.first_n),
        "odd_n_primes_le_300": census.odd_n_primes,
        "omega_n_le_80": {
            "omega1": omega[0],
            "omega2": omega[1],
            "omega3": omega[2],
            "omega_ge4": omega[3],
            "odd": omega[4],
            "even": omega[5],
        },
        "bh_truncated_B500": c_b,
        "predicted_n_le_300_naive": pred,
        "ratio_census_over_pred": (census.prime_values / pred) if pred else None,
        "gaussian_lines_re200": lines,
        "odd_prime_factors_1_mod_4_n_le_80": factors_ok,
        "note": (
            "These are finite shadows, not evidence of infinitude. "
            "BH constant here is a short truncation (B=500), not the locked "
            "high-precision product of a previous agent."
        ),
    }
    payload = {
        "card_id": card.id,
        "statement": card.statement,
        "n_generated": len(rows),
        "score_histogram": _hist([r["score"] for r in rows]),
        "top5": rows[:5],
        "all": rows,
        "shadows": shadows,
        "honesty": (
            "No claim of progress on Landau. A high score means the pairing "
            "hits generic tags, not that a new attack works."
        ),
        "unsure": card.unsure,
    }
    (RESULTS / "landau_results.json").write_text(
        json.dumps(payload, indent=2), encoding="utf-8"
    )
    print(f"generated {len(rows)} reframings")
    print("top5:")
    for r in rows[:5]:
        print(f"  {r['rank']:2d}  {r['score']:2d}  {r['title']}")
    print("shadows:", json.dumps(shadows, indent=2))
    return 0


def _hist(scores: list[int]) -> dict[str, int]:
    h: dict[str, int] = {}
    for s in scores:
        h[str(s)] = h.get(str(s), 0) + 1
    return h


if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    raise SystemExit(main())
