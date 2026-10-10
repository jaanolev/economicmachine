"""Problem cards. Historical cards use a year cutoff and only pre-cutoff facts.

Hindsight rule: a card may list objects that existed by that year, including
failed attempts. It may not list the winning *proof*. It may list a community
program that already existed (Hamilton 1995, GPY 2005, Frey 1985).

Each easier case and barrier is tagged. The scorer sees tags, not narratives.
Gold labels do not live here.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class EasierCase:
    id: str
    tags: tuple[str, ...]
    status: str
    note: str


@dataclass(frozen=True)
class Barrier:
    id: str
    tags: tuple[str, ...]
    note: str


@dataclass
class ProblemCard:
    id: str
    title: str
    year_cutoff: int
    statement: str
    area: str
    native_object_ids: tuple[str, ...]
    barriers: list[Barrier]
    easier_cases: list[EasierCase]
    known_partials: list[str] = field(default_factory=list)
    # known_partials are for humans and the generator prompt.
    # The scorer is forbidden to read this field.
    prestate_honesty: str = ""
    unsure: list[str] = field(default_factory=list)

    def barrier_tags(self) -> set[str]:
        tags: set[str] = set()
        for b in self.barriers:
            tags.update(b.tags)
        return tags

    def easier_tags(self) -> set[str]:
        tags: set[str] = set()
        for c in self.easier_cases:
            tags.update(c.tags)
        return tags


def _flt_1985() -> ProblemCard:
    return ProblemCard(
        id="flt_1985",
        title="Fermat's Last Theorem (pre-Ribet, Frey announced)",
        year_cutoff=1985,
        statement=(
            "No nonzero integers a,b,c satisfy a^n+b^n=c^n for an integer n>2."
        ),
        area="algebraic_nt",
        native_object_ids=("kummer_cyclotomic",),
        barriers=[
            Barrier(
                "irregular_descent",
                ("regular_primes", "galois_constraints"),
                "Kummer's descent works for regular primes and stops for irregular ones.",
            ),
            Barrier(
                "no_variety",
                ("no_geometric_object", "local_global"),
                (
                    "The equation is a superelliptic curve; Faltings (1983) gives "
                    "finiteness of rational points on each curve x^n+y^n=1, not vanishing."
                ),
            ),
        ],
        easier_cases=[
            EasierCase(
                "n3n4",
                ("n_eq_3_or_4", "low_degree_diophantine"),
                "solved",
                "n=4 Fermat; n=3 Euler / descent on a genus-1 curve. Standard; not rechecked here.",
            ),
            EasierCase(
                "regular",
                ("regular_primes",),
                "solved",
                "Kummer: FLT for regular primes. Standard; not rechecked here.",
            ),
        ],
        known_partials=[
            "Kummer regular primes (19th c.).",
            "Faltings 1983: finitely many primitive solutions for each n, not none.",
            (
                "Hellegouarch (late 1960s-70s) attached the curve "
                "y^2 = x(x-a^n)(x+b^n) to a Fermat solution, without a modularity link. "
                "UNSURE of the exact first paper year; secondary sources say late 1960s."
            ),
            (
                "Frey, Oberwolfach 1985: that curve should not be modular. "
                "Serre's epsilon conjecture is being formulated (letter to Mestre, Aug 1985). "
                "Ribet has not yet proved epsilon (July 1986)."
            ),
            "Taniyama-Shimura-Weil: every elliptic curve over Q is modular. Open. Weil 1967.",
        ],
        prestate_honesty=(
            "This is NOT a 1637 card. The question-change 'prove modularity of "
            "elliptic curves' is already being proposed in 1985. A 1637 generator "
            "could not have named modular forms. The test asks whether a 1985 "
            "card ranks that already-proposed reframe above known-bad descents."
        ),
        unsure=[
            "Exact year of Hellegouarch's first paper attaching those curves (secondary sources: late 1960s).",
            "Whether Frey's 1985 Oberwolfach remarks were already written as a preprint the same year.",
        ],
    )


def _poincare_1981() -> ProblemCard:
    return ProblemCard(
        id="poincare_1981",
        title="Poincare conjecture (pre-Hamilton Ricci flow)",
        year_cutoff=1981,
        statement=(
            "Every closed simply-connected 3-manifold is homeomorphic to S^3."
        ),
        area="topology",
        native_object_ids=("morse_theory",),
        barriers=[
            Barrier(
                "dim3",
                ("high_dimension_only", "no_canonical_geometry"),
                "Smale's h-cobordism / Whitney trick needs dim>=5. Dimension 4 is Freedman/Donaldson later.",
            ),
            Barrier(
                "no_metric_program",
                ("no_canonical_geometry", "deform_to_model"),
                "There is no canonical Riemannian metric produced by a working deformation.",
            ),
        ],
        easier_cases=[
            EasierCase(
                "dim_ge_5",
                ("dim_ge_5",),
                "solved",
                "Smale 1961, h-cobordism. Standard; not rechecked here.",
            ),
            EasierCase(
                "dim2",
                ("dim2_uniformization",),
                "solved",
                "Uniformization of surfaces is classical. Ricci flow is not yet a tool.",
            ),
        ],
        known_partials=[
            "Smale 1961: high-dimensional Poincare.",
            "Eells-Sampson 1964: harmonic map heat flow exists as a tool in geometric analysis.",
            "Thurston geometrization is being formulated around 1977-82; UNSURE how much is public as a precise conjecture in 1981.",
            "Hamilton's Ricci flow paper is 1982 and is NOT available.",
        ],
        prestate_honesty=(
            "Ricci flow does not exist as a named tool. The honest gold is "
            "'borrow a geometric heat flow (Eells-Sampson style) and deform a metric "
            "or map toward a model'. Naming Ricci flow exactly would be leakage."
        ),
        unsure=[
            "How widely Thurston's geometrization conjecture was circulated in 1981.",
            "Whether any Ricci-type flow was discussed informally before the 1982 paper.",
        ],
    )


def _poincare_1995() -> ProblemCard:
    return ProblemCard(
        id="poincare_1995",
        title="Poincare conjecture (Hamilton program exists)",
        year_cutoff=1995,
        statement=(
            "Every closed simply-connected 3-manifold is homeomorphic to S^3."
        ),
        area="topology",
        native_object_ids=("morse_theory", "thurston_geometrization"),
        barriers=[
            Barrier(
                "singularities",
                ("singularities", "deform_to_model", "no_canonical_geometry"),
                "Hamilton can run Ricci flow until pinch. Surgery in dim 3 and non-collapsing are missing.",
            ),
            Barrier(
                "dim3_morse",
                ("high_dimension_only",),
                "Morse / Whitney still fail in dimension 3.",
            ),
        ],
        easier_cases=[
            EasierCase(
                "pos_ricci",
                ("positive_ricci",),
                "solved",
                "Hamilton 1982: positive Ricci curvature 3-manifolds are spherical.",
            ),
            EasierCase(
                "dim2_rf",
                ("dim2_uniformization",),
                "solved",
                "Hamilton/Chow: Ricci flow on surfaces recovers uniformization. Standard; not rechecked here.",
            ),
            EasierCase(
                "haken",
                ("haken_manifolds",),
                "solved",
                "Thurston: geometrization for Haken manifolds. Standard; not rechecked here.",
            ),
        ],
        known_partials=[
            "Hamilton 1982 Ricci flow; 1995 survey on singularities.",
            "The community question is already: carry out Hamilton's program.",
            "Perelman's entropy / reduced volume (2002) are NOT available.",
        ],
        prestate_honesty=(
            "This card tests ranking of an already-named community reframe "
            "against Morse theory and decorative borrows. It does not test "
            "inventing Ricci flow."
        ),
    )


def _greentao_2003() -> ProblemCard:
    return ProblemCard(
        id="greentao_2003",
        title="arbitrarily long APs of primes (pre-Green-Tao)",
        year_cutoff=2003,
        statement=(
            "The primes contain arithmetic progressions of arbitrary finite length."
        ),
        area="analytic_nt",
        native_object_ids=("l_functions",),
        barriers=[
            Barrier(
                "density_zero",
                ("density_zero", "need_relative_density"),
                "Szemeredi needs positive upper density. Primes have density zero.",
            ),
            Barrier(
                "circle_hard",
                ("additive_problems", "thin_sequence"),
                "The circle method gives length 3 (van der Corput) and struggles for arbitrary length.",
            ),
        ],
        easier_cases=[
            EasierCase(
                "szemeredi",
                ("positive_density_aps",),
                "solved",
                "Szemeredi 1975. Standard; not rechecked here.",
            ),
            EasierCase(
                "length3",
                ("length3_primes",),
                "solved",
                "van der Corput 1939: infinitely many 3-term APs of primes. Standard; not rechecked here.",
            ),
        ],
        known_partials=[
            "Szemeredi 1975.",
            "van der Corput 1939, length 3.",
            "Gowers 2001: quantitative Szemeredi via uniformity norms.",
            (
                "Goldston-Yildirim truncated divisor sums / almost-primes are in circulation "
                "around 2003. UNSURE of the exact preprint month a 2003 reader would have."
            ),
        ],
        prestate_honesty=(
            "The objects (Szemeredi, Gowers norms, almost-prime majorants) exist. "
            "The reframe is the pairing: primes as a dense subset of a pseudorandom set."
        ),
        unsure=[
            "Exact public date of the Goldston-Yildirim truncated-divisor-sum paper a 2003 reader would cite.",
        ],
    )


def _fi_1995() -> ProblemCard:
    return ProblemCard(
        id="fi_1995",
        title="primes of the form x^2+y^4 (pre-Friedlander-Iwaniec)",
        year_cutoff=1995,
        statement="There are infinitely many primes of the form x^2+y^4.",
        area="analytic_nt",
        native_object_ids=("gaussian_integers", "half_dimensional_sieve"),
        barriers=[
            Barrier(
                "parity",
                ("parity_barrier", "thin_sequence"),
                "Classical sieves cannot separate primes from P2. The sequence is thinner than n^2+1.",
            ),
            Barrier(
                "degree",
                ("degree_ge_2", "no_extra_variable"),
                "No univariate polynomial of degree >=2 is known to take infinitely many prime values.",
            ),
        ],
        easier_cases=[
            EasierCase(
                "two_sq",
                ("two_squares", "p_1_mod_4"),
                "solved",
                "Infinitely many primes x^2+y^2 (Fermat + Dirichlet). Union over all lines, not one line.",
            ),
            EasierCase(
                "dirichlet",
                ("linear_dirichlet",),
                "solved",
                "Dirichlet: linear polynomials with no fixed prime divisor.",
            ),
            EasierCase(
                "p2_quad",
                ("almost_primes",),
                "solved",
                "Iwaniec 1978: n^2+1 is P2 infinitely often. DESCRIBED, not re-proved here.",
            ),
        ],
        known_partials=[
            "Iwaniec 1978 P2 for n^2+1 (literature; not used as a lemma we proved).",
            "Parity barrier: Selberg; Bombieri; Friedlander-Iwaniec expositions.",
            "Asymptotic sieve / bilinear forms: Bombieri, Friedlander-Iwaniec 1980s-90s exist as a method looking for an input.",
        ],
        prestate_honesty=(
            "The extra variable y is already in the problem statement. The reframe "
            "is to treat that extra variable as a source of bilinear forms that beat parity."
        ),
    )


def _boundedgaps_2012() -> ProblemCard:
    return ProblemCard(
        id="boundedgaps_2012",
        title="bounded gaps between primes (GPY known, Zhang/Maynard not)",
        year_cutoff=2012,
        statement="liminf (p_{n+1}-p_n) is finite.",
        area="analytic_nt",
        native_object_ids=("sieve_weights_selberg", "bombieri_vinogradov"),
        barriers=[
            Barrier(
                "level",
                ("insufficient_level_of_distribution", "tuple_detection"),
                (
                    "GPY (2005): Elliott-Halberstam (level > 1/2) implies bounded gaps. "
                    "Bombieri-Vinogradov gives level 1/2, just short."
                ),
            ),
            Barrier(
                "parity",
                ("parity_barrier",),
                "A raw twin-sieve still hits parity if it tries to detect two primes with Type I information only.",
            ),
        ],
        easier_cases=[
            EasierCase(
                "gpy_on_eh",
                ("eh_implies_bounded_gaps",),
                "solved",
                "Goldston-Pintz-Yildirim 2005: EH => bounded gaps. Literature; not re-proved here.",
            ),
            EasierCase(
                "almost_twins",
                ("brun_almost_twins", "almost_primes"),
                "solved",
                "Brun: infinitely many p such that p+2 is P2 (almost-twins). Standard; not rechecked here.",
            ),
        ],
        known_partials=[
            "GPY 2005: liminf (p_{n+1}-p_n)/log p_n = 0, and EH => bounded gaps.",
            "Bombieri-Vinogradov 1965: level 1/2 on average.",
            "Bombieri-Friedlander-Iwaniec / Fouvry-Iwaniec: distribution on well-factorable moduli, 1980s.",
            "Zhang 2013 and Maynard 2013 are NOT available.",
        ],
        prestate_honesty=(
            "The community question is already 'improve GPY'. Gold pairings are "
            "(i) better weights that need less distribution, (ii) a bit more than "
            "BV on restricted moduli. This tests ranking, not inventing GPY."
        ),
    )


def _landau_2026() -> ProblemCard:
    return ProblemCard(
        id="landau_2026",
        title="Landau n^2+1 (current, still open)",
        year_cutoff=2026,
        statement="There are infinitely many integers n such that n^2+1 is prime.",
        area="analytic_nt",
        native_object_ids=("gaussian_integers", "half_dimensional_sieve", "bateman_horn"),
        barriers=[
            Barrier(
                "parity",
                ("parity_barrier", "thin_sequence"),
                (
                    "Linear / combinatorial sieves reach P2, not primes. Iwaniec 1978 is "
                    "the face of this barrier for this sequence. DESCRIBED, not claimed."
                ),
            ),
            Barrier(
                "one_var",
                ("degree_ge_2", "no_extra_variable", "thin_sequence"),
                (
                    "The sequence has ~X values up to size X^2. Friedlander-Iwaniec need "
                    "the extra variable in x^2+y^4. Setting y=1 is the open slice."
                ),
            ),
            Barrier(
                "line",
                ("thin_sequence",),
                "n+i is the line Im=1 in Z[i]. The prime ideal theorem does not save a single line.",
            ),
        ],
        easier_cases=[
            EasierCase(
                "two_sq",
                ("two_squares", "p_1_mod_4"),
                "solved",
                "Infinitely many primes x^2+y^2. Union of lines, not Im=1.",
            ),
            EasierCase(
                "dirichlet",
                ("linear_dirichlet",),
                "solved",
                "Dirichlet on linear polynomials.",
            ),
            EasierCase(
                "p2",
                ("almost_primes",),
                "solved",
                "Iwaniec 1978: n^2+1 is P2 infinitely often. Literature; not a lemma of this repo.",
            ),
            EasierCase(
                "x2y4",
                ("extra_variable_polynomials",),
                "solved",
                "Friedlander-Iwaniec 1997/98: infinitely many primes x^2+y^4. y=1 is Landau. Literature.",
            ),
        ],
        known_partials=[
            "Odd prime factors of n^2+1 are 1 mod 4 (elementary).",
            "Iwaniec 1978 P2 (literature).",
            "Friedlander-Iwaniec x^2+y^4 (literature).",
            "Harman-Lewis: primes x^2+y^2 with y = O(p^{0.119}) (literature; UNSURE of the exact exponent citation without the paper in hand).",
            "Ankeny-Kubilius: y = O(log p) on a GRH for Hecke L-functions (conditional, literature).",
            "Green-Sawhney 2024: infinitely many primes p^2 + n q^2 for certain n. Different problem.",
            "No univariate degree>=2 polynomial is known to take infinitely many prime values.",
        ],
        prestate_honesty=(
            "Open problem. The engine must not claim a proof. Several high-scoring "
            "reframings will be known and already stuck (Z[i] translation, FI with y=1, "
            "P2 sieve, Bateman-Horn)."
        ),
        unsure=[
            "Exact Harman-Lewis exponent 0.119 taken from secondary summary (Wikipedia / survey); not re-read from the paper.",
        ],
    )


CARDS: dict[str, ProblemCard] = {
    "flt_1985": _flt_1985(),
    "poincare_1981": _poincare_1981(),
    "poincare_1995": _poincare_1995(),
    "greentao_2003": _greentao_2003(),
    "fi_1995": _fi_1995(),
    "boundedgaps_2012": _boundedgaps_2012(),
    "landau_2026": _landau_2026(),
}


OFFICIAL_KNOWN_ANSWER_IDS = (
    "flt_1985",
    "poincare_1981",
    "greentao_2003",
    "fi_1995",
    "boundedgaps_2012",
)
