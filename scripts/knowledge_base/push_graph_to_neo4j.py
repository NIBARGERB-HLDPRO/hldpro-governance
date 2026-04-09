#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import networkx as nx
from networkx.readwrite import json_graph

from graphify.export import push_to_neo4j


def build_scoped_graph(graph_path: Path, scope: str) -> nx.DiGraph:
    raw = json.loads(graph_path.read_text())
    source_graph = json_graph.node_link_graph(raw, edges="links")
    scoped_graph = nx.DiGraph()
    node_id_map: dict[str, str] = {}

    for node_id, attrs in source_graph.nodes(data=True):
        scoped_id = f"{scope}:{node_id}"
        node_id_map[str(node_id)] = scoped_id
        scoped_attrs = dict(attrs)
        scoped_attrs["graph_scope"] = scope
        scoped_attrs["source_graph_file"] = str(graph_path)
        scoped_graph.add_node(scoped_id, **scoped_attrs)

    for src, tgt, attrs in source_graph.edges(data=True):
        scoped_attrs = dict(attrs)
        scoped_attrs["graph_scope"] = scope
        scoped_graph.add_edge(node_id_map[str(src)], node_id_map[str(tgt)], **scoped_attrs)

    return scoped_graph


def main() -> int:
    parser = argparse.ArgumentParser(description="Push a governance-hosted graph.json into local Neo4j.")
    parser.add_argument("--graph", required=True, help="Path to governance-hosted graph.json")
    parser.add_argument("--scope", required=True, help="Namespace prefix used to isolate node ids")
    parser.add_argument("--uri", default="bolt://localhost:7687", help="Neo4j Bolt URI")
    parser.add_argument("--user", default="neo4j", help="Neo4j username")
    parser.add_argument("--password", default="governance-dev-password", help="Neo4j password")
    args = parser.parse_args()

    graph_path = Path(args.graph)
    if not graph_path.exists():
      print(f"ERROR: graph file not found: {graph_path}", file=sys.stderr)
      return 1

    scoped_graph = build_scoped_graph(graph_path, args.scope)
    result = push_to_neo4j(scoped_graph, args.uri, args.user, args.password)
    print(json.dumps({"scope": args.scope, "graph": str(graph_path), **result}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
