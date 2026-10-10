"""Persistent climb library: nodes + edges, merge on equiv_key.

This is a DAG. The brief says 'tree library'; joining partial climbs
from different routes makes a DAG. Schema version 1.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any


SCHEMA_VERSION = 1


@dataclass
class Claim:
    pred: str
    weight_family: str = "na"
    moduli: str = "na"
    level_demand: str = "na"
    level_have: str = "na"
    extra_var: str = "na"
    conditional: bool = False
    barrier: str = "na"
    family: str = "na"

    def equiv_key(self) -> str:
        return json.dumps(asdict(self), sort_keys=True, separators=(",", ":"))

    def node_id(self) -> str:
        return hashlib.sha1(self.equiv_key().encode("utf-8")).hexdigest()[:12]

    def statement(self) -> str:
        bits = [self.pred]
        if self.weight_family != "na":
            bits.append(f"weights={self.weight_family}")
        if self.moduli != "na":
            bits.append(f"moduli={self.moduli}")
        if self.level_demand != "na":
            bits.append(f"demand={self.level_demand}")
        if self.level_have != "na":
            bits.append(f"have={self.level_have}")
        if self.extra_var != "na":
            bits.append(f"extra_var={self.extra_var}")
        if self.conditional:
            bits.append("conditional")
        if self.barrier != "na":
            bits.append(f"barrier={self.barrier}")
        if self.family != "na":
            bits.append(f"family={self.family}")
        return " | ".join(bits)

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> "Claim":
        return cls(**{k: d[k] for k in cls.__dataclass_fields__ if k in d})


@dataclass
class Node:
    id: str
    claim: Claim
    kind: str  # seed | sketch | target | start
    status: str  # seed | sketched | checked_hold | checked_fail | checked_barrier | checked_unknown | checked_translation
    confidence: float
    prior_confidence: float
    year_available: int
    sources: list[str] = field(default_factory=list)
    check_note: str = ""
    card_id: str = ""

    def as_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "claim": self.claim.as_dict(),
            "statement": self.claim.statement(),
            "equiv_key": self.claim.equiv_key(),
            "kind": self.kind,
            "status": self.status,
            "confidence": self.confidence,
            "prior_confidence": self.prior_confidence,
            "year_available": self.year_available,
            "sources": list(self.sources),
            "check_note": self.check_note,
            "card_id": self.card_id,
        }

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> "Node":
        return cls(
            id=d["id"],
            claim=Claim.from_dict(d["claim"]),
            kind=d["kind"],
            status=d["status"],
            confidence=float(d["confidence"]),
            prior_confidence=float(d["prior_confidence"]),
            year_available=int(d["year_available"]),
            sources=list(d.get("sources") or []),
            check_note=d.get("check_note") or "",
            card_id=d.get("card_id") or "",
        )


@dataclass
class Edge:
    id: str
    src: str
    dst: str
    move: str
    confidence: float
    status: str
    reason: str
    sources: list[str] = field(default_factory=list)

    def as_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "src": self.src,
            "dst": self.dst,
            "move": self.move,
            "confidence": self.confidence,
            "status": self.status,
            "reason": self.reason,
            "sources": list(self.sources),
        }

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> "Edge":
        return cls(
            id=d["id"],
            src=d["src"],
            dst=d["dst"],
            move=d["move"],
            confidence=float(d["confidence"]),
            status=d["status"],
            reason=d["reason"],
            sources=list(d.get("sources") or []),
        )


def edge_id(src: str, dst: str, move: str) -> str:
    raw = f"{src}|{move}|{dst}"
    return hashlib.sha1(raw.encode("utf-8")).hexdigest()[:12]


class Library:
    def __init__(self, card_id: str, year_cutoff: int) -> None:
        self.schema_version = SCHEMA_VERSION
        self.card_id = card_id
        self.year_cutoff = year_cutoff
        self.nodes: dict[str, Node] = {}
        self.edges: dict[str, Edge] = {}
        self.merge_log: list[str] = []

    def add_node(self, node: Node) -> Node:
        existing = self.nodes.get(node.id)
        if existing is None:
            self.nodes[node.id] = node
            return node
        # Merge: union sources, keep higher confidence, prefer checked status.
        before = existing.confidence
        new_sources = [s for s in node.sources if s not in existing.sources]
        for s in new_sources:
            existing.sources.append(s)
        if node.confidence > existing.confidence:
            existing.confidence = node.confidence
        rank = _status_rank(node.status) - _status_rank(existing.status)
        if rank > 0:
            existing.status = node.status
            if node.check_note:
                existing.check_note = node.check_note
        if existing.kind == "sketch" and node.kind in {"seed", "target", "start"}:
            existing.kind = node.kind
        if new_sources or before != existing.confidence or rank > 0:
            self.merge_log.append(
                f"merged {node.id} sources+={new_sources} conf {before}->{existing.confidence}"
            )
        return existing

    def add_edge(self, edge: Edge) -> Edge:
        existing = self.edges.get(edge.id)
        if existing is None:
            self.edges[edge.id] = edge
            return edge
        for s in edge.sources:
            if s not in existing.sources:
                existing.sources.append(s)
        if edge.confidence > existing.confidence:
            existing.confidence = edge.confidence
        return existing

    def as_dict(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "card_id": self.card_id,
            "year_cutoff": self.year_cutoff,
            "nodes": [n.as_dict() for n in sorted(self.nodes.values(), key=lambda x: x.id)],
            "edges": [e.as_dict() for e in sorted(self.edges.values(), key=lambda x: x.id)],
            "merge_log": list(self.merge_log),
        }

    def save(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(self.as_dict(), indent=2), encoding="utf-8")

    @classmethod
    def load(cls, path: Path) -> "Library":
        data = json.loads(path.read_text(encoding="utf-8"))
        lib = cls(data["card_id"], int(data["year_cutoff"]))
        lib.schema_version = int(data.get("schema_version", SCHEMA_VERSION))
        for nd in data["nodes"]:
            lib.nodes[nd["id"]] = Node.from_dict(nd)
        for ed in data["edges"]:
            lib.edges[ed["id"]] = Edge.from_dict(ed)
        lib.merge_log = list(data.get("merge_log") or [])
        return lib

    def outgoing(self, node_id: str) -> list[Edge]:
        return [e for e in self.edges.values() if e.src == node_id]

    def incoming(self, node_id: str) -> list[Edge]:
        return [e for e in self.edges.values() if e.dst == node_id]


def _status_rank(status: str) -> int:
    order = {
        "sketched": 0,
        "seed": 1,
        "checked_unknown": 2,
        "checked_translation": 3,
        "checked_hold": 4,
        "checked_fail": 5,
        "checked_barrier": 6,
    }
    return order.get(status, 0)


def make_node(
    claim: Claim,
    kind: str,
    confidence: float,
    year_available: int,
    source: str,
    card_id: str,
    status: str | None = None,
) -> Node:
    return Node(
        id=claim.node_id(),
        claim=claim,
        kind=kind,
        status=status or ("seed" if kind in {"seed", "target"} else "sketched"),
        confidence=confidence,
        prior_confidence=confidence,
        year_available=year_available,
        sources=[source],
        card_id=card_id,
    )
