"""Frozen transfer templates for the reframing generator.

These are the only ways the engine is allowed to glue a distant object
to a problem. Do not add a template to fit a historical winner; add one
only if it names a reusable move. Dated 2026-10-10, frozen before scoring.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Template:
    id: str
    extra_averaging: bool
    addresses: tuple[str, ...]
    implication_pattern: str
    code_shadow: str
    cheap_prompt: str  # instructions a small model can follow


TEMPLATES: dict[str, Template] = {
    "DETECT": Template(
        id="DETECT",
        extra_averaging=True,
        addresses=("tuple_detection", "need_detector"),
        implication_pattern=(
            "If the imported object already detects the desired "
            "arithmetic/topological objects, then a positive detection "
            "theorem for that object implies the original statement."
        ),
        code_shadow="Count detections of the imported object on a finite range and compare to a null model.",
        cheap_prompt=(
            "Rewrite the problem as: detect the target objects using an "
            "object that already has a detection theorem. Write T => original."
        ),
    ),
    "DEFORM": Template(
        id="DEFORM",
        extra_averaging=True,
        addresses=("no_canonical_geometry", "deform_to_model", "singularities"),
        implication_pattern=(
            "If a deformation of the native structure converges (after "
            "controlled surgeries) to a model object whose classification "
            "implies the original statement, then the original follows."
        ),
        code_shadow="Run a discrete/toy flow on a small triangulated or metric example and record singularity types.",
        cheap_prompt=(
            "Replace the static object by a flow or deformation. Name the "
            "monotone quantity and what a singularity would mean for the claim."
        ),
    ),
    "RELATIVE_DENSITY": Template(
        id="RELATIVE_DENSITY",
        extra_averaging=True,
        addresses=("density_zero", "need_relative_density", "thin_sequence"),
        implication_pattern=(
            "If the native set is a positive-density subset of a "
            "pseudorandom ambient, and a dense-set theorem transfers to "
            "that ambient, then the original statement follows."
        ),
        code_shadow="On {1..N}, compare relative density of the native set inside a sifted/pseudorandom majorant vs absolute density.",
        cheap_prompt=(
            "Do not apply a positive-density theorem to a density-zero set. "
            "Name an ambient, a relative-density claim, and a transference step."
        ),
    ),
    "WEIGHTS": Template(
        id="WEIGHTS",
        extra_averaging=True,
        addresses=(
            "parity_barrier",
            "insufficient_level_of_distribution",
            "tuple_detection",
        ),
        implication_pattern=(
            "If a weighted detector (not the raw indicator) has a main term "
            "that dominates the remainder for the original counting problem, "
            "then a positive weighted count implies the original statement."
        ),
        code_shadow="Compare a raw indicator count to a Selberg-style weighted count on n<=N; record the main-term/remainder ratio.",
        cheap_prompt=(
            "Replace the indicator of the target by explicit weights. "
            "State the level of distribution the weights demand."
        ),
    ),
    "BILINEAR": Template(
        id="BILINEAR",
        extra_averaging=True,
        addresses=("parity_barrier", "thin_sequence"),
        implication_pattern=(
            "If the sequence admits a Type I / Type II factorization whose "
            "bilinear forms can be estimated beyond the parity barrier, "
            "then a prime-detecting sieve applies and the original follows."
        ),
        code_shadow="Write a finite bilinear expansion of the sequence up to N and check whether off-diagonal correlations decay.",
        cheap_prompt=(
            "Factor the sequence (or its von Mangoldt weights) into a "
            "bilinear form. Name the Type II range you would need."
        ),
    ),
    "MODULARITY": Template(
        id="MODULARITY",
        extra_averaging=True,
        addresses=("local_global", "no_geometric_object", "galois_constraints"),
        implication_pattern=(
            "If a geometric object attached to a hypothetical counterexample "
            "must be modular/automorphic, and modularity of that object is "
            "incompatible with the counterexample, then the original follows."
        ),
        code_shadow="For small hypothetical or real points, compute the attached object's conductor / a_p and test a modularity matching condition.",
        cheap_prompt=(
            "Attach a variety or Galois representation to a hypothetical "
            "solution. Write: modularity of the attachment => original."
        ),
    ),
    "EMBED": Template(
        id="EMBED",
        extra_averaging=True,
        addresses=("thin_sequence", "no_extra_variable", "degree_ge_2"),
        implication_pattern=(
            "If a larger family with an extra free variable is known (or "
            "easier) to satisfy the analog, and a specialization argument "
            "returns the original family, then the original follows. "
            "Specialization is the hard step and must be named."
        ),
        code_shadow="Count primes (or almost-primes) in the enlarged family vs the specialized slice on a finite box.",
        cheap_prompt=(
            "Add a free variable or enlarge the family. State why the "
            "enlarged problem is easier and what specialization would cost."
        ),
    ),
    "DUAL": Template(
        id="DUAL",
        extra_averaging=True,
        addresses=("parity_barrier", "insufficient_level_of_distribution"),
        implication_pattern=(
            "If a dual/adjoint form of the counting problem is tractable "
            "and a duality identity returns information about the original, "
            "then the original follows from the dual estimate."
        ),
        code_shadow="On a finite interval, compare a primal count to its dual (e.g. complementary sieve remainder).",
        cheap_prompt=(
            "Write the adjoint/dual problem. Name the identity that returns "
            "to the original count."
        ),
    ),
    "LOCAL_GLOBAL": Template(
        id="LOCAL_GLOBAL",
        extra_averaging=False,
        addresses=("local_global", "no_local_obstruction"),
        implication_pattern=(
            "If every local condition is satisfied and a local-to-global "
            "principle for the imported object is known, then a global "
            "object exists and the original follows."
        ),
        code_shadow="Check local solubility / local densities at many primes and compare to a predicted global count.",
        cheap_prompt=(
            "List local conditions. Name a local-to-global theorem for the "
            "imported object, and the remaining obstruction."
        ),
    ),
    "TRANSLATE": Template(
        id="TRANSLATE",
        extra_averaging=False,
        addresses=(),
        implication_pattern=(
            "The original statement is equivalent to a statement in the "
            "imported language. This changes vocabulary, not averaging."
        ),
        code_shadow="Check the claimed equivalence on a finite sample.",
        cheap_prompt=(
            "Give a literal dictionary between the original objects and the "
            "imported ones. If the thin set stays thin, say so."
        ),
    ),
    "HEURISTIC_MODEL": Template(
        id="HEURISTIC_MODEL",
        extra_averaging=False,
        addresses=("density_zero", "thin_sequence"),
        implication_pattern=(
            "A random model predicts the original. This is not a proof "
            "implication; it is a checkable prediction."
        ),
        code_shadow="Compare a finite census to the model's main-term prediction; record the ratio.",
        cheap_prompt=(
            "Write the random model and its main term. Mark the implication "
            "as heuristic, not a deduction."
        ),
    ),
    "RESTRICTED_SUPPORT": Template(
        id="RESTRICTED_SUPPORT",
        extra_averaging=True,
        addresses=("insufficient_level_of_distribution", "parity_barrier"),
        implication_pattern=(
            "If a distribution theorem holds on a thinner but better-behaved "
            "set of moduli (or support), and the original detector can be "
            "restricted to that support, then the original follows."
        ),
        code_shadow="Compare distribution remainders on all moduli <=Q vs smooth/well-factorable moduli <=Q.",
        cheap_prompt=(
            "Restrict moduli or support. Name the lost density and the "
            "gained distribution."
        ),
    ),
}


def all_templates() -> list[Template]:
    return list(TEMPLATES.values())
