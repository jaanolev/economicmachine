# Gut-feeling climber

Extension of the reframing engine. Reframings are *starting points*.
The climber sketches routes from known results toward a target as
chains of plausible lemmas, stores every node even when the route dies,
checks only the dangerous nodes, and recalibrates.

It is **not doing real math**. It is eyeballing climbs.

**Known-answer verdict: PASS, with a weak C2.** The library rediscovers
the two 2012-era route *shapes* (enrich the detector; change the moduli
support) from GPY-era seeds. After checks those shapes beat the
parity/heuristic known-bads. They do **not** beat a one-step TRANSLATE
on raw path score. The 2013 theorems are not HOLDs.

**Landau: no progress.** Surviving high paths are translations,
relative-density slogans, or the known enlargement to \(x^2+y^4\).
Every specialize-to-univariate and Type-I prime-detection node was
marked `checked_barrier`.

## 1. Cheap sketcher

No language model is called. `src/climb_moves.py` applies a frozen list
of generic moves. A small model can fill the same schema using
`CHEAP_CLIMBER_PROMPT` in that file.

Moves (names deliberately not later-theorem names):

| move | gut | what it sketches |
|---|---|---|
| ENRICH_DETECTOR | 0.55 | richer weight family, lower distribution demand |
| CHANGE_SUPPORT | 0.50 | same average on well-factorable / smooth moduli |
| COMBINE | 0.28–0.70 | glue a detector to a distribution node |
| ASSUME_OPEN | 0.40 | assume the open hypothesis; mark conditional |
| TYPE_I_ONLY | 0.32 | detect primes from Type I / indicator info |
| HEURISTIC_CLOSE | 0.30 | close by a random model |
| SPECIALIZE | 0.22 | set an extra variable to a constant |
| ENLARGE | 0.48 | add a free variable |
| TRANSLATE | 0.38 | rewrite in a neighbouring language |
| RELATIVE_AMBIENT | 0.34 | thin set as dense in a pseudorandom ambient |

Depth ≤ 3, ≤ 4 moves per node, ≤ 80 new nodes. Compute is a few
milliseconds.

**Hindsight confession.** ENRICH_DETECTOR and CHANGE_SUPPORT *are* the
Zhang/Maynard habits with the names filed off. They sit in the move
list because those are standard sieve reflexes (Selberg already
optimized weights; BFI already used well-factorable moduli), and also
because we know how the story ended. The known-answer test therefore
asks: given GPY-era *seeds*, do those generic moves fire, combine
toward the target, and survive a check that refuses to HOLD the 2013
theorems? It does not ask a 2004 climber to invent the move list.

## 2. Tree library (actually a DAG)

Schema version 1, files under `library/`.

A **node** is a structured claim, not a paragraph:

```
claim: pred, weight_family, moduli, level_demand, level_have,
       extra_var, conditional, barrier, family
id: sha1(canonical JSON of claim)[:12]
```

Equivalent claims merge: sources are unioned, the higher confidence
is kept, a checked status beats a sketch. That is how two failed
routes can still donate a shared lemma to a third route.

An **edge** is a move from `src` to `dst` with a cheap confidence.

Kinds: `seed` (known at cutoff), `start` (from the reframing generator),
`sketch` (eyeballed), `target`.

Statuses: `seed`, `sketched`, `checked_hold`, `checked_fail`,
`checked_barrier`, `checked_unknown`, `checked_translation`.

Seed for the official test (`seed_boundedgaps_2012.json`) contains
only 2012-or-earlier facts: 1-d GPY-style weights, Bombieri–Vinogradov
level 1/2, well-factorable moduli as a *setting* at level 1/2 (not
above), the 2005 implication "open level>1/2 ⇒ bounded gaps", Brun
almost-twins, a raw indicator, a random-model heuristic. It does
**not** contain a richer-detector theorem or a level>1/2-on-smooth
theorem.

Generator pairings with score ≥ 10 become `start` nodes and merge
with those seeds when the claim fields match (85 merges on the 2012
run).

## 3. Expensive check (cheap code, few nodes)

`src/climb_check.py`. No strong model is called. The "expensive" part
is a dated lookup plus one toy Rayleigh quotient.

Always checked (do not spend the slot budget): every sketched node
with `barrier=parity` or `barrier=no_extra_variable`.

Then up to 8 other summit-faking nodes: translations, heuristic
closes, target-shaped claims, relative-density slogans.

Rules (year cutoff is an argument):

