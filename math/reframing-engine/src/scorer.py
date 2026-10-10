"""Cheap scorer. Forbidden: gold labels, known_partials, problem-id branches,
winner names. Every feature is either computed from tags or flagged judgment.

Frozen 2026-10-10 before known-answer scores were computed.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from catalog import DistantObject, MATURITY_POINTS
from cards import ProblemCard
from templates import TEMPLATES, Template


# Areas that are "next door" to a problem area. Borrowing inside this
# neighbourhood does not earn the distant-borrow point.
NEARBY: dict[str, frozenset[str]] = {
    "analytic_nt": frozenset({"analytic_nt", "sieve", "algebraic_nt"}),
    "algebraic_nt": frozenset({"algebraic_nt", "arithmetic_geometry", "automorphic"}),
    "topology": frozenset({"topology", "geometric_analysis"}),
    "arithmetic_geometry": frozenset({"arithmetic_geometry", "algebraic_nt", "automorphic"}),
    "sieve": frozenset({"sieve", "analytic_nt"}),
    "additive_combinatorics": frozenset({"additive_combinatorics", "combinatorics"}),
    "geometric_analysis": frozenset({"geometric_analysis", "topology"}),
}


ATTACK_TEMPLATES = frozenset(
    {
        "RELATIVE_DENSITY",
        "WEIGHTS",
        "BILINEAR",
        "DEFORM",
        "EMBED",
        "MODULARITY",
        "DETECT",
        "RESTRICTED_SUPPORT",
    }
)
MILD_ATTACK = frozenset({"LOCAL_GLOBAL", "DUAL"})
NO_ATTACK = frozenset({"TRANSLATE", "HEURISTIC_MODEL"})


@dataclass
class Feature:
    name: str
    points: int
    kind: str  # "code" | "judgment"
    evidence: str


@dataclass
class Score:
    total: int
    features: list[Feature] = field(default_factory=list)
    flags: list[str] = field(default_factory=list)

    def as_dict(self) -> dict[str, Any]:
        return {
            "total": self.total,
            "features": [
                {
                    "name": f.name,
                    "points": f.points,
                    "kind": f.kind,
                    "evidence": f.evidence,
                }
                for f in self.features
            ],
            "flags": list(self.flags),
        }


def _feature_easier(card: ProblemCard, obj: DistantObject) -> Feature:
    hit = set(obj.solves_case_tags) & card.easier_tags()
    if not hit:
        return Feature(
            "easier_case",
            0,
            "code",
            "no overlap between object.solves_case_tags and card easier-case tags",
        )
    # Stronger if at least one overlapping tag is a *solved* easier case tag.
    solved_tags = set()
    for c in card.easier_cases:
        if c.status == "solved":
            solved_tags.update(c.tags)
    strong = hit & solved_tags
    if strong:
        return Feature(
            "easier_case",
            2,
            "code",
            f"object already solves solved-easier tags {sorted(strong)}",
        )
    return Feature(
        "easier_case",
        1,
        "code",
        f"weak overlap {sorted(hit)}",
    )


def _feature_barrier(card: ProblemCard, obj: DistantObject, tmpl: Template) -> Feature:
    offered = set(obj.addresses) | set(tmpl.addresses)
    hit = offered & card.barrier_tags()
    if not hit:
        return Feature(
            "barrier",
            0,
            "code",
            "object+template address none of the card's barrier tags",
        )
    # Naming a barrier is automatic here (tag overlap). +2 if the template
    # itself is one that can carry a mechanism, +1 if only the object matches.
    mechanism = set(tmpl.addresses) & card.barrier_tags()
    if mechanism and tmpl.id not in NO_ATTACK:
        return Feature(
            "barrier",
            2,
            "code",
            f"template {tmpl.id} carries mechanism tags {sorted(mechanism)}",
        )
    return Feature(
        "barrier",
        1,
        "code",
        f"object addresses {sorted(hit)} but template is not a mechanism for them",
    )


def _feature_code_shadow(obj: DistantObject, tmpl: Template) -> Feature:
    shadow = (obj.code_shadow or "") + " " + (tmpl.code_shadow or "")
    runnable_hints = (
        "n<=",
        "n<=N",
        "on n<=",
        "finite",
        "census",
        "count",
        "compute",
        "compare",
        "box",
        "Z/NZ",
        "triangulat",
    )
    if any(h in shadow.lower() for h in runnable_hints):
        if obj.maturity in {"heuristic", "speculative"}:
            return Feature(
                "code_shadow",
                1,
                "code",
                "finite shadow exists but object is heuristic/speculative",
            )
        return Feature(
            "code_shadow",
            2,
            "code",
            "finite computation is named in object or template shadow",
        )
    return Feature("code_shadow", 0, "code", "no finite shadow named")


def _feature_attack(tmpl: Template) -> Feature:
    if tmpl.id in ATTACK_TEMPLATES:
        return Feature(
            "attack_surface",
            2,
            "code",
            f"template {tmpl.id} changes averaging/weights/deformation/family",
        )
    if tmpl.id in MILD_ATTACK:
        return Feature(
            "attack_surface",
            1,
            "code",
            f"template {tmpl.id} is a language change with a possible principle",
        )
    return Feature(
        "attack_surface",
        0,
        "code",
        f"template {tmpl.id} is a translation or heuristic",
    )


def _feature_implication(tmpl: Template) -> Feature:
    # Mechanical generator always writes the template implication. That would
    # give every candidate +2 and be useless. Score the *quality* of the
    # implication by template class instead, and flag judgment.
    if tmpl.id == "HEURISTIC_MODEL":
        return Feature(
            "implication",
            0,
            "judgment",
            "heuristic models do not imply the original; flagged judgment",
        )
    if tmpl.id == "TRANSLATE":
        return Feature(
            "implication",
            1,
            "judgment",
            "equivalence is an implication both ways; no new leverage",
        )
    if tmpl.id in ATTACK_TEMPLATES or tmpl.id in MILD_ATTACK:
        return Feature(
            "implication",
            2,
            "judgment",
            "template writes T => original in the imported language; implication text is canned, not a checked proof",
        )
    return Feature("implication", 0, "judgment", "no implication pattern")


def _feature_maturity(obj: DistantObject) -> Feature:
    pts = MATURITY_POINTS[obj.maturity]
    return Feature("maturity", pts, "code", f"maturity={obj.maturity}")


def _feature_distant(card: ProblemCard, obj: DistantObject) -> Feature:
    nearby = NEARBY.get(card.area, frozenset({card.area}))
    if obj.area in nearby:
        return Feature(
            "distant_borrow",
            0,
            "code",
            f"object area {obj.area} is nearby {card.area}",
        )
    return Feature(
        "distant_borrow",
        1,
        "code",
        f"object area {obj.area} is distant from {card.area}",
    )


def _feature_circular(card: ProblemCard, obj: DistantObject, tmpl: Template) -> Feature:
    flags_penalty = 0
    evidence = []
    # Native language is the stuck language. Using it with a fancy
    # template is still a restatement. Applies to every template.
    if obj.id in card.native_object_ids:
        flags_penalty -= 2
        evidence.append("native object is a restatement of the stuck language")
    if obj.maturity in {"heuristic", "speculative"} and tmpl.id in ATTACK_TEMPLATES:
        flags_penalty -= 1
        evidence.append("attack template on a heuristic/speculative object")
    if not evidence:
        return Feature("circularity", 0, "code", "no circularity penalty")
    return Feature("circularity", flags_penalty, "code", "; ".join(evidence))


def score_pair(card: ProblemCard, obj: DistantObject, tmpl: Template) -> Score:
    features = [
        _feature_easier(card, obj),
        _feature_barrier(card, obj, tmpl),
        _feature_code_shadow(obj, tmpl),
        _feature_attack(tmpl),
        _feature_implication(tmpl),
        _feature_maturity(obj),
        _feature_distant(card, obj),
        _feature_circular(card, obj, tmpl),
    ]
    total = sum(f.points for f in features)
    flags = [f"{f.name}:{f.kind}" for f in features if f.kind == "judgment"]
    return Score(total=total, features=features, flags=flags)


def score_candidate(card: ProblemCard, candidate: dict[str, Any], obj: DistantObject) -> Score:
    tmpl = TEMPLATES[candidate["template_id"]]
    return score_pair(card, obj, tmpl)
