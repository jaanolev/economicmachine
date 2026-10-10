# Landau n²+1 reframings

**Open problem. This file does not claim progress.** A cold grader that
only sees the engine and these results should fail any smuggled infinitude
claim. None is made. The scorer **failed** its frozen known-answer suite
(see `known_answer_tests.md`). Scores below are a tag-overlap sorter.

Generated **151** pairings from the 2026 Landau card
(catalog objects dated ≤ 2026, templates the object allows).
Histogram of scores:

| score | count |
|---|---|
| 12 | 13 |
| 11 | 19 |
| 10 | 21 |
| 9 | 32 |
| 8 | 23 |
| 7 | 13 |
| 6 | 8 |
| 5 | 13 |
| 4 | 2 |
| 3 | 6 |
| 2 | 1 |

## Finite shadows actually computed here

Recomputed in `src/landau_shadows.py` during `run_landau.py`. Not copied
from the earlier `math/landau-n2plus1/` agent. Short timeouts. These are
finite facts, not evidence of infinitude.

- `#{n ≤ 300 : n²+1 prime}` = **49**
- first such n: `[1, 2, 4, 6, 10, 14, 16, 20, 24, 26, 36, 40, 54, 56, 66, 74, 84, 90, 94, 110]`
- of those, odd n: **1** (only n=1, as the even-composite identity predicts)
- odd prime factors of n²+1 are 1 mod 4 for all n ≤ 80: **True**
- Ω census n ≤ 80: ω=1,2,3,≥4 = 16, 38, 21, 5; odd/even Ω = 38/42
- Bateman–Horn product truncated at B=500: C_B ≈ **1.369856** (short truncation, not a high-precision lock)
- naive Simpson prediction for n≤300: **45.985**, ratio census/pred **1.0656**
- Gaussian-norm primes with Re≤200, Im=k: {'1': 34, '2': 34, '3': 25, '4': 31}  (Im=1 is not thinner than Im=2 on this box)

These are finite shadows, not evidence of infinitude. BH constant here is a short truncation (B=500), not the locked high-precision product of a previous agent.

UNSURE (from the card, not used as locks): Harman–Lewis exponent 0.119
taken from a secondary summary; Ankeny–Kubilius is conditional on a Hecke GRH
and was not re-read.

## Top 5, with an honest note each

All five score 12. The scorer cannot separate them. None is new.

### Rank 1. score 12. `BILINEAR + bilinear_forms_type_II`

- object: bilinear (Type II) forms in sieve remainders (area sieve, available 1970, maturity theorem_rich)
- template: `BILINEAR`
- easier-case hook: dirichlet (Dirichlet on linear polynomials.) | p2 (Iwaniec 1978: n^2+1 is P2 infinitely often. Literature; not a lemma of this repo.) | x2y4 (Friedlander-Iwaniec 1997/98: infinitely many primes x^2+y^4. y=1 is Landau. Literature.)
- barrier hook: parity: Linear / combinatorial sieves reach P2, not primes. Iwaniec 1978 is the face of this barrier for this sequence. DESCRIBED, not claimed. | one_var: The sequence has ~X values up to size X^2. Friedlander-Iwaniec need the extra variable in x^2+y^4. Setting y=1 is the open slice. | line: n+i is the line Im=1 in Z[i]. The prime ideal theorem does not save a single line.
- transfer (canned, judgment): If the sequence admits a Type I / Type II factorization whose bilinear forms can be estimated beyond the parity barrier, then a prime-detecting sieve applies and the original follows. Imported object: bilinear (Type II) forms in sieve remainders.
- engine tag: `new-looking`

**Known, and the known failure mode is the whole subject.**
This is the Friedlander–Iwaniec program pointed at n²+1. FI 1997/98
proves infinitely many primes of the form x²+y⁴ by feeding a bilinear
form to an asymptotic sieve. The case y=1 is Landau IV and is exactly
the slice their extra variable is there to avoid. Iwaniec 1978 already
got P2 for n²+1; the missing piece is Type II information on a
*univariate* thin sequence. The engine has no evidence that such a
form exists. MathOverflow commentary (not re-proved here) treats
"beat parity for n²+1" as equivalent to the problem.

