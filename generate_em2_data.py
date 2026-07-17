#!/usr/bin/env python3
"""Agrega em2_data/*.py em em2_bank_data.json."""
import importlib.util, json, pathlib, sys

ROOT = pathlib.Path(__file__).parent
DATA_DIR = ROOT / "em2_data"
OUT = ROOT / "em2_bank_data.json"

VARS = ["PORT", "MAT", "HIST", "GEO", "FIS", "QUI", "BIO", "ING", "FIL", "SOC"]

def load_module(path):
    spec = importlib.util.spec_from_file_location(path.stem, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

def main():
    subjects = []
    for var in VARS:
        found = None
        for py in sorted(DATA_DIR.glob("*.py")):
            mod = load_module(py)
            if hasattr(mod, var):
                found = getattr(mod, var)
                break
        if not found:
            sys.exit(f"Subject variable {var} not found in em2_data/")
        total = sum(len(v) for v in found["submaterias"].values())
        if total != 50:
            sys.exit(f"{found['materia']}: expected 50 questions, got {total}")
        subjects.append(found)
        print(f"  {found['code']} {found['materia']}: {total} questões")
    OUT.write_text(json.dumps(subjects, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nWrote {OUT.name}: {len(subjects)} matérias, {len(subjects)*50} questões total")

if __name__ == "__main__":
    main()
