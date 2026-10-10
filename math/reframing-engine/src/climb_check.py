"""Expensive checks on a few promising nodes. Code, not a language model.

A check may HOLD a pre-cutoff implication, mark BARRIER, FAIL a heuristic
as a proof, mark TRANSLATION, or leave UNKNOWN. It must not HOLD a
post-cutoff theorem. Year cutoff is an argument.

Finite shadows are tiny and are flagged as shadows, not HOLDs.
"""

from __future__ import annotations

from dataclasses import dataclass

from library import Library, Node


@dataclass
class CheckResult:
    status: str
    note: str
    kind: str  # code | judgment
    shadow: dict | None = None


def _meets(demand: str, have: str) -> bool:
    if demand == "any_positive" and have in {"half", "gt_half_smooth", "eh"}:
        return True
    if demand == "half" and have in {"half", "gt_half_smooth", "eh"}:
        return True
    if demand == "gt_half" and have in {"gt_half_smooth", "eh"}:
        return True
    return False


def toy_richer_weight_ratio() -> dict:
    """Rayleigh-quotient toy: more weight coordinates can raise a ratio.

    This is NOT a detection theorem. It is the gut-feeling shadow for
    ENRICH_DETECTOR. 1-d vector (1,) has ratio 1; (1,1) has ratio 2.
    """
    one = (1.0 * 1.0) / (1.0 * 1.0)
    two_num = (1.0 + 1.0) ** 2
    two_den = 1.0**2 + 1.0**2
    two = two_num / two_den
    return {"ratio_1d": one, "ratio_2d": two, "richer_wins_toy": two > one}


def check_node(node: Node, year_cutoff: int) -> CheckResult:
    c = node.claim

    if c.pred == "heuristic_target":
        return CheckResult(
            "checked_fail",
            "A heuristic close is not a deduction. Flagged judgment.",
            "judgment",
        )
    if c.pred == "translation":
        return CheckResult(
            "checked_translation",
            "Equivalence/dictionary holds as a rewrite; the thin set stays thin.",
            "judgment",
        )
    if c.pred == "relative_density":
        return CheckResult(
            "checked_unknown",
            "Relative-density transfer needs a constructed majorant. Not checked.",
            "judgment",
        )
    if c.barrier == "parity":
        return CheckResult(
            "checked_barrier",
            "Type I / indicator detection of primes hits the parity barrier.",
            "code",
        )
    if c.barrier == "no_extra_variable":
        return CheckResult(
            "checked_barrier",
            "Specialising away the extra variable deletes the bilinear input.",
            "judgment",
        )
    if c.pred == "weighted_detector" and c.weight_family == "richer":
        shadow = toy_richer_weight_ratio()
        # Cannot HOLD a post-2012 detection theorem. Toy shadow only.
        return CheckResult(
            "checked_unknown",
            "Toy Rayleigh quotient improves; no detection theorem is proved.",
            "code",
            shadow,
        )
    if c.pred == "level_of_distribution" and c.moduli == "smooth" and c.level_have == "gt_half_smooth":
        if year_cutoff < 2013:
            return CheckResult(
                "checked_unknown",
                "Well-factorable support is a known setting; a level above 1/2 on it is open at this cutoff.",
                "judgment",
            )
        return CheckResult(
            "checked_unknown",
            "Even after 2013 this check does not import a later theorem as a HOLD.",
            "judgment",
        )
    if c.pred in {"bounded_gaps", "prime_values"}:
        if c.conditional:
            return CheckResult(
                "checked_unknown",
                "Conditional close: the hypothesis remains open. Not an unconditional HOLD.",
                "judgment",
            )
        if c.weight_family == "richer" and c.level_demand == "any_positive" and _meets(c.level_demand, c.level_have):
            if year_cutoff < 2013:
                return CheckResult(
                    "checked_unknown",
                    "Detector-enrichment plus existing level 1/2 would close the target if the enrichment worked. Not held.",
                    "judgment",
                )
            return CheckResult(
                "checked_unknown",
                "Not held by this cheap checker even after the cutoff.",
                "judgment",
            )
        if c.moduli == "smooth" and c.level_have == "gt_half_smooth":
            return CheckResult(
                "checked_unknown",
                "Restricted-support plus a detector would close the target if the extra level were known. Not held.",
                "judgment",
            )
        if _meets(c.level_demand, c.level_have) and c.level_have == "eh" and c.level_demand == "gt_half":
            if year_cutoff >= 2005:
                return CheckResult(
                    "checked_hold",
                    "Pre-cutoff implication: an open level>1/2 hypothesis plus the 2005 weighted detector yields the target. HOLD the implication, not the hypothesis.",
                    "judgment",
                )
        return CheckResult(
            "checked_unknown",
            "Target-shaped node without a pre-cutoff closing theorem.",
            "judgment",
        )
    if c.pred == "implication_open_hyp" and year_cutoff >= 2005:
        return CheckResult(
            "checked_hold",
            "Seed implication with an open hypothesis is a known 2005-era lemma.",
            "judgment",
        )
    if c.pred == "level_of_distribution" and c.moduli == "all" and c.level_have == "half":
        return CheckResult(
            "checked_hold",
            "Averaged level 1/2 on all moduli is a 1965-era theorem.",
            "judgment",
        )
    if c.pred == "almost_primes":
        return CheckResult(
            "checked_hold",
            "Almost-prime results are seed theorems (Brun / linear sieve).",
            "judgment",
        )
    return CheckResult("checked_unknown", "No cheap check applies.", "judgment")