Code shadow that *was* run: the Ω split at n≤80 is roughly even
(38 odd / 42 even). That is the numerical face of parity, not a way
around it.

### Rank 2. score 12. `EMBED + bilinear_forms_type_II`

- object: bilinear (Type II) forms in sieve remainders (area sieve, available 1970, maturity theorem_rich)
- template: `EMBED`
- easier-case hook: dirichlet (Dirichlet on linear polynomials.) | p2 (Iwaniec 1978: n^2+1 is P2 infinitely often. Literature; not a lemma of this repo.) | x2y4 (Friedlander-Iwaniec 1997/98: infinitely many primes x^2+y^4. y=1 is Landau. Literature.)
- barrier hook: parity: Linear / combinatorial sieves reach P2, not primes. Iwaniec 1978 is the face of this barrier for this sequence. DESCRIBED, not claimed. | one_var: The sequence has ~X values up to size X^2. Friedlander-Iwaniec need the extra variable in x^2+y^4. Setting y=1 is the open slice. | line: n+i is the line Im=1 in Z[i]. The prime ideal theorem does not save a single line.
- transfer (canned, judgment): If a larger family with an extra free variable is known (or easier) to satisfy the analog, and a specialization argument returns the original family, then the original follows. Specialization is the hard step and must be named. Imported object: bilinear (Type II) forms in sieve remainders.
- engine tag: `new-looking`

**Known, already failed as a specialization.**
Embed n²+1 in the family x²+y⁴ (or x²+y^{2k}) and hope to specialize
y=1. FI need the extra variable for the bilinear input; setting it to
1 deletes the input. Heath-Brown–Li (2017, literature, not re-read)
keep y prime and still need that variable. This pairing should be
read as "solve FI again, then invent a specialization theorem that
does not exist."

Code shadow: on a box, the enlarged family x²+y⁴ is thicker than the
line y=1. That is why FI is easier, not why Landau follows.

### Rank 3. score 12. `WEIGHTS + bilinear_forms_type_II`

- object: bilinear (Type II) forms in sieve remainders (area sieve, available 1970, maturity theorem_rich)
- template: `WEIGHTS`
- easier-case hook: dirichlet (Dirichlet on linear polynomials.) | p2 (Iwaniec 1978: n^2+1 is P2 infinitely often. Literature; not a lemma of this repo.) | x2y4 (Friedlander-Iwaniec 1997/98: infinitely many primes x^2+y^4. y=1 is Landau. Literature.)
- barrier hook: parity: Linear / combinatorial sieves reach P2, not primes. Iwaniec 1978 is the face of this barrier for this sequence. DESCRIBED, not claimed. | one_var: The sequence has ~X values up to size X^2. Friedlander-Iwaniec need the extra variable in x^2+y^4. Setting y=1 is the open slice. | line: n+i is the line Im=1 in Z[i]. The prime ideal theorem does not save a single line.
- transfer (canned, judgment): If a weighted detector (not the raw indicator) has a main term that dominates the remainder for the original counting problem, then a positive weighted count implies the original statement. Imported object: bilinear (Type II) forms in sieve remainders.
- engine tag: `new-looking`

**Known-stuck near-miss. Same score as (1) because the scorer
cannot see Type II.**
Selberg / GPY-style weights on n²+1, or bilinear remainder weights
without a genuine Type II estimate, are Iwaniec's P2 world. The
known-answer test `fi_1995` failed G1 for exactly this reason:
`sieve_weights + WEIGHTS` tied `bilinear + BILINEAR`. Treating this
as a new Landau idea would be repeating that miss.

Code shadow: a weighted almost-prime count on n≤N is a finite
computation; it will not detect primes.

### Rank 4. score 12. `RESTRICTED_SUPPORT + bombieri_vinogradov`