- Type I / indicator ⇒ primes: `checked_barrier` (parity).
- Specialize away the extra variable: `checked_barrier`.
- Heuristic close: `checked_fail` (not a deduction).
- Translation: `checked_translation` (true rewrite, thin set stays thin).
- Richer detector / extra level on smooth moduli / target-shaped
  combine of those: `checked_unknown` at cutoff 2012. **Not HOLD.**
- 1965 level 1/2, 2005 implication-with-open-hypothesis, almost-primes:
  HOLD only if they appear as those seed predicates.

Toy shadow, not a HOLD: `(1,1)` beats `(1,)` on a Rayleigh quotient
(`ratio_2d=2 > ratio_1d=1`). This is the gut feeling "more weight
coordinates can help", not a detection theorem.

## 4. Recalibration

```
HOLD            ×1.20 (cap 0.95)
UNKNOWN         ×0.95
TRANSLATION     ×0.70
FAIL            ×0.25
BARRIER         ×0.12
```

Parents of barrier/fail sketches get a further ×0.85. Path score is
the product of edge confidences times the end-node confidence.

## 5. Known-answer test (official: GPY-era → bounded gaps)

Frozen gates, then the numbers from `results/climber_known_answer.json`.

| gate | meaning | result |
|---|---|---|
| C1 | library contains an enrich-detector node *and* a change-support node, and paths that reach a `bounded_gaps` claim of that shape | **PASS** (12 enrich paths, 8 support paths) |
| C2 | best gold-shaped path score > best known-bad path (parity or heuristic) | **PASS** (0.0272 > 0.0198) |
| C3 | no HOLD on richer-detector or extra-level-on-smooth | **PASS** |
| C4 | climber/moves/check/seeds/library do not import `climb_gold` and contain no winner-bonus strings | **PASS** |
| C5 | at least one sketched node off the gold paths is stored | **PASS** (14 extras) |
| suite | all of the above | **PASS** |

Best enrich path actually stored:

```
selberg_1d, demand>1/2
  --ENRICH_DETECTOR--> richer, demand any_positive
  --COMBINE--> bounded_gaps using existing level 1/2
  --TRANSLATE--> a rewrite (noise)
```

That is the 2012 question "do richer weights make Bombieri–Vinogradov
enough?". The expensive check left the target node `checked_unknown`.

Best support path:

```
level 1/2 on all moduli
  --CHANGE_SUPPORT--> hoped extra level on smooth moduli (conditional)
  --COMBINE--> conditional bounded_gaps (here glued to indicator weights, sloppy)
  --TRANSLATE--> a rewrite
```

That is the 2012 question "is there a bit more than 1/2 on a thinner
set of moduli?". Also `checked_unknown`.

**C2 is weak.** One-step TRANSLATE paths score ~0.071, above both gold
shapes. A 2012 reader using this gut ranking would still look at
rewrites first. The test only asked gold to beat *known-bads*, not to
win the library. I did not retune translation priors after seeing that.

Leakage remaining (author review, not a fresh agent this turn):

- The move list is the leaky object. C4 only proves we did not write
  "Zhang" on the score function.
- `family=twins` vs `n2plus1` is a card-family switch in the moves.
- Seed source tags say `gpy_weights`. GPY is pre-cutoff; the string is
  allowed. The 2013 names are banned in the climber modules.
- Gold labels live in `src/climb_gold.py`, imported only by the runner
  and tests.

## 6. Landau run

50 nodes, 116 edges, 250 paths, 16 checks. Generator starts (score ≥ 10)
were merged in.

What the expensive check did:

- Every Type-I or specialize-to-\(n^2+1\) node: `checked_barrier`.
- Translations: `checked_translation`.
- Heuristic close: `checked_fail`.
- No `checked_hold` of unconditional prime values of \(n^2+1\).

Top raw paths after that: RELATIVE_AMBIENT (some still sketched),
TRANSLATE, then routes that ENLARGE to the known \(x^2+y^4\) seed.
Those are the already-failed or already-solved neighbours. They are
not a new attack on Landau IV.

## 7. How to run

```
pip install pytest pytest-cov
PYTHONPATH=math/reframing-engine/src python3 -m pytest math/reframing-engine/src/verify.py math/reframing-engine/src/test_climber.py -q
PYTHONPATH=math/reframing-engine/src python3 math/reframing-engine/src/run_climber.py
```

PowerShell:

```
pip install pytest pytest-cov
$env:PYTHONPATH = "math/reframing-engine/src"
python -m pytest math/reframing-engine/src/verify.py math/reframing-engine/src/test_climber.py -q
python math/reframing-engine/src/run_climber.py
```

`run_climber.py` exits 0 on this machine because the (weak) KA suite
passes. That is not permission to treat Landau paths as mathematics.
