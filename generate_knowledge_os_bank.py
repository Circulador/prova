#!/usr/bin/env python3
"""Generate data/knowledge-os-bank.js — Velora Knowledge OS v3 (knowledge-node oriented)."""
from __future__ import annotations

import json
import pathlib
import sys
from datetime import datetime, timezone

ROOT = pathlib.Path(__file__).parent
sys.path.insert(0, str(ROOT))

from knowledge_os.content_engine import build_all_nodes, build_certifications  # noqa: E402

TAXONOMY_PATH = ROOT / "data" / "knowledge-os-taxonomy.json"
OUT = ROOT / "data" / "knowledge-os-bank.js"


def main():
    taxonomy = json.loads(TAXONOMY_PATH.read_text(encoding="utf-8"))
    nodes_map = build_all_nodes(questions_per_node=5)
    certifications, stats = build_certifications(taxonomy, nodes_map, target_questions=500)

    knowledge_nodes = list(nodes_map.values())
    bank = {
        "version": "3.0.0",
        "schemaVersion": "3.0.0",
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "title": "Velora Privacy & Security Knowledge OS",
        "uncertaintyPolicy": taxonomy.get("uncertaintyPolicy"),
        "sources": taxonomy.get("sources"),
        "tracks": taxonomy.get("tracks"),
        "knowledgeDomains": taxonomy.get("knowledgeDomains"),
        "nistPrivacyFramework": taxonomy.get("nistPrivacyFramework"),
        "knowledgeNodes": knowledge_nodes,
        "certifications": certifications,
        "stats": stats,
    }

    js = "/* Velora Knowledge OS v3 — generated; do not edit by hand. */\n"
    js += "/* Regenerate: python generate_knowledge_os_bank.py */\n"
    js += "const KNOWLEDGE_OS_BANK = "
    js += json.dumps(bank, ensure_ascii=False, indent=2)
    js += ";\n"
    js += "// Legacy alias removed intentionally — use KNOWLEDGE_OS_BANK only.\n"

    OUT.write_text(js, encoding="utf-8")
    size_kb = OUT.stat().st_size / 1024
    print(f"Wrote {OUT} ({size_kb:.1f} KB)")
    print(f"Knowledge nodes: {len(knowledge_nodes)}")
    print(f"Certifications: {len(certifications)}")
    print(f"Total question slots: {stats['totalQuestions']}")
    for code, n in sorted(stats["byCert"].items()):
        print(f"  {code}: {n}")


if __name__ == "__main__":
    main()
