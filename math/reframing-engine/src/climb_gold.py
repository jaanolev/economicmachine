"""Gold path shapes for the climber known-answer test.

THE CLIMBER MUST NOT IMPORT THIS. Only run_climber / test_climber may.
"""

from __future__ import annotations

from library import Library, Node


# A path is enrich-shaped if it contains the richer-detector node that
# lowers demand to any_positive, coming from a 1-d weighted detector.
def is_enrich_shaped(lib: Library, ids: list[str]) -> bool:
    nodes = [lib.nodes[i] for i in ids]
    has_1d = any(
        n.claim.pred == "weighted_detector" and n.claim.weight_family == "selberg_1d"
        for n in nodes
    )
    has_richer = any(
        n.claim.pred == "weighted_detector"
        and n.claim.weight_family == "richer"
        and n.claim.level_demand == "any_positive"
        for n in nodes
    )
    # Must actually aim at the target, not wander off into a translation.
    has_target = any(
        n.claim.pred == "bounded_gaps"
        and n.claim.weight_family == "richer"
        and n.claim.level_demand == "any_positive"
        for n in nodes
    )
    return has_1d and has_richer and has_target


def is_support_shaped(lib: Library, ids: list[str]) -> bool:
    nodes = [lib.nodes[i] for i in ids]
    has_all_half = any(
        n.claim.pred == "level_of_distribution"
        and n.claim.moduli == "all"
        and n.claim.level_have == "half"
        for n in nodes
    )
    has_smooth = any(
        n.claim.pred == "level_of_distribution"
        and n.claim.moduli == "smooth"
        and n.claim.level_have == "gt_half_smooth"
        for n in nodes
    )
    has_target = any(
        n.claim.pred == "bounded_gaps" and n.claim.moduli == "smooth"
        for n in nodes
    )
    return has_all_half and has_smooth and has_target


def is_raw_twin_bad(lib: Library, ids: list[str]) -> bool:
    nodes = [lib.nodes[i] for i in ids]
    return any(n.claim.barrier == "parity" for n in nodes) or any(
        n.claim.weight_family == "indicator" and n.claim.pred in {"bounded_gaps", "prime_values"}
        for n in nodes
    )


def is_heuristic_bad(lib: Library, ids: list[str]) -> bool:
    nodes = [lib.nodes[i] for i in ids]
    return any(n.claim.pred == "heuristic_target" for n in nodes)


def library_has_enrich_node(lib: Library) -> bool:
    return any(
        n.claim.pred == "weighted_detector"
        and n.claim.weight_family == "richer"
        and n.claim.level_demand == "any_positive"
        for n in lib.nodes.values()
    )


def library_has_support_node(lib: Library) -> bool:
    return any(
        n.claim.pred == "level_of_distribution"
        and n.claim.moduli == "smooth"
        and n.claim.level_have == "gt_half_smooth"
        for n in lib.nodes.values()
    )


def no_postcutoff_hold_on_open_lemmas(lib: Library) -> bool:
    """C3: enrich-detector and extra-level-on-smooth must not be HOLD."""
    for n in lib.nodes.values():
        if n.status != "checked_hold":
            continue
        c = n.claim
        if c.pred == "weighted_detector" and c.weight_family == "richer":
            return False
        if c.pred == "level_of_distribution" and c.level_have == "gt_half_smooth":
            return False
        if (
            c.pred in {"bounded_gaps", "prime_values"}
            and not c.conditional
            and (
                c.weight_family == "richer"
                or c.level_have == "gt_half_smooth"
            )
        ):
            return False
    return True


def evaluate_known_answer(lib: Library, paths: list[dict], checks: list[dict]) -> dict:
    enrich_paths = [p for p in paths if is_enrich_shaped(lib, p["node_ids"])]
    support_paths = [p for p in paths if is_support_shaped(lib, p["node_ids"])]
    bad_paths = [
        p
        for p in paths
        if is_raw_twin_bad(lib, p["node_ids"]) or is_heuristic_bad(lib, p["node_ids"])
    ]
    best_gold = 0.0
    if enrich_paths:
        best_gold = max(best_gold, max(p["score"] for p in enrich_paths))
    if support_paths:
        best_gold = max(best_gold, max(p["score"] for p in support_paths))
    best_bad = max((p["score"] for p in bad_paths), default=0.0)

    c1 = library_has_enrich_node(lib) and library_has_support_node(lib)
    c1_paths = bool(enrich_paths) and bool(support_paths)
    c2 = bool((enrich_paths or support_paths) and best_gold > best_bad)
    c3 = no_postcutoff_hold_on_open_lemmas(lib)
    # C5: some sketched node is not on a gold-shaped path
    gold_ids = set()
    for p in enrich_paths + support_paths:
        gold_ids.update(p["node_ids"])
    extras = [
        n
        for n in lib.nodes.values()
        if n.kind == "sketch" and n.id not in gold_ids
    ]
    c5 = len(extras) >= 1

    return {
        "C1_nodes_exist": c1,
        "C1_paths_exist": c1_paths,
        "C2_gold_beats_bad": c2,
        "C3_no_false_hold": c3,
        "C5_partials_kept": c5,
        "n_enrich_paths": len(enrich_paths),
        "n_support_paths": len(support_paths),
        "n_bad_paths": len(bad_paths),
        "best_gold_score": best_gold,
        "best_bad_score": best_bad,
        "n_extra_sketches": len(extras),
        "n_checks": len(checks),
        "PASS": bool(c1 and c1_paths and c2 and c3 and c5),
    }
