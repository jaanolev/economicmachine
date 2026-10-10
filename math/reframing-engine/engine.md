# Reframing engine

Thesis (Jaan): on the hardest problems the bottleneck is the question. The
historical breakthroughs named in the brief were question-changes:

| later name | old question | new question |
|---|---|---|
| Wiles | no solutions of \(a^n+b^n=c^n\) for \(n>2\) | modularity of (semistable) elliptic curves over \(\mathbb{Q}\) |
| Perelman | every simply-connected closed 3-manifold is \(S^3\) | Ricci flow with surgery, after Hamilton |
| Green–Tao | arbitrarily long APs of primes | a dense subset of a pseudorandom set inherits Szemerédi |
| Friedlander–Iwaniec | primes of the form \(x^2+y^4\) | bilinear / Type II input that beats the parity barrier |
| Zhang / Maynard | bounded gaps between primes | GPY weights, refined either in the weights or in the moduli |

This folder is a **generator plus a cheap scorer**, not a proof engine. It
borrows objects from a frozen catalog and scores pairings without looking up
who won.

**The scorer did not pass its frozen known-answer suite.** Gold pairings
ranked in the top band on all five official cards, but a known-bad Selberg
reframe tied the Friedlander–Iwaniec gold, and both Green–Tao known-bads sat
above the median. See `known_answer_tests.md`. Until that is fixed, treat
every Landau score as a **sorting heuristic**, not a certificate.

Code lives in `src/`. Claims that are numbers or tag-overlaps are locked in
`src/verify.py`. Canned implication text is flagged `judgment`.

## 1. What successful reframings share (checkable, not vibes)

Written before scoring. A pairing is treated as a *candidate reframe* only if
it can be written in the schema below. The shared structure is a list of
yes/no tests.

1. **Transfer sentence.** There is a statement \(T\) in the imported language
   such that "if \(T\) then original". Equivalence both ways with no new
   averaging is a *translation*, not a reframe. Check: `template_id != TRANSLATE`
   or the candidate writes a one-way implication.
2. **Easier-case hook.** At least one *already solved* special case of the
   original becomes a known theorem about the imported object. Check: overlap
   of `object.solves_case_tags` with the card's solved easier-case tags.
3. **Barrier engagement.** The pairing names a listed barrier and uses a
   template that is a *mechanism* for that barrier class (weights, bilinear
   forms, relative density, deformation, extra variable, restricted support,
   modularity), not a rename. Check: overlap of `template.addresses` with
   card barrier tags, and template not in `{TRANSLATE, HEURISTIC_MODEL}`.
4. **Finite shadow.** There is an \(N\) and an observable that would look
   different if the reframe were empty. Check: a code_shadow string that
   names a count/compare/census. Some shadows are actually run in
   `src/landau_shadows.py`.
5. **Non-native language, or a genuine refinement.** Restating the problem
   in its native objects is circular. Check: `object.id` not in
   `card.native_object_ids`, *or* the template is a refinement move
   (`WEIGHTS`, `RESTRICTED_SUPPORT`, `BILINEAR`) — the second clause is
   *not* implemented, and that is why Zhang/Maynard gold dropped after the
   native-object penalty. Flagged as a known scorer defect.
6. **Object maturity.** The imported object already has theorems, not only
   a slogan. Check: `maturity == theorem_rich` (2 pts) or `mixed` (1).
7. **Distant borrow (weak).** The object's area is not next door to the
   problem area. Nearby map is in `src/scorer.py`. This is a bonus, not a
   requirement: Zhang/Maynard stayed inside sieve theory.

These seven are the whole theory. If a pairing fails (1)–(4), it is
decorative or a translation.

## 2. Generator (procedure a cheap model can run)

No language model is required. `src/generator.py` enumerates pairings.

```
read problem card (statement, year_cutoff, barriers, easier cases, native ids)
for object in catalog with object.year_available <= year_cutoff:
    for template in object.templates_ok:
        emit a candidate:
            new_question = template.cheap_prompt applied to object + statement
            transfer     = template.implication_pattern + object.name
            easier_hook  = tag overlap with card.easier_cases (or NONE)
            barrier_hook = tag overlap with card.barriers (or NONE)
            code_shadow  = object.code_shadow + template.code_shadow
```

The cheap-model prompt (also in `src/generator.py`) is for optional polish.
Tests do not call a model. A small model that cannot invent post-cutoff
theorems can still fill the JSON schema from one card, one object, one
template.

Frozen catalog: 47 objects, dated, tagged. Frozen templates: 12 moves
(`DETECT`, `DEFORM`, `RELATIVE_DENSITY`, `WEIGHTS`, `BILINEAR`,
`MODULARITY`, `EMBED`, `DUAL`, `LOCAL_GLOBAL`, `TRANSLATE`,
`HEURISTIC_MODEL`, `RESTRICTED_SUPPORT`).

Do not add an object because a winner used it, and do not delete one
because it dilutes a winner. The catalog is supposed to generate junk.

## 3. Scorer (cheap, mostly code)

`src/scorer.py` never imports `gold.py`, never branches on a card id, and
is linted for winner-bonus strings (`wiles`, `perelman`, `taniyama`, …).

| feature | max | kind | rule |
|---|---|---|---|
| easier_case | +2 | code | tag overlap with a *solved* easier case |
| barrier | +2 | code | template carries a mechanism tag of a listed barrier |
| code_shadow | +2 | code | a finite count/compare is named; heuristic objects get +1 |
| attack_surface | +2 | code | template in the attack list |
| implication | +2 | **judgment** | canned \(T\Rightarrow P\); 0 for heuristics |
| maturity | +2 | code | theorem_rich / mixed / else |
| distant_borrow | +1 | code | object area not in `NEARBY[card.area]` |
| circularity | −2/−1 | code | native object, or attack template on a heuristic object |

Theoretical max is about 13. Typical gold scores were 12–13. Translations
of native objects land around 4–6.

**Iteration 1 (documented, after the first known-answer run):** circularity
originally penalized only `native + TRANSLATE`. Morse+DEFORM then tied the
1981 Poincaré gold at 12. The native-object penalty was extended to every
template. That is a rule about restatement, not a winner-name bonus. Side
effect: Zhang/Maynard gold uses native sieve objects, so those pairings
were also penalized and dropped from rank 5 to rank 11 (still inside the
top 15% band).

## 4. How to run

From the repo root (Linux/macOS):

```
pip install pytest pytest-cov
PYTHONPATH=math/reframing-engine/src python3 -m pytest math/reframing-engine/src/verify.py -q
PYTHONPATH=math/reframing-engine/src python3 math/reframing-engine/src/run_known_answers.py
PYTHONPATH=math/reframing-engine/src python3 math/reframing-engine/src/run_landau.py
```

PowerShell (this VM is Linux; these are the Windows-friendly twins):

```
pip install pytest pytest-cov
$env:PYTHONPATH = "math/reframing-engine/src"
python -m pytest math/reframing-engine/src/verify.py -q
python math/reframing-engine/src/run_known_answers.py
python math/reframing-engine/src/run_landau.py
```

Every loop in `landau_shadows.py` has a deadline. On timeout it raises;
it does not guess a number.

## 5. What this engine will not do

- It will not invent Frey curves, Ricci flow, or GPY from a blank 1637 /
  1904 / 1921 card. Year cutoffs are part of the test.
- It will not prove Landau IV. A high score is tag overlap.
- It will not distinguish "Selberg weights" from "Type II bilinear forms"
  on the 1995 \(x^2+y^4\) card. That is a recorded fail.
- Implication text is a template. Flagged judgment. Not a deduction.
