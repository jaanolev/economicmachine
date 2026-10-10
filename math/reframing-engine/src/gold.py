"""Gold labels and known-bad reframes for known-answer tests.

THIS MODULE IS THE ANSWER KEY. The scorer and generator must not import it.
Only the test harness (run_known_answers.py / verify.py) may import it.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class GoldSpec:
    card_id: str
    # A generated candidate matches gold if object_id in objects AND template_id in templates.
    objects: frozenset[str]
    templates: frozenset[str]
    note: str


@dataclass(frozen=True)
class BadSpec:
    card_id: str
    object_id: str
    template_id: str
    why_bad: str


# Official five. Written before looking at scores.
GOLD: dict[str, GoldSpec] = {
    "flt_1985": GoldSpec(
        "flt_1985",
        frozenset({"elliptic_curves", "modular_forms", "galois_representations"}),
        frozenset({"MODULARITY", "LOCAL_GLOBAL"}),
        (
            "Frey 1985 + Serre epsilon + Taniyama-Shimura: prove modularity of "
            "(semistable) elliptic curves. Ribet 1986 is after the cutoff; the "
            "reframe is already the proposed question."
        ),
    ),
    "poincare_1981": GoldSpec(
        "poincare_1981",
        frozenset({"harmonic_map_flow", "mean_curvature_flow", "minimal_surfaces"}),
        frozenset({"DEFORM"}),
        (
            "Ricci flow is not available in 1981. The honest ancestor is a "
            "geometric heat flow / canonical-metric deformation (Eells-Sampson 1964)."
        ),
    ),
    "poincare_1995": GoldSpec(
        "poincare_1995",
        frozenset({"ricci_flow"}),
        frozenset({"DEFORM"}),
        "Hamilton's program is already the community question.",
    ),
    "greentao_2003": GoldSpec(
        "greentao_2003",
        frozenset({"pseudorandom_majorants", "gowers_norms", "szemeredi_regularity"}),
        frozenset({"RELATIVE_DENSITY"}),
        "Transference: primes dense in a pseudorandom ambient.",
    ),
    "fi_1995": GoldSpec(
        "fi_1995",
        frozenset({"bilinear_forms_type_II", "switching_principle"}),
        frozenset({"BILINEAR", "EMBED"}),
        "Extra variable supplies Type II information that beats parity.",
    ),
    "boundedgaps_2012": GoldSpec(
        "boundedgaps_2012",
        frozenset(
            {
                "sieve_weights_selberg",
                "well_factorable_moduli",
                "bombieri_vinogradov",
            }
        ),
        frozenset({"WEIGHTS", "RESTRICTED_SUPPORT"}),
        "Maynard: better weights. Zhang: a bit more than BV on restricted moduli.",
    ),
}


# Known-bad = historically tried and stuck, or ignores a named barrier.
# Same schema as generated candidates so the scorer cannot treat them specially.
BADS: list[BadSpec] = [
    BadSpec(
        "flt_1985",
        "kummer_cyclotomic",
        "TRANSLATE",
        "Kummer already did this; irregular primes are the barrier.",
    ),
    BadSpec(
        "flt_1985",
        "class_groups",
        "TRANSLATE",
        "Iwasawa / class groups without a modularity attachment stay inside the stuck descent.",
    ),
    BadSpec(
        "poincare_1981",
        "morse_theory",
        "TRANSLATE",
        "Smale's method; Whitney trick fails in dimension 3.",
    ),
    BadSpec(
        "poincare_1981",
        "morse_theory",
        "DEFORM",
        "A Morse deformation still needs high-dimensional cancellation.",
    ),
    BadSpec(
        "poincare_1995",
        "morse_theory",
        "TRANSLATE",
        "Still fails in dimension 3 after Hamilton's program exists.",
    ),
    BadSpec(
        "greentao_2003",
        "szemeredi_regularity",
        "TRANSLATE",
        "Applies Szemeredi directly to a density-zero set.",
    ),
    BadSpec(
        "greentao_2003",
        "circle_method",
        "DETECT",
        "Circle method for arbitrary-length prime APs is the stuck traditional path.",
    ),
    BadSpec(
        "fi_1995",
        "sieve_weights_selberg",
        "WEIGHTS",
        "Selberg weights without Type II still hit parity, and the sequence is thinner than n^2+1.",
    ),
    BadSpec(
        "fi_1995",
        "gaussian_integers",
        "TRANSLATE",
        "x^2+y^4 = N(x+y^2 i) is a translation; without bilinear input it is Landau-like.",
    ),
    BadSpec(
        "boundedgaps_2012",
        "sieve_weights_selberg",
        "TRANSLATE",
        "Raw twin indicator / classical Selberg without the GPY improvement of weights or moduli.",
    ),
    BadSpec(
        "boundedgaps_2012",
        "l_functions",
        "HEURISTIC_MODEL",
        "Assuming RH-quality pair correlation does not produce an unconditional bounded gap.",
    ),
]


def is_gold(card_id: str, object_id: str, template_id: str) -> bool:
    spec = GOLD.get(card_id)
    if spec is None:
        return False
    return object_id in spec.objects and template_id in spec.templates


def bads_for(card_id: str) -> list[BadSpec]:
    return [b for b in BADS if b.card_id == card_id]
