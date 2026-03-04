#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
from pathlib import Path
from typing import Dict, List, Tuple


# =========================
# Hard-coded paths (as requested)
# =========================
ORIGIN_DIR = Path("/media/nfs/tmp_data/fenghr/SegviGen-Page/assets/interactive_origin_mesh")
SEG_DIR = Path("/media/nfs/tmp_data/fenghr/SegviGen-Page/assets/interactive_seg_results")
OUT_JS = Path("/media/nfs/tmp_data/fenghr/SegviGen-Page/assets/interactive_segmentation_items.js")

# Web-relative prefixes used in generated JS
ORIGIN_PREFIX = "assets/interactive_origin_mesh"
SEG_PREFIX = "assets/interactive_seg_results"


# Filename patterns
RE_ORIGIN = re.compile(r"^segmented_mesh_(\d{8})_(\d{6})_mesh\.glb$")
RE_SEG = re.compile(r"^segmented_mesh_(\d{8})_(\d{6})_merge\.glb$")
RE_MP4 = re.compile(r"^(\d{6})\.mp4$")


def _pick_better(existing: Path, candidate: Path) -> Path:
    """
    Choose a better file when multiple files map to the same id.
    Strategy:
      1) Prefer lexicographically larger basename (usually newer date/time embedded)
      2) If tie, prefer newer mtime
    """
    if existing.name < candidate.name:
        return candidate
    if existing.name > candidate.name:
        return existing
    # Same name: fallback to mtime
    try:
        return candidate if candidate.stat().st_mtime > existing.stat().st_mtime else existing
    except Exception:
        return existing


def _index_origin_meshes(origin_dir: Path) -> Tuple[Dict[str, Path], List[str]]:
    by_id: Dict[str, Path] = {}
    warnings: List[str] = []

    for p in sorted(origin_dir.glob("*.glb")):
        m = RE_ORIGIN.match(p.name)
        if not m:
            continue
        _date, mesh_id = m.group(1), m.group(2)
        if mesh_id in by_id:
            chosen = _pick_better(by_id[mesh_id], p)
            if chosen != by_id[mesh_id]:
                warnings.append(
                    f"[origin] duplicate id={mesh_id}: chose {chosen.name} over {by_id[mesh_id].name}"
                )
                by_id[mesh_id] = chosen
            else:
                warnings.append(
                    f"[origin] duplicate id={mesh_id}: kept {by_id[mesh_id].name}, ignored {p.name}"
                )
        else:
            by_id[mesh_id] = p

    return by_id, warnings


def _index_seg_meshes(seg_dir: Path) -> Tuple[Dict[str, Path], List[str]]:
    by_id: Dict[str, Path] = {}
    warnings: List[str] = []

    for p in sorted(seg_dir.glob("*.glb")):
        m = RE_SEG.match(p.name)
        if not m:
            continue
        _date, mesh_id = m.group(1), m.group(2)
        if mesh_id in by_id:
            chosen = _pick_better(by_id[mesh_id], p)
            if chosen != by_id[mesh_id]:
                warnings.append(
                    f"[seg] duplicate id={mesh_id}: chose {chosen.name} over {by_id[mesh_id].name}"
                )
                by_id[mesh_id] = chosen
            else:
                warnings.append(
                    f"[seg] duplicate id={mesh_id}: kept {by_id[mesh_id].name}, ignored {p.name}"
                )
        else:
            by_id[mesh_id] = p

    return by_id, warnings


def _index_mp4(seg_dir: Path) -> Dict[str, Path]:
    by_id: Dict[str, Path] = {}
    for p in sorted(seg_dir.glob("*.mp4")):
        m = RE_MP4.match(p.name)
        if not m:
            continue
        mesh_id = m.group(1)
        # If duplicates exist, keep lexicographically larger (rare)
        if mesh_id in by_id:
            by_id[mesh_id] = _pick_better(by_id[mesh_id], p)
        else:
            by_id[mesh_id] = p
    return by_id


def _to_js_string(s: str) -> str:
    # Basic JS string escaping for quotes/backslashes
    return s.replace("\\", "\\\\").replace('"', '\\"')


def main() -> None:
    if not ORIGIN_DIR.is_dir():
        raise FileNotFoundError(f"ORIGIN_DIR not found: {ORIGIN_DIR}")
    if not SEG_DIR.is_dir():
        raise FileNotFoundError(f"SEG_DIR not found: {SEG_DIR}")

    origin_map, origin_warnings = _index_origin_meshes(ORIGIN_DIR)
    seg_map, seg_warnings = _index_seg_meshes(SEG_DIR)
    mp4_map = _index_mp4(SEG_DIR)

    all_ids = sorted(set(origin_map.keys()) | set(seg_map.keys()) | set(mp4_map.keys()))
    items: List[Tuple[str, str, str]] = []  # (video_rel, origin_rel, seg_rel)

    missing_origin: List[str] = []
    missing_seg: List[str] = []
    missing_mp4: List[str] = []

    for mesh_id in all_ids:
        o = origin_map.get(mesh_id)
        s = seg_map.get(mesh_id)
        v = mp4_map.get(mesh_id)

        if o is None:
            missing_origin.append(mesh_id)
        if s is None:
            missing_seg.append(mesh_id)
        if v is None:
            missing_mp4.append(mesh_id)

        # Only emit items when all three exist
        if o is None or s is None or v is None:
            continue

        video_rel = f"{SEG_PREFIX}/{v.name}"
        origin_rel = f"{ORIGIN_PREFIX}/{o.name}"
        seg_rel = f"{SEG_PREFIX}/{s.name}"
        items.append((video_rel, origin_rel, seg_rel))

    # Sort by id numerically (still keep leading zeros)
    items.sort(key=lambda x: int(Path(x[0]).stem))

    # Generate JS content
    lines: List[str] = []
    lines.append("var interactive_segmentation_items = [")
    for idx, (video_rel, origin_rel, seg_rel) in enumerate(items):
        comma = "," if idx < len(items) - 1 else ""
        lines.extend([
            "    {",
            f'        video: "{_to_js_string(video_rel)}",',
            f'        source_model: "{_to_js_string(origin_rel)}",',
            f'        segmented_model: "{_to_js_string(seg_rel)}",',
            f"    }}{comma}",
        ])
    lines.append("];")
    lines.append("")  # newline at EOF

    OUT_JS.parent.mkdir(parents=True, exist_ok=True)
    OUT_JS.write_text("\n".join(lines), encoding="utf-8")

    # Console summary
    print(f"[OK] Wrote JS: {OUT_JS}")
    print(f"[OK] Items emitted: {len(items)}")
    if origin_warnings or seg_warnings:
        print("\n[WARN] Duplicates found (kept one per id):")
        for w in origin_warnings + seg_warnings:
            print("  - " + w)

    print("\n[CHECK] Missing counts (by id):")
    print(f"  - missing origin mesh: {len(missing_origin)}")
    print(f"  - missing seg merge glb: {len(missing_seg)}")
    print(f"  - missing mp4: {len(missing_mp4)}")

    # Print a few examples to help debugging
    def _preview(name: str, arr: List[str], k: int = 20) -> None:
        if not arr:
            return
        print(f"\n  {name} (show up to {k}):")
        for x in arr[:k]:
            print("   - " + x)

    _preview("missing origin mesh ids", missing_origin)
    _preview("missing seg glb ids", missing_seg)
    _preview("missing mp4 ids", missing_mp4)


if __name__ == "__main__":
    main()