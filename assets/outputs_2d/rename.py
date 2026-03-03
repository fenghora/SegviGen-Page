import os
from pathlib import Path

# ========= 你只需要改这里 =========
ROOT = Path(r"/media/nfs/tmp_data/fenghr/SegviGen-Page/assets/outputs_2d")  # 例如 r"D:\data\cases" 或 "/home/xxx/data"
# =================================

VIDEO_EXTS = {".mp4", ".mov", ".avi", ".mkv", ".webm", ".m4v"}

def find_single(folder: Path, exts: set) -> Path | None:
    files = [p for p in folder.iterdir() if p.is_file() and p.suffix.lower() in exts]
    if len(files) == 0:
        return None
    if len(files) > 1:
        print(f"[SKIP] {folder} has multiple candidates for {exts}: {[f.name for f in files]}")
        return None
    return files[0]

def safe_rename(src: Path, dst: Path) -> None:
    if src == dst:
        return

    # 避免覆盖：若 dst 已存在则追加 _1, _2...
    if dst.exists():
        stem, suffix = dst.stem, dst.suffix
        k = 1
        while True:
            cand = dst.parent / f"{stem}_{k}{suffix}"
            if not cand.exists():
                dst = cand
                break
            k += 1

    src.rename(dst)
    print(f"[OK ] {src} -> {dst}")

def main():
    root = ROOT.expanduser().resolve()
    if not root.exists() or not root.is_dir():
        raise RuntimeError(f"ROOT not found or not a directory: {root}")

    subfolders = [p for p in root.iterdir() if p.is_dir()]
    if not subfolders:
        print(f"[INFO] No subfolders under: {root}")
        return

    for sub in subfolders:
        glb = find_single(sub, {".glb"})
        if glb is None:
            print(f"[SKIP] {sub}: missing/ambiguous .glb")
            continue

        base = glb.stem

        png = find_single(sub, {".png"})
        vid = find_single(sub, VIDEO_EXTS)

        if png is None:
            print(f"[WARN] {sub}: no .png")
        else:
            safe_rename(png, sub / f"{base}{png.suffix.lower()}")

        if vid is None:
            print(f"[WARN] {sub}: no video (supported: {sorted(VIDEO_EXTS)})")
        else:
            safe_rename(vid, sub / f"{base}{vid.suffix.lower()}")

if __name__ == "__main__":
    main()