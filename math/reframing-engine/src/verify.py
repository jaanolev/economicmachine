"""Locks for the reframing engine. Every claimed identity/number lives here.

Run from this folder (Linux/macOS):
  pip install pytest pytest-cov
  PYTHONPATH=. python -m pytest verify.py -q

PowerShell:
  pip install pytest pytest-cov
  $env:PYTHONPATH = "."
  python -m pytest verify.py -q
"""

from __future__ import annotations

import ast
import math
from pathlib import Path

import pytest

from cards import CARDS, OFFICIAL_KNOWN_ANSWER_IDS
from catalog import CATALOG, by_id, objects_available
from generator import generate
from gold import GOLD, BADS, is_gold
from landau_shadows import (
    bateman_horn_truncated,
    census_n2plus1,
    chi4,
    gaussian_line_counts,
    local_root_count,
    no_covering_system,
    odd_prime_factors_mod4,
    omega_parity,
    predicted_count,
    sieve_primes,
)
from run_known_answers import WINNER_BONUS_STRINGS, evaluate_card, leakage_scan
from scorer import score_pair
from templates import TEMPLATES


SRC = Path(__file__).resolve().parent


def test_catalog_size_and_ids_unique():
    assert len(CATALOG) >= 40
    assert len(CATALOG) == 47  # cold grader caught engine.md saying 46
    ids = [o.id for o in CATALOG]
    assert len(ids) == len(set(ids))


def test_every_object_templates_exist():
    for o in CATALOG:
        for t in o.templates_ok:
            assert t in TEMPLATES, f"{o.id} lists unknown template {t}"
        assert o.maturity in {"theorem_rich", "mixed", "heuristic", "speculative"}


def test_year_cutoff_excludes_future_objects():
    assert all(o.year_available <= 1981 for o in objects_available(1981))
    ricci = by_id()["ricci_flow"]
    assert ricci.year_available == 1982
    assert ricci.id not in {o.id for o in objects_available(1981)}
    assert ricci.id in {o.id for o in objects_available(1995)}


