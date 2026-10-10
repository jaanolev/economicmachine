# Known-answer tests

Jaan's rule, applied before the Landau scores were used: **no score is used
as a certificate until it ranks a known-good reframe high, a known-bad
reframe low, and survives an adversarial review for hindsight leakage.**

The frozen suite is in `src/run_known_answers.py`. Gold labels live only in
`src/gold.py`. The scorer does not import that file.

**Suite verdict: FAIL.**

```
S1 all G1 (gold strictly above every known-bad):  FAIL  (fi_1995 tie 12-12)
S2 at least 3/5 G2 (best gold in top 5 or top 15%): PASS  (5/5)
S3 all G3 (some known-bad at or below median): FAIL  (greentao_2003: bads 9 and 11, median 8)
S4 no winner-bonus strings / no gold import in scorer: PASS
PASS: false
```

Gold pairings were *found* by the mechanical generator on every official
card, and the best gold ranked in the top band every time. That is the
part that worked. The part that did not: the scorer cannot punish a
near-miss that shares the winner's tags.

## Protocol (frozen before the first scores)

For each official card:

1. Hide the gold labels from the scorer.
2. Generate every legal `(object, template)` with `year_available <= cutoff`.
3. Score them with `src/scorer.py`.
4. A generated candidate is gold if its pair sits in `gold.py`.
5. Known-bads are scored the same way (no special case).

Gates:

- **G1.** `best gold score > best known-bad score` (strict).
- **G2.** `best gold rank <= max(5, ceil(0.15 * n_generated))`.
- **G3.** at least one known-bad score `<=` median generated score.

Diagnostic card `poincare_1995` is reported and is **not** in S1–S3.

## The five official cards

Dates were checked against secondary sources (Wiles 1995 introduction,
Ribet Notices note, Hamilton 1982 / 1995, Green–Tao arXiv 2004,
Friedlander–Iwaniec 1997/98, GPY 2005, Zhang/Maynard 2013). Anything
not re-read from the original paper is marked UNSURE.

### 1. `flt_1985` — Fermat, Frey announced, Ribet not proved

**Cutoff:** 1985. **Statement:** no nonzero integer solutions of
\(a^n+b^n=c^n\) for \(n>2\).

**Available (not leaked from 1995):** Kummer regular primes; Faltings 1983
finiteness; Hellegouarch attached \(y^2=x(x-a^n)(x+b^n)\) without a
modularity link (UNSURE of the exact first year; secondary sources say
late 1960s); Frey, Oberwolfach 1985, that the curve should not be modular;
Serre epsilon being formulated (letter to Mestre, August 1985); Taniyama–
Shimura–Weil open (Weil 1967). Ribet's proof of epsilon is July 1986 and
is **out**.

**Honesty:** this is not a 1637 card. The question-change is already being
proposed. The test is whether a 1985 card ranks that already-proposed
reframe above Kummer restatements.

**Gold:** `{elliptic_curves, modular_forms, galois_representations}` ×
`{MODULARITY, LOCAL_GLOBAL}`.

**Known-bads:** Kummer `TRANSLATE`; class groups `TRANSLATE`.

| gate | result |
|---|---|
| n generated | 120 |
| best gold | rank **1**, score 12 (`elliptic_curves + MODULARITY`) |
| known-bads | 6 and 7 |
| G1 / G2 / G3 | PASS / PASS / PASS |

Ranks 1–3 are exactly the three MODULARITY golds. Rank 4 is
`class_groups + MODULARITY` (not gold, not a known-bad). That is a
near-miss the scorer likes, and it is historically closer to the stuck
descent than to Wiles.

### 2. `poincare_1981` — Poincaré, Ricci flow does not exist

**Cutoff:** 1981. **Statement:** every closed simply-connected 3-manifold
is homeomorphic to \(S^3\).

**Available:** Smale 1961; Eells–Sampson 1964 harmonic map heat flow;
mean curvature flow exists as a tool (Huisken 1984 is *after* the cutoff —
the catalog dates MCF at 1978, which may be early; UNSURE). Hamilton 1982
is **out**. Thurston geometrization is being formulated around 1977–82
(UNSURE how much is public as a precise conjecture in 1981).

**Honesty:** the user's slogan is "Poincaré → Ricci flow". Ricci flow
cannot appear on a 1981 card without leakage. The honest ancestor is a
geometric heat flow. Perelman's entropy (2002) is out even on the 1995
diagnostic card.

