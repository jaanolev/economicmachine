"""Cheap gut-feeling moves. Eyeballing climbs, not proofs.

A cheap model can follow CHEAP_CLIMBER_PROMPT. Tests use the mechanical
applicators below. Moves are generic sieve/geometry habits, not named
after later theorems.

Frozen 2026-10-10 before known-answer scoring.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from library import Claim, Edge, Library, Node, edge_id, make_node


CHEAP_CLIMBER_PROMPT = """
You are a cheap gut-feeling climber. You are NOT proving anything.
You sketch a short route from a KNOWN node toward a TARGET as a chain
of plausible lemmas. Each step gets a confidence in (0,1).

Rules:
- Do not invent theorems dated after the year cutoff.
- A step is a lemma-shaped claim (structured fields), not a paragraph.
- If a step would detect primes with Type I / indicator information only,
  still write it, but give it low confidence (the expensive check will
  look for the parity barrier).
- If a step specialises away an extra variable, give it low confidence.
- Store every step even if the route dies.

Output JSON:
{
  "steps": [
    {"move": "ENRICH_DETECTOR|CHANGE_SUPPORT|COMBINE|ASSUME_OPEN|TYPE_I_ONLY|HEURISTIC_CLOSE|SPECIALIZE|ENLARGE|TRANSLATE|RELATIVE_AMBIENT",
     "dst_claim": { ... Claim fields ... },
     "confidence": 0.4,
     "reason": "one line"}
  ]
}
""".strip()


@dataclass(frozen=True)
class Proposed:
    dst: Claim
    move: str
    confidence: float
    reason: str
    year_available: int


def _copy(c: Claim, **kwargs) -> Claim:
    data = c.as_dict()
    data.update(kwargs)
    return Claim(**data)


def move_enrich_detector(src: Node, card_id: str) -> list[Proposed]:
    c = src.claim
    if c.pred != "weighted_detector":
        return []
    if c.weight_family != "selberg_1d":
        return []
    dst = _copy(
        c,
        pred="weighted_detector",
        weight_family="richer",
        level_demand="any_positive",
    )
    return [
        Proposed(
            dst,
            "ENRICH_DETECTOR",
            0.55,
            "Richer detector class may lower the distribution demand.",
            max(src.year_available, 1947),
        )
    ]


def move_change_support(src: Node, card_id: str) -> list[Proposed]:
    c = src.claim
    if c.pred != "level_of_distribution":
        return []
    if c.moduli != "all" or c.level_have != "half":
        return []
    dst = _copy(
        c,
        pred="level_of_distribution",
        moduli="smooth",
        level_have="gt_half_smooth",
        conditional=True,
    )
    return [
        Proposed(
            dst,
            "CHANGE_SUPPORT",
            0.50,
            "Averages on a thinner well-factorable support are often cheaper.",
            max(src.year_available, 1986),
        )
    ]


def move_combine(src: Node, lib: Library, card_id: str) -> list[Proposed]:
    """Combine a detector with a distribution node already in the library."""
    out: list[Proposed] = []
    if src.claim.pred not in {"weighted_detector", "level_of_distribution"}:
        return out
    detectors = [n for n in lib.nodes.values() if n.claim.pred == "weighted_detector"]
    levels = [n for n in lib.nodes.values() if n.claim.pred == "level_of_distribution"]
    pairs: list[tuple[Node, Node]] = []
    if src.claim.pred == "weighted_detector":
        pairs = [(src, lv) for lv in levels]
    else:
        pairs = [(dt, src) for dt in detectors]
    family = "twins" if card_id.startswith("boundedgaps") else "n2plus1"
    for det, lv in pairs:
        meet = _meets(det.claim.level_demand, lv.claim.level_have)
        cond = bool(lv.claim.conditional or det.claim.conditional or not meet)
        dst = Claim(
            pred="bounded_gaps" if card_id.startswith("boundedgaps") else "prime_values",
            weight_family=det.claim.weight_family,
            moduli=lv.claim.moduli,
            level_demand=det.claim.level_demand,
            level_have=lv.claim.level_have,
            extra_var=det.claim.extra_var,
            conditional=cond,
            family=family,
        )
        conf = 0.70 if meet and not cond else (0.42 if meet else 0.28)
        out.append(
            Proposed(
                dst,
                "COMBINE",
                conf,
                f"Combine detector {det.id} with distribution {lv.id}; meet={meet}.",
                max(det.year_available, lv.year_available),
            )
        )
    return out


def _meets(demand: str, have: str) -> bool:
    if demand == "na" or have == "na":
        return False
    if demand == "any_positive" and have in {"half", "gt_half_smooth", "eh"}:
        return True
    if demand == "half" and have in {"half", "gt_half_smooth", "eh"}:
        return True
    if demand == "gt_half" and have in {"gt_half_smooth", "eh"}:
        return True
    return False


def move_assume_open(src: Node, card_id: str) -> list[Proposed]:
    c = src.claim
    if c.pred != "implication_open_hyp":
        return []
    family = "twins" if card_id.startswith("boundedgaps") else c.family
    dst = Claim(
        pred="bounded_gaps" if card_id.startswith("boundedgaps") else "prime_values",
        conditional=True,
        family=family,
        weight_family=c.weight_family,
        level_demand=c.level_demand,
        level_have="eh",
    )
    return [
        Proposed(
            dst,
            "ASSUME_OPEN",
            0.40,
            "Assume the open hypothesis in the implication; climb is conditional.",
            src.year_available,
        )
    ]


def move_type_i_only(src: Node, card_id: str) -> list[Proposed]:
    c = src.claim
    if c.pred not in {"weighted_detector", "almost_primes"}:
        return []
    if c.weight_family not in {"indicator", "selberg_1d", "na"}:
        return []
    family = "twins" if card_id.startswith("boundedgaps") else "n2plus1"
    dst = Claim(
        pred="bounded_gaps" if card_id.startswith("boundedgaps") else "prime_values",
        weight_family=c.weight_family if c.weight_family != "na" else "indicator",
        barrier="parity",
        family=family,
        extra_var="no",
    )
    return [
        Proposed(
            dst,
            "TYPE_I_ONLY",
            0.32,
            "Detect primes from Type I / indicator information only.",
            src.year_available,
        )
    ]


def move_heuristic_close(src: Node, card_id: str) -> list[Proposed]:
    if src.claim.pred not in {"heuristic", "level_of_distribution"}:
        return []
    if src.claim.pred == "level_of_distribution" and src.claim.level_have != "eh":
        return []
    family = "twins" if card_id.startswith("boundedgaps") else "n2plus1"
    dst = Claim(
        pred="bounded_gaps" if card_id.startswith("boundedgaps") else "prime_values",
        conditional=True,
        family=family,
        barrier="na",
    )
    # Force a distinct heuristic close even when ASSUME_OPEN already made a conditional target.
    dst = Claim(
        pred="heuristic_target",
        conditional=True,
        family=family,
    )
    return [
        Proposed(
            dst,
            "HEURISTIC_CLOSE",
            0.30,
            "Close the problem by a random-model or RH-quality heuristic.",
            src.year_available,
        )
    ]


def move_specialize(src: Node, card_id: str) -> list[Proposed]:
    if src.claim.extra_var != "yes":
        return []
    dst = _copy(src.claim, extra_var="no", pred=src.claim.pred if src.claim.pred != "prime_values" else "prime_values")
    if src.claim.pred in {"prime_values", "almost_primes"}:
        dst = _copy(dst, pred="prime_values", family="n2plus1", barrier="no_extra_variable")
    return [
        Proposed(
            dst,
            "SPECIALIZE",
            0.22,
            "Set the extra variable to a constant. This usually deletes the averaging.",
            src.year_available,
        )
    ]


def move_enlarge(src: Node, card_id: str) -> list[Proposed]:
    if src.claim.family not in {"n2plus1", "na"} and src.claim.pred != "prime_values":
        return []
    if src.claim.extra_var == "yes":
        return []
    if not card_id.startswith("landau") and src.claim.family != "n2plus1":
        return []
    dst = Claim(
        pred="prime_values",
        extra_var="yes",
        family="x2y4",
        weight_family=src.claim.weight_family,
    )
    return [
        Proposed(
            dst,
            "ENLARGE",
            0.48,
            "Enlarge to a family with a free variable.",
            src.year_available,
        )
    ]


def move_translate(src: Node, card_id: str) -> list[Proposed]:
    if src.claim.pred == "translation":
        return []
    if src.claim.family not in {"n2plus1", "twins", "na"} and src.claim.pred not in {
        "prime_values",
        "target",
        "bounded_gaps",
    }:
        return []
    dst = Claim(
        pred="translation",
        family=src.claim.family if src.claim.family != "na" else ("n2plus1" if card_id.startswith("landau") else "twins"),
        extra_var=src.claim.extra_var,
    )
    return [
        Proposed(
            dst,
            "TRANSLATE",
            0.38,
            "Rewrite in a neighbouring ring or language. Thin set may stay thin.",
            src.year_available,
        )
    ]


def move_relative_ambient(src: Node, card_id: str) -> list[Proposed]:
    if src.claim.pred in {"relative_density", "translation"}:
        return []
    dst = Claim(
        pred="relative_density",
        family=src.claim.family if src.claim.family != "na" else ("n2plus1" if card_id.startswith("landau") else "twins"),
        extra_var=src.claim.extra_var,
    )
    return [
        Proposed(
            dst,
            "RELATIVE_AMBIENT",
            0.34,
            "Treat the thin set as dense in a pseudorandom ambient.",
            src.year_available,
        )
    ]


def propose(src: Node, lib: Library, card_id: str) -> list[Proposed]:
    out: list[Proposed] = []
    out.extend(move_enrich_detector(src, card_id))
    out.extend(move_change_support(src, card_id))
    out.extend(move_combine(src, lib, card_id))
    out.extend(move_assume_open(src, card_id))
    out.extend(move_type_i_only(src, card_id))
    out.extend(move_heuristic_close(src, card_id))
    out.extend(move_specialize(src, card_id))
    out.extend(move_enlarge(src, card_id))
    out.extend(move_translate(src, card_id))
    out.extend(move_relative_ambient(src, card_id))
    return out


def apply_proposed(
    lib: Library,
    src: Node,
    prop: Proposed,
    source: str,
    card_id: str,
) -> tuple[Node, Edge]:
    node = make_node(
        prop.dst,
        kind="sketch",
        confidence=prop.confidence,
        year_available=prop.year_available,
        source=source,
        card_id=card_id,
        status="sketched",
    )
    node = lib.add_node(node)
    edge = Edge(
        id=edge_id(src.id, node.id, prop.move),
        src=src.id,
        dst=node.id,
        move=prop.move,
        confidence=prop.confidence,
        status="sketched",
        reason=prop.reason,
        sources=[source],
    )
    edge = lib.add_edge(edge)
    return node, edge


def sketch(lib: Library, card_id: str, max_depth: int = 3, max_new_nodes: int = 80) -> int:
    """Expand the library. Returns number of new nodes created."""
    created = 0
    wave = list(lib.nodes.values())
    for depth in range(max_depth):
        nxt: list[Node] = []
        # Stable order so tests are deterministic.
        for src in sorted(wave, key=lambda n: n.id):
            if created >= max_new_nodes:
                return created
            props = propose(src, lib, card_id)
            # Cap branching per node.
            props = sorted(props, key=lambda p: (-p.confidence, p.move, p.dst.equiv_key()))[:4]
            for i, prop in enumerate(props):
                if created >= max_new_nodes:
                    return created
                before = set(lib.nodes)
                node, _ = apply_proposed(
                    lib, src, prop, source=f"sketch:d{depth}:{src.id}:{prop.move}:{i}", card_id=card_id
                )
                if node.id not in before:
                    created += 1
                    nxt.append(node)
                elif node not in nxt:
                    nxt.append(node)
        wave = nxt
        if not wave:
            break
    return created