def promising_nodes(lib: Library, k: int = 8) -> list[Node]:
    """Barrier-shaped nodes are always cheap to check and always get checked.

    Remaining slots go to summit-faking claims (translation, heuristic,
    target-shaped), then raw gut confidence. k is a floor for the
    non-barrier batch; barrier nodes do not consume it.
    """
    sketched = [n for n in lib.nodes.values() if n.status == "sketched"]
    barriers = [n for n in sketched if n.claim.barrier != "na"]
    barriers.sort(key=lambda n: n.id)
    rest = [n for n in sketched if n.claim.barrier == "na"]
    forced: list[Node] = []
    for pred in (
        "translation",
        "heuristic_target",
        "bounded_gaps",
        "prime_values",
        "relative_density",
    ):
        group = [n for n in rest if n.claim.pred == pred]
        group.sort(key=lambda n: (-n.confidence, n.id))
        forced.extend(group)  # all of them: still a table lookup
    leftovers = [n for n in rest if n.id not in {x.id for x in forced}]
    leftovers.sort(key=lambda n: (-n.confidence, n.id))
    picked: list[Node] = list(barriers)
    seen = {n.id for n in picked}
    for n in forced + leftovers:
        if n.id in seen:
            continue
        non_barrier = sum(1 for x in picked if x.claim.barrier == "na")
        if non_barrier >= k:
            break
        picked.append(n)
        seen.add(n.id)
    return picked


def run_checks(lib: Library, year_cutoff: int, k: int = 8) -> list[dict]:
    out = []
    for node in promising_nodes(lib, k=k):
        result = check_node(node, year_cutoff)
        node.status = result.status
        node.check_note = result.note
        # Recalibrate this node's confidence immediately; path scores later.
        node.confidence = recalibrate_value(node.prior_confidence, result.status)
        rec = {
            "id": node.id,
            "statement": node.claim.statement(),
            "status": result.status,
            "note": result.note,
            "kind": result.kind,
            "shadow": result.shadow,
            "new_confidence": node.confidence,
        }
        out.append(rec)
        # Recalibrate incoming edges the same way.
        for e in lib.incoming(node.id):
            e.status = result.status
            e.confidence = recalibrate_value(e.confidence, result.status)
    return out


RECAL = {
    "checked_hold": 1.20,
    "checked_unknown": 0.95,
    "checked_translation": 0.70,
    "checked_fail": 0.25,
    "checked_barrier": 0.12,
    "sketched": 1.0,
    "seed": 1.0,
}


def recalibrate_value(conf: float, status: str) -> float:
    factor = RECAL.get(status, 1.0)
    out = conf * factor
    if out > 0.95:
        out = 0.95
    if out < 0.01:
        out = 0.01
    return out


def recalibrate_library(lib: Library) -> None:
    """Second pass: nodes that were not in the expensive batch keep priors;
    edges into barrier/fail nodes already updated. Soft-penalise parents of
    barriers so the climber learns.
    """
    for node in lib.nodes.values():
        if node.status in RECAL and node.status.startswith("checked"):
            node.confidence = recalibrate_value(node.prior_confidence, node.status)
        for e in lib.incoming(node.id):
            if node.status in {"checked_barrier", "checked_fail"}:
                parent = lib.nodes.get(e.src)
                if parent and parent.kind == "sketch" and parent.status == "sketched":
                    parent.confidence = max(0.01, parent.confidence * 0.85)