**Gold:** `{harmonic_map_flow, mean_curvature_flow, minimal_surfaces}` ×
`{DEFORM}`.

**Known-bads:** Morse `TRANSLATE`; Morse `DEFORM`.

| gate | first run | after native-penalty iteration |
|---|---|---|
| n generated | 107 | 107 |
| best gold | rank 1, score 12 | rank 1, score 12 |
| Morse DEFORM | **12 (tie, G1 fail)** | 10 (G1 pass) |
| G1 / G2 / G3 | FAIL / PASS / PASS | **PASS / PASS / PASS** |

The first-run tie is why circularity was extended from
`native+TRANSLATE` to every native pairing. That is the only scorer
change after seeing numbers. It is disclosed here so a cold grader can
call it cherry-picking if they want.

### 3. `greentao_2003` — long APs of primes, pre-Green–Tao

**Cutoff:** 2003. **Statement:** the primes contain APs of arbitrary finite
length.

**Available:** Szemerédi 1975; van der Corput 1939 (length 3); Gowers 2001
uniformity norms. Goldston–Yıldırım truncated divisor sums are in
circulation around 2003 (UNSURE of the exact preprint a 2003 reader
would cite). Green–Tao arXiv is April 2004 and is **out**.

**Honesty:** this is the cleanest of the five. The objects exist; the
reframe is the pairing.

**Gold:** `{pseudorandom_majorants, gowers_norms, szemeredi_regularity}` ×
`{RELATIVE_DENSITY}`.

**Known-bads:** Szemerédi `TRANSLATE` (apply it to a density-zero set);
circle method `DETECT` (the stuck traditional path for long APs).

| gate | result |
|---|---|
| n generated | 148 |
| best gold | rank **2**, score 13 (`gowers_norms + RELATIVE_DENSITY`) |
| rank 1 | `gowers_norms + BILINEAR` (score 13, not gold) |
| known-bads | TRANSLATE 9, circle DETECT 11 |
| median | 8 |
| G1 / G2 / G3 | PASS / PASS / **FAIL** |

G3 fails because both known-bads sit above the median. The circle-method
bad scores 11: it really did solve the length-3 easier case, and the
scorer has no "this method already stalled at the next length" feature.
Szemerédi `RELATIVE_DENSITY` (gold, rank 3, score 13) correctly beats
Szemerédi `TRANSLATE` (bad, score 9). That pair is the one part of G1
that is a real discrimination, not a tag pile-up.

### 4. `fi_1995` — primes \(x^2+y^4\), pre-Friedlander–Iwaniec

**Cutoff:** 1995. **Statement:** infinitely many primes of the form
\(x^2+y^4\).

**Available:** Dirichlet; primes \(x^2+y^2\); Iwaniec 1978 \(P_2\) for
\(n^2+1\) (described, not re-proved); parity barrier; asymptotic sieve /
bilinear-form language of Bombieri–Friedlander–Iwaniec already exists as
a method looking for an input. The 1997/98 theorem is **out**.

**Honesty:** the extra variable \(y\) is already in the problem. The
reframe is to treat it as Type II information.

**Gold:** `{bilinear_forms_type_II, switching_principle}` ×
`{BILINEAR, EMBED}`.

**Known-bads:** Selberg weights `WEIGHTS` (parity, and the sequence is
thinner than \(n^2+1\)); Gaussian integers `TRANSLATE`.

| gate | result |
|---|---|
| n generated | 139 |
| best gold | rank **1**, score 12 (`bilinear_forms_type_II + BILINEAR`) |
| Selberg WEIGHTS | **12 (tie)** |
| Gaussian TRANSLATE | 5 |
| G1 / G2 / G3 | **FAIL** / PASS / PASS |

This is the scorer's real miss. "Put weights on the sequence" and "extract
a bilinear form that beats parity" share the tags `parity_barrier`,
`thin_sequence`, `almost_primes`. The cheap scorer cannot see the missing
Type II input. I did **not** add a Type-II-only bonus after seeing this.
Doing so would be fitting the answer.

### 5. `boundedgaps_2012` — GPY known, Zhang/Maynard not

**Cutoff:** 2012. **Statement:** \(\liminf(p_{n+1}-p_n)\) is finite.

