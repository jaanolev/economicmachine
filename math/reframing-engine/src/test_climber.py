"""Locks for the gut-feeling climber."""

from __future__ import annotations

from cards import CARDS
from climb_check import check_node, toy_richer_weight_ratio
from climb_seeds import reframe_to_node, seed_boundedgaps_2012
from climber import add_generator_starts, climb
from library import Claim, Library, make_node
from run_climber import leakage_scan


def test_toy_richer_weight_ratio():
    s = toy_richer_weight_ratio()
    assert s["ratio_1d"] == 1.0
    assert s["ratio_2d"] == 2.0
    assert s["richer_wins_toy"] is True


def test_equiv_merge_joins_partial_climbs():
    lib = Library("boundedgaps_2012", 2012)
    c = Claim(pred="weighted_detector", weight_family="richer", level_demand="any_positive", family="twins")
    a = make_node(c, "sketch", 0.4, 2005, "attempt_a", "boundedgaps_2012")
    b = make_node(c, "sketch", 0.6, 2005, "attempt_b", "boundedgaps_2012")
    lib.add_node(a)
    lib.add_node(b)
    assert len(lib.nodes) == 1
    node = next(iter(lib.nodes.values()))
    assert "attempt_a" in node.sources and "attempt_b" in node.sources
    assert node.confidence == 0.6
    assert lib.merge_log


def test_seed_has_no_post_2012_level_or_richer_hold():
    lib = seed_boundedgaps_2012()
    assert all(n.year_available <= 2012 for n in lib.nodes.values())
    assert not any(n.claim.weight_family == "richer" for n in lib.nodes.values())
    assert not any(n.claim.level_have == "gt_half_smooth" for n in lib.nodes.values())


def test_reframe_start_merges_with_seed_weights():
    lib = seed_boundedgaps_2012()
    before = set(lib.nodes)
    n = add_generator_starts(lib, "boundedgaps_2012", min_score=8, limit=20)
    assert n >= 1
    # WEIGHTS / BV-type starts should merge into existing seeds, not only add new ids.
    assert lib.merge_log or len(lib.nodes) < len(before) + n


def test_leakage_scan_climber():
    leak = leakage_scan()
    assert leak["ok"], leak["hits"]


def test_expensive_check_does_not_hold_open_enrichment():
    node = make_node(
        Claim(pred="weighted_detector", weight_family="richer", level_demand="any_positive", family="twins"),
        "sketch",
        0.55,
        2005,
        "t",
        "boundedgaps_2012",
        status="sketched",
    )
    r = check_node(node, year_cutoff=2012)
    assert r.status == "checked_unknown"
    r2 = check_node(
        make_node(
            Claim(pred="level_of_distribution", moduli="smooth", level_have="gt_half_smooth", family="twins", conditional=True),
            "sketch",
            0.5,
            1986,
            "t",
            "boundedgaps_2012",
        ),
        2012,
    )
    assert r2.status == "checked_unknown"


def test_parity_is_barrier():
    node = make_node(
        Claim(pred="bounded_gaps", barrier="parity", family="twins", weight_family="indicator"),
        "sketch",
        0.3,
        1919,
        "t",
        "boundedgaps_2012",
    )
    assert check_node(node, 2012).status == "checked_barrier"


def test_known_answer_gates_are_locked_honestly():
    """Run the official climber KA and lock whatever is true.

    Do not force PASS. If this fails after a real regression, fix the
    engine or update the locked vector with a confession.
    """
    from climb_gold import evaluate_known_answer
    from climber import enumerate_paths, path_record

    out = climb("boundedgaps_2012")
    lib = out["library"]
    paths = [path_record(lib, p) for p in enumerate_paths(lib)]
    gates = evaluate_known_answer(lib, paths, out["checks"])
    leak = leakage_scan()
    assert leak["ok"] is True
    assert gates["C1_nodes_exist"] is True
    assert gates["C1_paths_exist"] is True
    assert gates["C2_gold_beats_bad"] is True
    assert gates["C3_no_false_hold"] is True
    assert gates["C5_partials_kept"] is True
    assert gates["PASS"] is True
    # Weakness locked so it cannot be silently "fixed": translations
    # outrank gold paths. C2 only requires gold > known-bad.
    assert gates["best_gold_score"] < 0.08
    assert gates["best_bad_score"] < gates["best_gold_score"]


def test_landau_card_still_open_in_climber():
    assert CARDS["landau_2026"].year_cutoff == 2026
    out = climb("landau_2026", max_new_nodes=60, check_k=8)
    lib = out["library"]
    held_targets = [
        n
        for n in lib.nodes.values()
        if n.claim.pred == "prime_values"
        and n.claim.family == "n2plus1"
        and n.claim.extra_var == "no"
        and n.status == "checked_hold"
        and not n.claim.conditional
    ]
    assert held_targets == []
