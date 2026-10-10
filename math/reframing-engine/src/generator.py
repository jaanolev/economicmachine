"""Mechanical reframing generator plus a cheap-model prompt.

The procedure does not call a language model. It enumerates
(object, template) pairs that existed by the card's year cutoff and
fills a fixed schema. A small model can be asked to polish the text
using CHEAP_MODEL_PROMPT; polish is optional and is not used in tests.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any

from catalog import DistantObject, objects_available
from cards import ProblemCard
from templates import TEMPLATES, Template


CHEAP_MODEL_PROMPT = """
You are a cheap reframing generator for a hard math problem.

You will be given:
- a PROBLEM CARD (statement, barriers with tags, easier cases with tags, year cutoff)
- one DISTANT OBJECT from a frozen catalog (name, area, addresses, solves_case_tags)
- one TEMPLATE from a frozen list

Write ONE reframe. Follow the template's cheap_prompt. Do not invent theorems
dated after the year cutoff. Do not claim a proof of the original statement.

Output exactly this JSON:
{
  "title": "short name",
  "new_question": "the question you want asked instead",
  "transfer": "If T then original. Name T.",
  "easier_case_hook": "which listed easier case becomes a known theorem, or NONE",
  "barrier_hook": "which listed barrier you engage, or NONE",
  "code_shadow": "a finite computation with an N and an observable, or NONE",
  "known_or_failed": "known-and-stuck / known-open / new-looking / decorative",
  "honesty": "one sentence on why this might be empty"
}

Rules:
- If the template is TRANSLATE, say that the thin set stays thin.
- If the template is HEURISTIC_MODEL, mark transfer as heuristic, not a deduction.
- If you cannot attach the object to the problem, say so and mark decorative.
- Borrow the object; do not rename the original problem as the object.
""".strip()


@dataclass
class Candidate:
    id: str
    card_id: str
    object_id: str
    object_name: str
    object_area: str
    template_id: str
    title: str
    new_question: str
    transfer: str
    easier_case_hook: str
    barrier_hook: str
    code_shadow: str
    known_or_failed: str
    honesty: str
    year_available: int
    maturity: str
    generated_by: str = "mechanical_v1"
    notes: list[str] = field(default_factory=list)

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


def compatible(obj: DistantObject, tmpl: Template) -> bool:
    return tmpl.id in obj.templates_ok


def _easier_hook(card: ProblemCard, obj: DistantObject) -> str:
    hits = []
    obj_tags = set(obj.solves_case_tags)
    for case in card.easier_cases:
        if obj_tags & set(case.tags):
            hits.append(f"{case.id} ({case.note})")
    return " | ".join(hits) if hits else "NONE"


def _barrier_hook(card: ProblemCard, obj: DistantObject, tmpl: Template) -> str:
    offered = set(obj.addresses) | set(tmpl.addresses)
    hits = []
    for b in card.barriers:
        if offered & set(b.tags):
            hits.append(f"{b.id}: {b.note}")
    return " | ".join(hits) if hits else "NONE"


def _known_tag(card: ProblemCard, obj: DistantObject, tmpl: Template) -> str:
    if obj.id in card.native_object_ids and tmpl.id == "TRANSLATE":
        return "known-and-stuck"
    if obj.maturity == "heuristic":
        return "known-open"
    if obj.maturity == "speculative":
        return "decorative"
    if tmpl.id == "TRANSLATE":
        return "known-and-stuck"
    return "new-looking"


def fill(card: ProblemCard, obj: DistantObject, tmpl: Template) -> Candidate:
    cid = f"{card.id}::{obj.id}::{tmpl.id}"
    easier = _easier_hook(card, obj)
    barrier = _barrier_hook(card, obj, tmpl)
    transfer = tmpl.implication_pattern + f" Imported object: {obj.name}."
    if tmpl.id == "HEURISTIC_MODEL":
        transfer = (
            "HEURISTIC ONLY. "
            + tmpl.implication_pattern
            + f" Object: {obj.name}."
        )
    new_q = (
        f"[{tmpl.id} via {obj.name}] Recast: {card.statement} "
        f"as a statement about {obj.one_line} "
        f"using the move: {tmpl.cheap_prompt}"
    )
    honesty = (
        f"Mechanical pairing. Attachment quality is not checked beyond tag overlap. "
        f"Object available {obj.year_available} <= cutoff {card.year_cutoff}."
    )
    if obj.needs_attachment and tmpl.id in {"MODULARITY", "DETECT", "LOCAL_GLOBAL"}:
        honesty += " Needs an explicit attachment recipe; none is proved here."
    return Candidate(
        id=cid,
        card_id=card.id,
        object_id=obj.id,
        object_name=obj.name,
        object_area=obj.area,
        template_id=tmpl.id,
        title=f"{tmpl.id} + {obj.id}",
        new_question=new_q,
        transfer=transfer,
        easier_case_hook=easier,
        barrier_hook=barrier,
        code_shadow=f"{obj.code_shadow} / {tmpl.code_shadow}",
        known_or_failed=_known_tag(card, obj, tmpl),
        honesty=honesty,
        year_available=obj.year_available,
        maturity=obj.maturity,
        notes=[obj.one_line],
    )


def generate(card: ProblemCard) -> list[Candidate]:
    out: list[Candidate] = []
    for obj in objects_available(card.year_cutoff):
        for tmpl in TEMPLATES.values():
            if compatible(obj, tmpl):
                out.append(fill(card, obj, tmpl))
    return out


def generate_dicts(card: ProblemCard) -> list[dict[str, Any]]:
    return [c.as_dict() for c in generate(card)]
