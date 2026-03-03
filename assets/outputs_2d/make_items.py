# -*- coding: utf-8 -*-
import os
import json

# ===================== 写死参数（最直白写法） =====================
# 脚本所在目录：.../SegviGen-Page/assets/outputs_2d
SCRIPT_DIR = "/media/nfs/tmp_data/fenghr/SegviGen-Page/assets/outputs_2d"

# 你的输入目录：就是脚本所在目录（里面有很多子文件夹）
INPUT_DIR = SCRIPT_DIR

# 原始 glb 目录：.../SegviGen-Page/assets/origanl_mesh
SOURCE_GLB_DIR = "/media/nfs/tmp_data/fenghr/SegviGen-Page/assets/origanl_mesh"

# 输出 js：写到 INPUT_DIR 同目录
OUTPUT_JS = os.path.join(INPUT_DIR, "tmp.js")
# ===============================================================

IMG_EXTS = [".png", ".jpg", ".jpeg", ".webp"]
VID_EXTS = [".mp4", ".webm", ".mov", ".m4v"]


def to_posix_relpath(abs_path, project_root):
    """转成相对 project_root 的路径，并把 \\ 变成 / 适配网页"""
    rel = os.path.relpath(abs_path, project_root)
    return rel.replace("\\", "/")


def find_file_same_stem(folder, stem, exts):
    """优先找同名 stem 文件；找不到则如果该类文件只有一个就用它"""
    # 先按 stem 精确匹配
    for ext in exts:
        p = os.path.join(folder, stem + ext)
        if os.path.isfile(p):
            return p

    # 再扫描同 stem
    for name in os.listdir(folder):
        p = os.path.join(folder, name)
        if os.path.isfile(p):
            base, ext = os.path.splitext(name)
            if base == stem and ext.lower() in exts:
                return p

    # 兜底：如果这一类文件在 folder 里只有一个
    cand = []
    for name in os.listdir(folder):
        p = os.path.join(folder, name)
        if os.path.isfile(p):
            _, ext = os.path.splitext(name)
            if ext.lower() in exts:
                cand.append(p)
    if len(cand) == 1:
        return cand[0]

    return None


def main():
    if not os.path.isdir(INPUT_DIR):
        raise FileNotFoundError("INPUT_DIR 不存在: " + INPUT_DIR)
    if not os.path.isdir(SOURCE_GLB_DIR):
        raise FileNotFoundError("SOURCE_GLB_DIR 不存在: " + SOURCE_GLB_DIR)

    # project_root 取 SegviGen-Page（也就是 SCRIPT_DIR 的上两级）
    # SCRIPT_DIR = .../assets/outputs_2d
    # project_root = .../SegviGen-Page
    project_root = os.path.abspath(os.path.join(SCRIPT_DIR, "..", ".."))

    items = []
    problems = []

    # 遍历 INPUT_DIR 下所有 .glb（递归）
    for root, _, files in os.walk(INPUT_DIR):
        for fname in files:
            if not fname.lower().endswith(".glb"):
                continue

            seg_glb = os.path.join(root, fname)
            stem, _ = os.path.splitext(fname)

            img = find_file_same_stem(root, stem, IMG_EXTS)
            vid = find_file_same_stem(root, stem, VID_EXTS)
            src_glb = os.path.join(SOURCE_GLB_DIR, fname)

            if img is None:
                problems.append("[缺图像] " + seg_glb)
                continue
            if vid is None:
                problems.append("[缺视频] " + seg_glb)
                continue
            if not os.path.isfile(src_glb):
                problems.append("[缺原始GLB] " + src_glb + " （对应分割GLB: " + seg_glb + "）")
                continue

            items.append({
                "prompt": to_posix_relpath(os.path.abspath(img), project_root),
                "video": to_posix_relpath(os.path.abspath(vid), project_root),
                "source_model": to_posix_relpath(os.path.abspath(src_glb), project_root),
                "segmented_model": to_posix_relpath(os.path.abspath(seg_glb), project_root),
            })

    # 稳定排序
    items.sort(key=lambda d: d["segmented_model"])

    if problems:
        print("发现以下问题（已跳过这些条目）：")
        for p in problems:
            print(" - " + p)

    if not items:
        raise RuntimeError("没有生成任何条目：请检查目录结构/文件命名。")

    # 写 tmp.js
    lines = []
    lines.append("var full_segmentation_items = [")
    for it in items:
        lines.append("  {")
        lines.append("    prompt: " + json.dumps(it["prompt"], ensure_ascii=False) + ",")
        lines.append("    video: " + json.dumps(it["video"], ensure_ascii=False) + ",")
        lines.append("    source_model: " + json.dumps(it["source_model"], ensure_ascii=False) + ",")
        lines.append("    segmented_model: " + json.dumps(it["segmented_model"], ensure_ascii=False) + ",")
        lines.append("  },")
    lines.append("];")
    lines.append("")

    with open(OUTPUT_JS, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print("✅ 已生成 %d 条，写入: %s" % (len(items), OUTPUT_JS))


if __name__ == "__main__":
    main()