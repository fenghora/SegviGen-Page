import os
import re
import shutil
import subprocess
from pathlib import Path

# =========================
# 你只需要改这里
# =========================
ROOT_DIR = "/media/nfs/tmp_data/fenghr/SegviGen-Page"     # 项目根目录
JS_FILE  = "/media/nfs/tmp_data/fenghr/SegviGen-Page/assets/interactive_seg_results/interactive_segmentation_items.js"            # 你的 js 文件路径（或改成你实际文件名）
KEEP_BAK = False                                            # True: 备份原视频为 .bak
DRY_RUN  = False                                            # True: 只打印不执行转换

# ffmpeg 编码参数：浏览器通吃（H.264 + yuv420p + faststart），音频可选
FFMPEG_ARGS = [
    "-map", "0:v:0",
    "-map", "0:a?",                # 有音频就带上，没有就忽略
    "-c:v", "libx264",
    "-pix_fmt", "yuv420p",
    "-profile:v", "high",
    "-level", "4.1",
    "-movflags", "+faststart",
    "-c:a", "aac",
    "-b:a", "128k",
    "-ac", "2",
    # 防止奇数宽高导致 yuv420p 报错：强制缩到偶数尺寸（基本不影响视觉）
    "-vf", "scale=trunc(iw/2)*2:trunc(ih/2)*2",
]


def run(cmd: list[str]) -> None:
    subprocess.run(cmd, check=True)


def ensure_ffmpeg() -> None:
    if shutil.which("ffmpeg") is None:
        raise RuntimeError(
            "找不到 ffmpeg。请先安装：\n"
            "  conda install -c conda-forge ffmpeg\n"
            "或 ubuntu: sudo apt-get install -y ffmpeg"
        )


def extract_mp4_paths_from_js(js_path: str) -> list[str]:
    text = Path(js_path).read_text(encoding="utf-8")
    # 抽取 video: "xxx.mp4"
    paths = re.findall(r'video\s*:\s*"([^"]+\.mp4)"', text)
    # 去重、保持顺序
    seen = set()
    uniq = []
    for p in paths:
        if p not in seen:
            seen.add(p)
            uniq.append(p)
    return uniq


def convert_one(in_path: str) -> None:
    """
    in_path: 绝对路径
    覆盖原文件（可选备份 .bak）
    """
    in_path = os.path.abspath(in_path)
    if not os.path.isfile(in_path):
        print(f"[Missing] {in_path}")
        return

    tmp_out = in_path + ".tmp.mp4"
    bak_out = in_path + ".bak"

    cmd = ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", in_path] + FFMPEG_ARGS + [tmp_out]

    if DRY_RUN:
        print("[DRY_RUN]", " ".join(cmd))
        return

    try:
        run(cmd)
    except subprocess.CalledProcessError as e:
        # 转换失败就删掉临时文件
        if os.path.exists(tmp_out):
            os.remove(tmp_out)
        print(f"[FFMPEG FAILED] {in_path} -> {e}")
        return

    # 成功：备份/替换
    if KEEP_BAK:
        # 只备份一次（避免重复覆盖旧备份）
        if not os.path.exists(bak_out):
            os.replace(in_path, bak_out)
        else:
            os.remove(in_path)
    else:
        os.remove(in_path)

    os.replace(tmp_out, in_path)
    print(f"[OK] {in_path}")


def main():
    ensure_ffmpeg()

    if not os.path.isfile(JS_FILE):
        raise FileNotFoundError(f"JS 文件不存在：{JS_FILE}")

    rel_videos = extract_mp4_paths_from_js(JS_FILE)
    if not rel_videos:
        print("[WARN] JS 里没找到 video: \"...mp4\"")
        return

    print(f"[INFO] Found {len(rel_videos)} videos in JS.")

    for rel in rel_videos:
        abs_path = os.path.join(ROOT_DIR, rel)
        if not os.path.isfile(abs_path):
            print(f"[Missing video] {abs_path}")
            continue
        convert_one(abs_path)


if __name__ == "__main__":
    main()