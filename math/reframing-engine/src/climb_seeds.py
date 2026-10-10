"""Seed libraries: known results at the card cutoff. No later theorems."""

from __future__ import annotations

from library import Claim, Library, make_node


def seed_boundedgaps_2012() -> Library:
    lib = Library("boundedgaps_2012", 2012)
    cid = "boundedgaps_2012"

    def add(claim: Claim, kind: str, conf: float, year: int, source: str, status: str = "seed") -> None:
        lib.add_node(
            make_node(claim, kind, conf, year, source, cid, status=status)
        )

    add(
        Claim(pred="target", family="twins"),
        "target",
        1.0,
        1921,
        "seed:target",
    )
    add(
        Claim(pred="weighted_detector", weight_family="selberg_1d", level_demand="gt_half", family="twins"),
        "seed",
        0.85,
        2005,
        "seed:gpy_weights",
    )
    add(
        Claim(pred="level_of_distribution", moduli="all", level_have="half", family="twins"),
        "seed",
        0.90,
        1965,
        "seed:bv_half",
    )
    add(
        Claim(pred="level_of_distribution", moduli="smooth", level_have="half", family="twins"),
        "seed",
        0.70,
        1986,
        "seed:well_factorable_setting",
    )
    add(
        Claim(
            pred="implication_open_hyp",
            weight_family="selberg_1d",
            level_demand="gt_half",
            level_have="eh",
            family="twins",
        ),
        "seed",
        0.88,
        2005,
        "seed:open_hyp_implies_target",
    )
    add(
        Claim(pred="almost_primes", family="twins", extra_var="no"),
        "seed",
        0.92,
        1919,
        "seed:almost_twins",
    )
    add(
        Claim(pred="weighted_detector", weight_family="indicator", level_demand="gt_half", family="twins"),
        "seed",
        0.40,
        1919,
        "seed:raw_indicator",
    )
    add(
        Claim(pred="heuristic", family="twins"),
        "seed",
        0.35,
        1936,
        "seed:random_model",
    )
    return lib


def seed_landau_2026() -> Library:
    lib = Library("landau_2026", 2026)
    cid = "landau_2026"

    def add(claim: Claim, kind: str, conf: float, year: int, source: str) -> None:
        lib.add_node(make_node(claim, kind, conf, year, source, cid, status="seed"))

    add(Claim(pred="target", family="n2plus1", extra_var="no"), "target", 1.0, 1912, "seed:target")
    add(Claim(pred="almost_primes", family="n2plus1", extra_var="no"), "seed", 0.86, 1978, "seed:p2")
    add(Claim(pred="prime_values", family="x2y4", extra_var="yes"), "seed", 0.84, 1998, "seed:enlarged_family")
    add(Claim(pred="prime_values", family="two_squares", extra_var="yes"), "seed", 0.90, -100, "seed:two_squares")
    add(Claim(pred="prime_values", family="linear", extra_var="no"), "seed", 0.95, 1837, "seed:dirichlet")
    add(Claim(pred="weighted_detector", weight_family="selberg_1d", family="n2plus1", extra_var="no"), "seed", 0.70, 1978, "seed:sieve_weights")
    add(Claim(pred="translation", family="n2plus1", extra_var="no"), "seed", 0.80, -100, "seed:gaussian_line")
    add(Claim(pred="heuristic", family="n2plus1"), "seed", 0.40, 1962, "seed:bh")
    add(Claim(pred="level_of_distribution", moduli="all", level_have="half", family="n2plus1"), "seed", 0.75, 1965, "seed:bv")
    return lib


def reframe_to_node(card_id: str, object_id: str, template_id: str, score: int) -> tuple:
    """Turn a generator pairing into a start Claim. Mergeable with seeds."""
    from library import Claim

    family = "twins" if card_id.startswith("boundedgaps") else "n2plus1"
    conf = min(0.80, 0.35 + 0.03 * max(score, 0))
    if template_id == "WEIGHTS":
        claim = Claim(pred="weighted_detector", weight_family="selberg_1d", level_demand="gt_half", family=family)
    elif template_id == "RESTRICTED_SUPPORT":
        claim = Claim(pred="level_of_distribution", moduli="all", level_have="half", family=family)
    elif template_id == "BILINEAR":
        claim = Claim(pred="weighted_detector", weight_family="selberg_1d", extra_var="yes" if family == "n2plus1" else "no", family=family)
    elif template_id == "EMBED":
        claim = Claim(pred="prime_values", extra_var="yes", family="x2y4" if family == "n2plus1" else family)
    elif template_id == "TRANSLATE":
        claim = Claim(pred="translation", family=family)
    elif template_id == "HEURISTIC_MODEL":
        claim = Claim(pred="heuristic", family=family)
    elif template_id == "RELATIVE_DENSITY":
        claim = Claim(pred="relative_density", family=family)
    elif template_id == "DETECT" and object_id in {"sieve_weights_selberg", "bombieri_vinogradov"}:
        claim = Claim(pred="weighted_detector", weight_family="indicator", family=family)
    else:
        claim = Claim(pred="sketch_start", family=family)
    return claim, conf
