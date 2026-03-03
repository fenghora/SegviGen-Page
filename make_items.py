import os

# =========================
# 你只需要改这里
# =========================
ROOT_DIR = "/media/nfs/tmp_data/fenghr/SegviGen-Page/"  # 根目录（里面应包含 assets/）
OUTPUT_JS = "tmp.js"
VIDEO_SUFFIX = "_combined.mp4"

# segmented_model 放在这里（分割后的 glb）
SEG_DIR_NAME = "full_segmentation"
# source_model 放在这里（原始 mesh glb）
SOURCE_DIR_NAME = "origanl_mesh"


def to_posix(rel_path: str) -> str:
    return rel_path.replace("\\", "/")


def write_full_segmentation_items(root_dir: str, out_js_name: str = "tmp.js") -> str:
    seg_dir = os.path.join(root_dir, "assets", SEG_DIR_NAME)
    out_js_path = os.path.join(root_dir, out_js_name)

    if not os.path.isdir(seg_dir):
        print(f"[Missing folder] {seg_dir}")
        with open(out_js_path, "w", encoding="utf-8") as f:
            f.write("var full_segmentation_items = [\n];\n")
        return out_js_path

    items = []

    # 遍历 assets/full_segmentation 下所有 *_combined.mp4
    for dirpath, _, filenames in os.walk(seg_dir):
        for fn in filenames:
            if not fn.endswith(VIDEO_SUFFIX):
                continue

            video_abs = os.path.join(dirpath, fn)
            if not os.path.isfile(video_abs):
                print(f"[Missing video] {video_abs}")
                continue

            base = fn[: -len(VIDEO_SUFFIX)]  # 去掉 _combined.mp4

            # segmented_model: 与视频同目录的 <id>.glb（full_segmentation）
            segmented_abs = os.path.join(dirpath, base + ".glb")
            if not os.path.isfile(segmented_abs):
                print(f"[Missing segmented_model] {segmented_abs}")
                continue

            # source_model: 把 full_segmentation 路径替换成 origanl_mesh
            source_abs = segmented_abs.replace(
                os.sep + SEG_DIR_NAME + os.sep,
                os.sep + SOURCE_DIR_NAME + os.sep,
            )
            if source_abs == segmented_abs:
                source_abs = os.path.join(root_dir, "assets", SOURCE_DIR_NAME, base + ".glb")

            if not os.path.isfile(source_abs):
                print(f"[Missing source_model] {source_abs}")
                continue

            # 写入 JS：相对 ROOT_DIR 的路径
            video_rel = to_posix(os.path.relpath(video_abs, root_dir))
            source_rel = to_posix(os.path.relpath(source_abs, root_dir))
            segmented_rel = to_posix(os.path.relpath(segmented_abs, root_dir))

            items.append((base, video_rel, source_rel, segmented_rel))

    items.sort(key=lambda x: x[0])

    with open(out_js_path, "w", encoding="utf-8") as f:
        f.write("var full_segmentation_items =[\n")
        for _, video_rel, source_rel, segmented_rel in items:
            f.write("    {\n")
            f.write(f'        video: "{video_rel}",\n')
            f.write(f'        source_model: "{source_rel}",\n')
            f.write(f'        segmented_model: "{segmented_rel}",\n')
            f.write("    },\n")
        f.write("]\n")

    print(f"[OK] wrote {len(items)} items -> {out_js_path}")
    return out_js_path


if __name__ == "__main__":
    write_full_segmentation_items(ROOT_DIR, OUTPUT_JS)