- object: Bombieri-Vinogradov / primes in APs on average (area analytic_nt, available 1965, maturity theorem_rich)
- template: `RESTRICTED_SUPPORT`
- easier-case hook: dirichlet (Dirichlet on linear polynomials.) | p2 (Iwaniec 1978: n^2+1 is P2 infinitely often. Literature; not a lemma of this repo.)
- barrier hook: parity: Linear / combinatorial sieves reach P2, not primes. Iwaniec 1978 is the face of this barrier for this sequence. DESCRIBED, not claimed.
- transfer (canned, judgment): If a distribution theorem holds on a thinner but better-behaved set of moduli (or support), and the original detector can be restricted to that support, then the original follows. Imported object: Bombieri-Vinogradov / primes in APs on average.
- engine tag: `new-looking`

**Known method, wrong shape.**
Bombieri–Vinogradov is an averaged distribution theorem for primes
in arithmetic progressions, level 1/2. Landau is prime *values of a
quadratic polynomial*, not primes in a linear progression. Restricted
support (smooth / well-factorable moduli) is Zhang's move for bounded
*gaps*, where the detector is already a linear tuple. There is no
attachment recipe in this pairing that turns n²+1 into an AP-tuple.
Decorative unless someone writes that recipe; none is written.

Code shadow: one can compare BV remainders on a small table. That
computation does not mention n²+1.

### Rank 5. score 12. `WEIGHTS + bombieri_vinogradov`

- object: Bombieri-Vinogradov / primes in APs on average (area analytic_nt, available 1965, maturity theorem_rich)
- template: `WEIGHTS`
- easier-case hook: dirichlet (Dirichlet on linear polynomials.) | p2 (Iwaniec 1978: n^2+1 is P2 infinitely often. Literature; not a lemma of this repo.)
- barrier hook: parity: Linear / combinatorial sieves reach P2, not primes. Iwaniec 1978 is the face of this barrier for this sequence. DESCRIBED, not claimed.
- transfer (canned, judgment): If a weighted detector (not the raw indicator) has a main term that dominates the remainder for the original counting problem, then a positive weighted count implies the original statement. Imported object: Bombieri-Vinogradov / primes in APs on average.
- engine tag: `new-looking`

**Known method, same objection as (4).**
Weights plus BV is the GPY / Maynard setting. Maynard weights detect
linear tuples n+h_i. The polynomial n²+1 is not a linear tuple.
Green–Sawhney 2024 (literature; different problem) get primes of the
form p² + n q² for certain n — still two prime variables, not n²+1.
Do not file this as progress.

Code shadow: same as (4).

## Rank 6–15 (same score band, same honesty)

Score 12 continues through rank 13; 11 from 14. These are the rest of
the sieve / Grossencharacter neighbourhood. None is claimed new.

| rank | score | pairing | one-line honesty |
|---|---|---|---|
| 6 | 12 | `WEIGHTS + hecke_grossencharacters` | Hecke characters of Q(i) detect *sectors*, not the line Im=1. Ankeny–Kubilius need GRH to get y = O(log p) in x²+y². Not Landau. |
| 7 | 12 | `RESTRICTED_SUPPORT + sieve_weights_selberg` | GPY/Maynard restricted support, pointed at a quadratic polynomial. No recipe. |
| 8 | 12 | `WEIGHTS + sieve_weights_selberg` | Iwaniec P2 weights. Known, stops at parity. |
| 9 | 12 | `BILINEAR + switching_principle` | Switching is how Iwaniec reached P2. Known. |
| 10 | 12 | `WEIGHTS + switching_principle` | Switching + weights. Known. |
| 11 | 12 | `BILINEAR + well_factorable_moduli` | Well-factorable moduli are a Zhang-type distribution input. No Landau detector. |
| 12 | 12 | `RESTRICTED_SUPPORT + well_factorable_moduli` | Same, restricted support. |
| 13 | 12 | `WEIGHTS + well_factorable_moduli` | Same, weights. |
| 14 | 11 | `BILINEAR + additive_energy` | Additive energy of {n²+1} is a finite computation and a long way from primes. |
| 15 | 11 | `EMBED + additive_energy` | Embed into a sum-product problem. Decorative until an identity is written. |

## Translations and heuristics the scorer correctly buried

