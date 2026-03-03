#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import os
import re
import shutil
from pathlib import Path
from typing import List, Tuple, Optional


def _extract_items_block(js_text: str, var_name: str) -> str:
    """
    Extract the array block assigned to `var <var_name> = [ ... ]`.
    """
    pattern = rf"\bvar\s+{re.escape(var_name)}\s*=\s*\[(.*?)\]\s*;?"
    m = re.search(pattern, js_text, flags=re.DOTALL)
    return m.group(1) if m else js_text


def _extract_prompt_and_source_model(items_text: str) -> List[Tuple[str, str]]:
    """
    Extract (prompt, source_model) pairs from JS object literals.
    Supports single/double quotes.
    """
    pairs: List[Tuple[str, str]] = []

    for obj_m in re.finditer(r"\{(.*?)\}", items_text, flags=re.DOTALL):
        obj_text = obj_m.group(1)

        prompt_m = re.search(r"\bprompt\b\s*:\s*([\"'])(.*?)\1", obj_text, flags=re.DOTALL)
        source_m = re.search(r"\bsource_model\b\s*:\s*([\"'])(.*?)\1", obj_text, flags=re.DOTALL)

        if not prompt_m or not source_m:
            continue

        prompt_path = prompt_m.group(2).strip()
        source_path = source_m.group(2).strip()
        pairs.append((prompt_path, source_path))

    return pairs


def _is_probably_relative(p: str) -> bool:
    if p.startswith(("http://", "https://")):
        return False
    if os.path.isabs(p):
        return False
    return True


def _ensure_unique_path(dest_dir: Path, filename: str) -> Path:
    """
    If filename exists in dest_dir, append _1/_2/... before suffix.
    """
    base = Path(filename).stem
    suffix = Path(filename).suffix
    candidate = dest_dir / (base + suffix)

    idx = 1
    while candidate.exists():
        candidate = dest_dir / f"{base}_{idx}{suffix}"
        idx += 1

    return candidate


def _resolve_source_path(path_str: str, src_root: Path) -> Optional[Path]:
    """
    Resolve path string to an existing filesystem path.
    - If relative: src_root / path_str
    - If absolute: path_str
    Returns None if it's a URL or can't be resolved.
    """
    if path_str.startswith(("http://", "https://")):
        return None

    p = Path(path_str)
    if _is_probably_relative(path_str):
        p = (src_root / path_str).resolve()
    else:
        p = p.expanduser().resolve()

    return p


def copy_flatten_prompt_and_glb(js_path: Path, dest_dir: Path, var_name: str, src_root: Path) -> None:
    js_text = js_path.read_text(encoding="utf-8", errors="ignore")
    items_text = _extract_items_block(js_text, var_name)
    pairs = _extract_prompt_and_source_model(items_text)

    if not pairs:
        raise RuntimeError(
            f"No (prompt, source_model) pairs found. "
            f"Check var_name='{var_name}' and your JS content."
        )

    dest_dir.mkdir(parents=True, exist_ok=True)

    copied = 0
    skipped_ext = 0
    missing = []
    ignored = []

    allowed_ext = {".png", ".glb"}

    def _copy_one(path_str: str) -> None:
        nonlocal copied, skipped_ext, missing, ignored

        src = _resolve_source_path(path_str, src_root)
        if src is None:
            ignored.append(path_str)
            return

        if not src.exists():
            missing.append(str(src))
            return

        if src.suffix.lower() not in allowed_ext:
            skipped_ext += 1
            return

        dst = _ensure_unique_path(dest_dir, src.name)
        shutil.copy2(src, dst)
        copied += 1

    for prompt_path, source_model_path in pairs:
        _copy_one(prompt_path)
        _copy_one(source_model_path)

    print(f"[OK] Found {len(pairs)} items.")
    print(f"[OK] Copied {copied} files (flattened) into: {dest_dir}")
    if skipped_ext:
        print(f"[INFO] Skipped {skipped_ext} files due to extension filter (only .png/.glb).")

    if missing:
        print(f"[WARN] Missing {len(missing)} files:")
        for p in missing[:50]:
            print("  -", p)
        if len(missing) > 50:
            print(f"  ... and {len(missing) - 50} more")

    if ignored:
        print(f"[INFO] Ignored {len(ignored)} non-local paths (e.g., URLs).")


def main():
    parser = argparse.ArgumentParser(
        description="Flatten-copy .png (prompt) and .glb (source_model) referenced in a JS file into a target folder."
    )
    parser.add_argument("--js", required=True, type=str, help="Path to the JS file.")
    parser.add_argument("--dest", required=True, type=str, help="Destination folder (no subfolders will be created).")
    parser.add_argument(
        "--var",
        default="full_segmentation_items",
        type=str,
        help="JS variable name holding the array (default: full_segmentation_items).",
    )
    parser.add_argument(
        "--src_root",
        default=None,
        type=str,
        help="Source root folder for resolving relative paths like assets/... (default: directory of the JS file).",
    )

    args = parser.parse_args()
    js_path = Path(args.js).expanduser().resolve()
    dest_dir = Path(args.dest).expanduser().resolve()

    if args.src_root is None:
        src_root = js_path.parent
    else:
        src_root = Path(args.src_root).expanduser().resolve()

    if not js_path.exists():
        raise FileNotFoundError(f"JS file not found: {js_path}")

    copy_flatten_prompt_and_glb(js_path=js_path, dest_dir=dest_dir, var_name=args.var, src_root=src_root)


if __name__ == "__main__":
    main()