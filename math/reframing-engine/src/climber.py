"""Orchestrate cheap sketches, merge, expensive checks, recalibration."""

from __future__ import annotations

from typing import Any

from cards import CARDS
from climb_check import recalibrate_library, run_checks
from climb_moves import sketch
from climb_seeds import reframe_to_node, seed_boundedgaps_2012, seed_landau_2026
from generator import generate
from library import Library, Node, make_node
from scorer import score_pair
from catalog import by_id
from templates import TEMPLATES


def seed_for(card_id: str) -> Library:
    if card_id == "boundedgaps_2012":
        return seed_boundedgaps_2012()
    if card_id == "landau_2026":
        return seed_landau_2026()
    raise KeyError(card_id)


def add_generator_starts(lib: Library, card_id: str, min_score: int = 10, limit: int = 20) -> int:
    card = CARDS[card_id]
    rows = []
    for cand in generate(card):
        obj = by_id()[cand.object_id]
        sc = score_pair(card, obj, TEMPLATES[cand.template_id])
        rows.append((sc.total, cand))
    rows.sort(key=lambda kv: (-kv[0], kv[1].id))
    added = 0
    for score, cand in rows:
        if score < min_score:
            continue
        if added >= limit:
            break
        claim, conf = reframe_to_node(card_id, cand.object_id, cand.template_id, score)
        node = make_node(
            claim,
            kind="start",
            confidence=conf,
            year_available=min(cand.year_available, lib.year_cutoff),
            source=f"reframe:{cand.object_id}:{cand.template_id}",
            card_id=card_id,
            status="sketched",
        )
        lib.add_node(node)
        added += 1
    return added


def enumerate_paths(lib: Library, max_len: int = 5) -> list[list[str]]:
    """All simple paths of length >= 1 edge, from seeds/starts toward sinks."""
    roots = [
        n.id
        for n in lib.nodes.values()
        if n.kind in {"seed", "start", "target"} or not lib.incoming(n.id)
    ]
    paths: list[list[str]] = []

    def walk(cur: list[str]) -> None:
        outs = lib.outgoing(cur[-1])
        if not outs:
            if len(cur) >= 2:
                paths.append(cur)
            return
        grew = False
        for e in outs:
            if e.dst in cur:
                continue
            if len(cur) >= max_len:
                continue
            grew = True
            walk(cur + [e.dst])
        if not grew and len(cur) >= 2:
            paths.append(cur)

    for r in roots:
        walk([r])
    # Dedup
    seen = set()
    uniq = []
    for p in paths:
        t = tuple(p)
        if t not in seen:
            seen.add(t)
            uniq.append(p)
    return uniq


def path_score(lib: Library, ids: list[str]) -> float:
    if len(ids) < 2:
        return 0.0
    acc = 1.0
    for a, b in zip(ids, ids[1:]):
        edges = [e for e in lib.outgoing(a) if e.dst == b]
        if not edges:
            return 0.0
        acc *= max(e.confidence for e in edges)
    acc *= lib.nodes[ids[-1]].confidence
    return acc


def path_record(lib: Library, ids: list[str]) -> dict[str, Any]:
    nodes = [lib.nodes[i] for i in ids]
    moves = []
    for a, b in zip(ids, ids[1:]):
        edges = [e for e in lib.outgoing(a) if e.dst == b]
        if edges:
            e = max(edges, key=lambda x: x.confidence)
            moves.append(e.move)
    return {
        "node_ids": ids,
        "statements": [n.claim.statement() for n in nodes],
        "moves": moves,
        "end_pred": nodes[-1].claim.pred,
        "end_status": nodes[-1].status,
        "end_conditional": nodes[-1].claim.conditional,
        "score": path_score(lib, ids),
        "end_confidence": nodes[-1].confidence,
    }


def climb(card_id: str, max_depth: int = 3, max_new_nodes: int = 80, check_k: int = 8, min_reframe_score: int = 10) -> dict[str, Any]:
    lib = seed_for(card_id)
    n_seed = len(lib.nodes)
    n_starts = add_generator_starts(lib, card_id, min_score=min_reframe_score)
    n_new = sketch(lib, card_id, max_depth=max_depth, max_new_nodes=max_new_nodes)
    checks = run_checks(lib, year_cutoff=lib.year_cutoff, k=check_k)
    recalibrate_library(lib)
    paths = [path_record(lib, p) for p in enumerate_paths(lib)]
    paths.sort(key=lambda r: (-r["score"], r["node_ids"][0]))
    return {
        "card_id": card_id,
        "year_cutoff": lib.year_cutoff,
        "n_seed": n_seed,
        "n_reframe_starts": n_starts,
        "n_sketched_new": n_new,
        "n_nodes": len(lib.nodes),
        "n_edges": len(lib.edges),
        "n_merges": len(lib.merge_log),
        "checks": checks,
        "top_paths": paths[:15],
        "n_paths": len(paths),
        "library": lib,
    }