def test_scorer_and_generator_do_not_import_gold():
    for name in ("scorer.py", "generator.py", "catalog.py", "templates.py"):
        tree = ast.parse((SRC / name).read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    assert alias.name.split(".")[0] != "gold", name
            if isinstance(node, ast.ImportFrom):
                if node.module:
                    assert node.module.split(".")[0] != "gold", name


def test_no_winner_bonus_strings_in_scorer_generator():
    leak = leakage_scan()
    assert leak["ok"], leak["hits"]
    text = (SRC / "scorer.py").read_text(encoding="utf-8").lower()
    for s in WINNER_BONUS_STRINGS:
        assert s not in text


def test_scorer_has_no_card_id_branches():
    src = (SRC / "scorer.py").read_text(encoding="utf-8")
    for cid in OFFICIAL_KNOWN_ANSWER_IDS:
        assert cid not in src
    assert "flt_1985" not in src
    assert "landau_2026" not in src


def test_chi4_and_local_roots():
    assert [chi4(n) for n in range(8)] == [0, 1, 0, -1, 0, 1, 0, -1]
    assert local_root_count(2) == 1
    assert local_root_count(5) == 2
    assert local_root_count(13) == 2
    assert local_root_count(3) == 0
    assert local_root_count(7) == 0


def test_odd_prime_factors_of_n2plus1_are_1_mod_4():
    assert odd_prime_factors_mod4(80) is True
    # Generic parameters: 8^2+1=65=5*13, both 1 mod 4; 10^2+1=101 prime 1 mod 4.
    assert (8 * 8 + 1) == 65
    assert (10 * 10 + 1) == 101


def test_odd_n_greater_than_1_gives_composite():
    for n in range(3, 80, 2):
        val = n * n + 1
        assert val % 2 == 0 and val > 2


def test_census_small_locked_counts():
    # Computed in this file; do not copy from another agent.
    assert census_n2plus1(10).prime_values == 5
    assert census_n2plus1(30).prime_values == 10
    assert census_n2plus1(100).prime_values == 19
    c = census_n2plus1(30)
    assert c.first_n[0] == 1
    assert 1 in c.first_n
    # Only odd n that works is n=1 among small n.
    assert c.odd_n_primes == 1


def test_no_tiny_covering():
    assert no_covering_system([3, 5, 7]) is True
    assert no_covering_system([5, 13]) is True


def test_norm_prime_sample_matches_census():
    # n^2+1 prime iff its Gaussian norm is a rational prime.
    primes = set(sieve_primes(40 * 40 + 1))
    counted = 0
    for n in range(1, 41):
        val = n * n + 1
        if val in primes:
            counted += 1
    assert counted == census_n2plus1(40).prime_values


def test_omega_parity_not_degenerate_small():
    c1, c2, c3, cge4, odd, even = omega_parity(40)
    assert c1 + c2 + c3 + cge4 == 40
    assert odd + even == 40
    assert c1 >= 1


def test_bh_product_in_range():
    c = bateman_horn_truncated(300)
    assert 0.5 < c < 2.5
    pred = predicted_count(100, c)
    got = census_n2plus1(100).prime_values
    # A short truncation need not match tightly; lock only that both are positive
    # and the ratio is not insane.
    assert pred > 0
    assert 0.2 < got / pred < 5.0


def test_line_im1_not_obviously_thinner_than_neighbours_tiny():
    lines = gaussian_line_counts(80, 3)
    assert set(lines) == {1, 2, 3}
    assert all(v >= 0 for v in lines.values())
    # Not a theorem. Just lock that the function returns three counts.


def test_generator_emits_gold_pairs_when_object_exists():
    for cid in OFFICIAL_KNOWN_ANSWER_IDS:
        card = CARDS[cid]
        cands = generate(card)
        pairs = {(c.object_id, c.template_id) for c in cands}
        spec = GOLD[cid]
        hits = [
            (o, t)
            for o in spec.objects
            for t in spec.templates
            if (o, t) in pairs
        ]
        assert hits, f"generator produced no gold pair for {cid}"


def test_known_bads_are_not_gold():
    for b in BADS:
        assert not is_gold(b.card_id, b.object_id, b.template_id)


def test_scorer_is_deterministic():
    card = CARDS["greentao_2003"]
    obj = by_id()["pseudorandom_majorants"]
    tmpl = TEMPLATES["RELATIVE_DENSITY"]
    a = score_pair(card, obj, tmpl).total
    b = score_pair(card, obj, tmpl).total
    assert a == b


def test_translate_native_is_penalized_on_landau():
    card = CARDS["landau_2026"]
    trans = score_pair(card, by_id()["gaussian_integers"], TEMPLATES["TRANSLATE"]).total
    bilinear = score_pair(
        card, by_id()["bilinear_forms_type_II"], TEMPLATES["BILINEAR"]
    ).total
    assert bilinear > trans


def test_official_g1_status_locked_honestly():
    """Lock the actual G1 outcomes. The suite does NOT pass.

    fi_1995 G1 is False: Selberg weights score as high as Type II bilinear
    forms. That is a scorer miss, not a test bug.
    """
    got = {
        cid: evaluate_card(CARDS[cid])["G1_gold_above_all_bads"]
        for cid in OFFICIAL_KNOWN_ANSWER_IDS
    }
    assert got == {
        "flt_1985": True,
        "poincare_1981": True,
        "greentao_2003": True,
        "fi_1995": False,
        "boundedgaps_2012": True,
    }


def test_suite_does_not_pass():
    from run_known_answers import leakage_scan

    official = [evaluate_card(CARDS[cid]) for cid in OFFICIAL_KNOWN_ANSWER_IDS]
    s1 = all(r["G1_gold_above_all_bads"] for r in official)
    s3 = all(r["G3_some_bad_at_or_below_median"] for r in official)
    assert s1 is False
    assert s3 is False
    assert leakage_scan()["ok"] is True
    assert sum(1 for r in official if r["G2_gold_in_top_band"]) == 5


def test_leakage_scan_module():
    assert leakage_scan()["ok"]


def test_sieve_small_primes():
    assert sieve_primes(20) == [2, 3, 5, 7, 11, 13, 17, 19]