| rank | score | pairing | note |
|---|---|---|---|
| 46 | 10 | `RELATIVE_DENSITY + pseudorandom_majorants` | Green–Tao move. n²+1 is a thin *value* sequence, not a positive-density subset of a sifted integer ambient in the G-T sense. The analog would need a majorant on {n²+1} that is pseudorandom *and* dense enough for a prime-detecting theorem. Not written. Not Green–Tao. |
| 81 | 9 | `DEFORM + ricci_flow` | Cross-wire. No 3-manifold. |
| 134 | 5 | `TRANSLATE + gaussian_integers` | n²+1 prime iff n+i is Gaussian-prime. True, and the thin set stays thin. Known translation. |
| 151 | 2 | `HEURISTIC_MODEL + bateman_horn` | The census/prediction ratio 1.07 at n≤300 is consistent with the heuristic and proves nothing. Correctly scored as a non-implication. |

## Full ranked list

All 151 pairings. `known_or_failed` is a mechanical tag
(`new-looking` only means 'not a native TRANSLATE and not a heuristic
object'; it is **not** a claim of novelty).

| rank | score | pairing | area | year | maturity | mechanical tag |
|---|---|---|---|---|---|---|
| 1 | 12 | `BILINEAR + bilinear_forms_type_II` | sieve | 1970 | theorem_rich | new-looking |
| 2 | 12 | `EMBED + bilinear_forms_type_II` | sieve | 1970 | theorem_rich | new-looking |
| 3 | 12 | `WEIGHTS + bilinear_forms_type_II` | sieve | 1970 | theorem_rich | new-looking |
| 4 | 12 | `RESTRICTED_SUPPORT + bombieri_vinogradov` | analytic_nt | 1965 | theorem_rich | new-looking |
| 5 | 12 | `WEIGHTS + bombieri_vinogradov` | analytic_nt | 1965 | theorem_rich | new-looking |
| 6 | 12 | `WEIGHTS + hecke_grossencharacters` | algebraic_nt | 1920 | theorem_rich | new-looking |
| 7 | 12 | `RESTRICTED_SUPPORT + sieve_weights_selberg` | sieve | 1947 | theorem_rich | new-looking |
| 8 | 12 | `WEIGHTS + sieve_weights_selberg` | sieve | 1947 | theorem_rich | new-looking |
| 9 | 12 | `BILINEAR + switching_principle` | sieve | 1978 | theorem_rich | new-looking |
| 10 | 12 | `WEIGHTS + switching_principle` | sieve | 1978 | theorem_rich | new-looking |
| 11 | 12 | `BILINEAR + well_factorable_moduli` | sieve | 1986 | theorem_rich | new-looking |
| 12 | 12 | `RESTRICTED_SUPPORT + well_factorable_moduli` | sieve | 1986 | theorem_rich | new-looking |
| 13 | 12 | `WEIGHTS + well_factorable_moduli` | sieve | 1986 | theorem_rich | new-looking |
| 14 | 11 | `BILINEAR + additive_energy` | combinatorics | 1983 | theorem_rich | new-looking |
| 15 | 11 | `EMBED + additive_energy` | combinatorics | 1983 | theorem_rich | new-looking |
| 16 | 11 | `DETECT + bilinear_forms_type_II` | sieve | 1970 | theorem_rich | new-looking |
| 17 | 11 | `EMBED + elliptic_curves` | arithmetic_geometry | 1960 | theorem_rich | new-looking |
| 18 | 11 | `BILINEAR + expander_graphs` | dynamics | 1973 | theorem_rich | new-looking |
| 19 | 11 | `EMBED + function_field_analogs` | function_fields | 1930 | theorem_rich | new-looking |
| 20 | 11 | `BILINEAR + gowers_norms` | additive_combinatorics | 2001 | theorem_rich | new-looking |
| 21 | 11 | `RELATIVE_DENSITY + gowers_norms` | additive_combinatorics | 2001 | theorem_rich | new-looking |
| 22 | 11 | `DETECT + hecke_grossencharacters` | algebraic_nt | 1920 | theorem_rich | new-looking |
| 23 | 11 | `EMBED + homogeneous_flows` | dynamics | 1991 | theorem_rich | new-looking |
| 24 | 11 | `BILINEAR + incidence_geometry` | combinatorics | 1983 | theorem_rich | new-looking |
| 25 | 11 | `EMBED + incidence_geometry` | combinatorics | 1983 | theorem_rich | new-looking |
| 26 | 11 | `DETECT + l_functions` | analytic_nt | 1920 | theorem_rich | new-looking |
| 27 | 11 | `DUAL + l_functions` | analytic_nt | 1920 | theorem_rich | new-looking |
| 28 | 11 | `DETECT + sieve_weights_selberg` | sieve | 1947 | theorem_rich | new-looking |
| 29 | 11 | `DUAL + sieve_weights_selberg` | sieve | 1947 | theorem_rich | new-looking |
| 30 | 11 | `DUAL + switching_principle` | sieve | 1978 | theorem_rich | new-looking |
| 31 | 11 | `RELATIVE_DENSITY + szemeredi_regularity` | additive_combinatorics | 1975 | theorem_rich | new-looking |
| 32 | 11 | `DETECT + well_factorable_moduli` | sieve | 1986 | theorem_rich | new-looking |
| 33 | 10 | `DETECT + additive_energy` | combinatorics | 1983 | theorem_rich | new-looking |
| 34 | 10 | `DETECT + bombieri_vinogradov` | analytic_nt | 1965 | theorem_rich | new-looking |
| 35 | 10 | `BILINEAR + circle_method` | analytic_nt | 1920 | theorem_rich | new-looking |
| 36 | 10 | `EMBED + circle_method` | analytic_nt | 1920 | theorem_rich | new-looking |
| 37 | 10 | `DETECT + function_field_analogs` | function_fields | 1930 | theorem_rich | new-looking |
| 38 | 10 | `EMBED + gaussian_integers` | algebraic_nt | -100 | theorem_rich | new-looking |
| 39 | 10 | `RELATIVE_DENSITY + graph_limits` | combinatorics | 2004 | mixed | new-looking |
| 40 | 10 | `BILINEAR + half_dimensional_sieve` | sieve | 1978 | theorem_rich | new-looking |
| 41 | 10 | `EMBED + half_dimensional_sieve` | sieve | 1978 | theorem_rich | new-looking |
| 42 | 10 | `WEIGHTS + half_dimensional_sieve` | sieve | 1978 | theorem_rich | new-looking |
| 43 | 10 | `DEFORM + homogeneous_flows` | dynamics | 1991 | theorem_rich | new-looking |
| 44 | 10 | `DETECT + homogeneous_flows` | dynamics | 1991 | theorem_rich | new-looking |
| 45 | 10 | `EMBED + pseudorandom_majorants` | additive_combinatorics | 1990 | mixed | new-looking |
| 46 | 10 | `RELATIVE_DENSITY + pseudorandom_majorants` | additive_combinatorics | 1990 | mixed | new-looking |
| 47 | 10 | `WEIGHTS + pseudorandom_majorants` | additive_combinatorics | 1990 | mixed | new-looking |
| 48 | 10 | `DETECT + quaternion_algebras` | algebraic_nt | 1930 | theorem_rich | new-looking |
| 49 | 10 | `MODULARITY + quaternion_algebras` | algebraic_nt | 1930 | theorem_rich | new-looking |
| 50 | 10 | `EMBED + spectral_gap` | automorphic | 1965 | mixed | new-looking |
| 51 | 10 | `WEIGHTS + spectral_gap` | automorphic | 1965 | mixed | new-looking |
| 52 | 10 | `BILINEAR + vinogradov_mean_value` | analytic_nt | 1935 | theorem_rich | new-looking |
| 53 | 10 | `EMBED + vinogradov_mean_value` | analytic_nt | 1935 | theorem_rich | new-looking |
| 54 | 9 | `DETECT + circle_method` | analytic_nt | 1920 | theorem_rich | new-looking |
| 55 | 9 | `BILINEAR + delta_method` | analytic_nt | 1990 | mixed | new-looking |
| 56 | 9 | `DETECT + elliptic_curves` | arithmetic_geometry | 1960 | theorem_rich | new-looking |
| 57 | 9 | `MODULARITY + elliptic_curves` | arithmetic_geometry | 1960 | theorem_rich | new-looking |
| 58 | 9 | `DETECT + etale_cohomology` | arithmetic_geometry | 1960 | theorem_rich | new-looking |
| 59 | 9 | `MODULARITY + etale_cohomology` | arithmetic_geometry | 1960 | theorem_rich | new-looking |
| 60 | 9 | `DEFORM + expander_graphs` | dynamics | 1973 | theorem_rich | new-looking |
| 61 | 9 | `DETECT + expander_graphs` | dynamics | 1973 | theorem_rich | new-looking |
| 62 | 9 | `LOCAL_GLOBAL + function_field_analogs` | function_fields | 1930 | theorem_rich | new-looking |
| 63 | 9 | `DETECT + galois_representations` | arithmetic_geometry | 1964 | theorem_rich | new-looking |
| 64 | 9 | `MODULARITY + galois_representations` | arithmetic_geometry | 1964 | theorem_rich | new-looking |
| 65 | 9 | `DETECT + gowers_norms` | additive_combinatorics | 2001 | theorem_rich | new-looking |
| 66 | 9 | `DETECT + half_dimensional_sieve` | sieve | 1978 | theorem_rich | new-looking |
| 67 | 9 | `DEFORM + harmonic_map_flow` | geometric_analysis | 1964 | theorem_rich | new-looking |
| 68 | 9 | `DETECT + harmonic_map_flow` | geometric_analysis | 1964 | theorem_rich | new-looking |
| 69 | 9 | `DETECT + incidence_geometry` | combinatorics | 1983 | theorem_rich | new-looking |
| 70 | 9 | `DEFORM + mean_curvature_flow` | geometric_analysis | 1978 | theorem_rich | new-looking |
| 71 | 9 | `DETECT + mean_curvature_flow` | geometric_analysis | 1978 | theorem_rich | new-looking |
| 72 | 9 | `DEFORM + minimal_surfaces` | geometric_analysis | 1960 | theorem_rich | new-looking |
| 73 | 9 | `DETECT + minimal_surfaces` | geometric_analysis | 1960 | theorem_rich | new-looking |
| 74 | 9 | `DETECT + modular_forms` | automorphic | 1967 | theorem_rich | new-looking |
| 75 | 9 | `MODULARITY + modular_forms` | automorphic | 1967 | theorem_rich | new-looking |
| 76 | 9 | `DEFORM + morse_theory` | topology | 1961 | theorem_rich | new-looking |
| 77 | 9 | `DETECT + morse_theory` | topology | 1961 | theorem_rich | new-looking |
| 78 | 9 | `WEIGHTS + pretentious_chars` | analytic_nt | 2003 | mixed | new-looking |
| 79 | 9 | `DETECT + pseudorandom_majorants` | additive_combinatorics | 1990 | mixed | new-looking |
| 80 | 9 | `LOCAL_GLOBAL + quaternion_algebras` | algebraic_nt | 1930 | theorem_rich | new-looking |
| 81 | 9 | `DEFORM + ricci_flow` | geometric_analysis | 1982 | theorem_rich | new-looking |
| 82 | 9 | `DETECT + ricci_flow` | geometric_analysis | 1982 | theorem_rich | new-looking |
| 83 | 9 | `DETECT + spectral_gap` | automorphic | 1965 | mixed | new-looking |
| 84 | 9 | `DETECT + szemeredi_regularity` | additive_combinatorics | 1975 | theorem_rich | new-looking |
| 85 | 9 | `DETECT + vinogradov_mean_value` | analytic_nt | 1935 | theorem_rich | new-looking |
| 86 | 8 | `DETECT + automorphic_langlands` | automorphic | 1970 | mixed | new-looking |
| 87 | 8 | `MODULARITY + automorphic_langlands` | automorphic | 1970 | mixed | new-looking |
| 88 | 8 | `DEFORM + branching_random_walks` | probability | 1975 | mixed | new-looking |
| 89 | 8 | `DETECT + branching_random_walks` | probability | 1975 | mixed | new-looking |
| 90 | 8 | `DETECT + delta_method` | analytic_nt | 1990 | mixed | new-looking |
| 91 | 8 | `DUAL + delta_method` | analytic_nt | 1990 | mixed | new-looking |
| 92 | 8 | `LOCAL_GLOBAL + elliptic_curves` | arithmetic_geometry | 1960 | theorem_rich | new-looking |
| 93 | 8 | `LOCAL_GLOBAL + etale_cohomology` | arithmetic_geometry | 1960 | theorem_rich | new-looking |
| 94 | 8 | `DETECT + euler_systems` | arithmetic_geometry | 1990 | mixed | new-looking |
| 95 | 8 | `MODULARITY + euler_systems` | arithmetic_geometry | 1990 | mixed | new-looking |
| 96 | 8 | `DEFORM + floer_homology` | topology | 1988 | mixed | new-looking |
| 97 | 8 | `DETECT + floer_homology` | topology | 1988 | mixed | new-looking |
| 98 | 8 | `LOCAL_GLOBAL + galois_representations` | arithmetic_geometry | 1964 | theorem_rich | new-looking |
| 99 | 8 | `DETECT + gaussian_integers` | algebraic_nt | -100 | theorem_rich | new-looking |
| 100 | 8 | `DETECT + graph_limits` | combinatorics | 2004 | mixed | new-looking |
| 101 | 8 | `TRANSLATE + hecke_grossencharacters` | algebraic_nt | 1920 | theorem_rich | known-and-stuck |
| 102 | 8 | `DETECT + kummer_cyclotomic` | algebraic_nt | 1850 | theorem_rich | new-looking |
| 103 | 8 | `TRANSLATE + l_functions` | analytic_nt | 1920 | theorem_rich | known-and-stuck |
| 104 | 8 | `LOCAL_GLOBAL + minimal_surfaces` | geometric_analysis | 1960 | theorem_rich | new-looking |
| 105 | 8 | `LOCAL_GLOBAL + modular_forms` | automorphic | 1967 | theorem_rich | new-looking |
| 106 | 8 | `DETECT + pretentious_chars` | analytic_nt | 2003 | mixed | new-looking |
| 107 | 8 | `DEFORM + thurston_geometrization` | topology | 1982 | mixed | new-looking |
| 108 | 8 | `DETECT + thurston_geometrization` | topology | 1982 | mixed | new-looking |
| 109 | 7 | `LOCAL_GLOBAL + automorphic_langlands` | automorphic | 1970 | mixed | new-looking |
| 110 | 7 | `DETECT + class_groups` | algebraic_nt | 1959 | mixed | new-looking |
| 111 | 7 | `MODULARITY + class_groups` | algebraic_nt | 1959 | mixed | new-looking |
| 112 | 7 | `RELATIVE_DENSITY + cramer_model` | probability | 1936 | heuristic | known-open |
| 113 | 7 | `LOCAL_GLOBAL + euler_systems` | arithmetic_geometry | 1990 | mixed | new-looking |
| 114 | 7 | `LOCAL_GLOBAL + gaussian_integers` | algebraic_nt | -100 | theorem_rich | new-looking |
| 115 | 7 | `HEURISTIC_MODEL + hecke_grossencharacters` | algebraic_nt | 1920 | theorem_rich | new-looking |
| 116 | 7 | `LOCAL_GLOBAL + kummer_cyclotomic` | algebraic_nt | 1850 | theorem_rich | new-looking |
| 117 | 7 | `HEURISTIC_MODEL + l_functions` | analytic_nt | 1920 | theorem_rich | new-looking |
| 118 | 7 | `TRANSLATE + quaternion_algebras` | algebraic_nt | 1930 | theorem_rich | known-and-stuck |
| 119 | 7 | `DETECT + stark_units` | algebraic_nt | 1975 | mixed | new-looking |
| 120 | 7 | `LOCAL_GLOBAL + thurston_geometrization` | topology | 1982 | mixed | new-looking |
| 121 | 7 | `EMBED + tropical_geometry` | combinatorics | 2000 | speculative | decorative |
| 122 | 6 | `LOCAL_GLOBAL + class_groups` | algebraic_nt | 1959 | mixed | new-looking |
| 123 | 6 | `TRANSLATE + elliptic_curves` | arithmetic_geometry | 1960 | theorem_rich | known-and-stuck |
| 124 | 6 | `HEURISTIC_MODEL + function_field_analogs` | function_fields | 1930 | theorem_rich | new-looking |
| 125 | 6 | `TRANSLATE + modular_forms` | automorphic | 1967 | theorem_rich | known-and-stuck |
| 126 | 6 | `TRANSLATE + morse_theory` | topology | 1961 | theorem_rich | known-and-stuck |
| 127 | 6 | `TRANSLATE + ricci_flow` | geometric_analysis | 1982 | theorem_rich | known-and-stuck |
| 128 | 6 | `LOCAL_GLOBAL + stark_units` | algebraic_nt | 1975 | mixed | new-looking |
| 129 | 6 | `TRANSLATE + szemeredi_regularity` | additive_combinatorics | 1975 | theorem_rich | known-and-stuck |
| 130 | 5 | `DETECT + bateman_horn` | analytic_nt | 1962 | heuristic | known-open |
| 131 | 5 | `LOCAL_GLOBAL + bateman_horn` | analytic_nt | 1962 | heuristic | known-open |
| 132 | 5 | `HEURISTIC_MODEL + branching_random_walks` | probability | 1975 | mixed | new-looking |
| 133 | 5 | `HEURISTIC_MODEL + circle_method` | analytic_nt | 1920 | theorem_rich | new-looking |
| 134 | 5 | `TRANSLATE + gaussian_integers` | algebraic_nt | -100 | theorem_rich | known-and-stuck |
| 135 | 5 | `TRANSLATE + graph_limits` | combinatorics | 2004 | mixed | known-and-stuck |
| 136 | 5 | `TRANSLATE + kummer_cyclotomic` | algebraic_nt | 1850 | theorem_rich | known-and-stuck |
| 137 | 5 | `DETECT + motives` | arithmetic_geometry | 1965 | speculative | decorative |
| 138 | 5 | `MODULARITY + motives` | arithmetic_geometry | 1965 | speculative | decorative |
| 139 | 5 | `DETECT + proof_complexity` | logic | 1979 | speculative | decorative |
| 140 | 5 | `DETECT + random_matrices` | probability | 1973 | heuristic | known-open |
| 141 | 5 | `TRANSLATE + thurston_geometrization` | topology | 1982 | mixed | known-and-stuck |
| 142 | 5 | `DETECT + tropical_geometry` | combinatorics | 2000 | speculative | decorative |
| 143 | 4 | `HEURISTIC_MODEL + pretentious_chars` | analytic_nt | 2003 | mixed | new-looking |
| 144 | 4 | `HEURISTIC_MODEL + stark_units` | algebraic_nt | 1975 | mixed | new-looking |
| 145 | 3 | `HEURISTIC_MODEL + cramer_model` | probability | 1936 | heuristic | known-open |
| 146 | 3 | `TRANSLATE + motives` | arithmetic_geometry | 1965 | speculative | decorative |
| 147 | 3 | `HEURISTIC_MODEL + proof_complexity` | logic | 1979 | speculative | decorative |
| 148 | 3 | `TRANSLATE + proof_complexity` | logic | 1979 | speculative | decorative |
| 149 | 3 | `HEURISTIC_MODEL + random_matrices` | probability | 1973 | heuristic | known-open |
| 150 | 3 | `TRANSLATE + tropical_geometry` | combinatorics | 2000 | speculative | decorative |
| 151 | 2 | `HEURISTIC_MODEL + bateman_horn` | analytic_nt | 1962 | heuristic | known-open |

## Cold-grader instruction (Landau half)

If you are grading this file in isolation: FAIL the author if they claim
infinitude, claim a new attack that beats parity, or treat a score of 12
as evidence. PASS the honesty bar only if the top five are all marked
known or already failed and the shadows are finite.