**Available:** GPY 2005 (EH \(\Rightarrow\) bounded gaps; also
\(\liminf (p_{n+1}-p_n)/\log p_n = 0\)); Bombieri–Vinogradov 1965, level
\(1/2\); distribution on well-factorable moduli (Bombieri–Friedlander–
Iwaniec / Fouvry–Iwaniec, 1980s). Zhang 2013 and Maynard 2013 are **out**.

**Honesty:** the community question is already "improve GPY". This tests
ranking, not inventing GPY. Gold is (i) better weights, (ii) a bit more
than BV on restricted moduli.

**Gold:** `{sieve_weights_selberg, well_factorable_moduli, bombieri_vinogradov}`
× `{WEIGHTS, RESTRICTED_SUPPORT}`.

**Known-bads:** Selberg `TRANSLATE`; L-functions `HEURISTIC_MODEL`.

| gate | first run | after native-penalty iteration |
|---|---|---|
| n generated | 151 | 151 |
| best gold rank | 5 | **11** |
| known-bads | 6 and 4 | 6 and 4 |
| G1 / G2 / G3 | PASS / PASS / PASS | PASS / PASS / PASS |

G2 still passes because the top-band cutoff is 23. The native-object
penalty hurt the *winning* language: Maynard is a refinement of native
Selberg weights. That is a second recorded defect. The top of this card
is now generic bilinear-sieve pairings, not GPY weights.

### Diagnostic: `poincare_1995` (not in the suite)

Hamilton's program is already the community question. Gold
`ricci_flow + DEFORM` ranks 2, G1/G2 pass. This card is too easy and
was kept only to show that "Perelman → Ricci flow" is Hamilton's
reframe, not Perelman's. Perelman solved the reframed question
(entropy, reduced volume, surgery).

## Leakage and cherry-picking (author self-review)

A cold grader should treat this list as a confession, not a defense.

**What would be leakage, and what we did.**

- Scoring bonuses for the strings Wiles / Perelman / Taniyama / Frey /
  Zhang / Maynard: **linted absent** from `scorer.py`, `generator.py`,
  `catalog.py`.
- `scorer.py` importing `gold.py` or branching on `flt_1985` etc.:
  **absent** (AST check).
- Putting Ricci flow on the 1981 card: **not done**. Gold is heat flow.
- Putting Ribet 1986 on the 1985 card: **not done**.
- Putting Green–Tao 2004 on the 2003 card: **not done**.
- Catalog containing only the five winning objects: **not done** (46
  objects, many decorative).
- Tuning tags after seeing scores so that gold wins: **one** change,
  the native-object penalty, disclosed above. FI tags were not touched
  after the 12–12 tie.
- Choosing known-bads that the scorer already crushes (motives on
  Poincaré, tropical geometry on FLT): we used historically real stuck
  paths instead. That made G1/G3 harder, and they failed.

**What is still leaky, even after that.**

- The catalog *does* contain Ricci flow, modular forms, Gowers norms,
  bilinear Type II forms, well-factorable moduli, Selberg weights. A
  1981 Poincaré generator can still emit "Ricci flow" only after 1982;
  a 1637 FLT generator cannot emit modular forms (year 1967). The
  library is the modern working mathematician's toolbox, not a 1900
  toolbox. That is selection bias.
- Easier-case tags were written by someone who knows the endings.
  `eh_implies_bounded_gaps` exists as a tag because GPY exists. The
  tag is dated 2005 and is legal on the 2012 card; it would be leakage
  on a 2004 card.
- Official cards are exactly the five the user named. That is
  cherry-picking of *problems*, requested by the brief. A fairer
  battery would include a breakthrough the engine should *miss*
  (something that was not a reframe, or a reframe the catalog lacks).
- Implication points are canned. Every attack template gets +2
  judgment. That inflates every non-translation.

## Can the score be used?

**No, not as a certificate.** It can be used as a sorter that:

- puts modularity-of-curves at the top of a 1985 FLT card,
- puts heat-flow deformations at the top of a 1981 Poincaré card,
- puts relative density / Gowers at the top of a 2003 AP-of-primes card,
- puts bilinear forms at the top of a 1995 \(x^2+y^4\) card *and also
  puts Selberg weights there*,
- puts many sieve refinements near the top of a 2012 bounded-gap card,
  with GPY-like pairings nearby but no longer first.

That is enough to *generate* Landau questions and not enough to *believe*
the top five. The Landau file says so on every line.
