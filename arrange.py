import os
import json

def generate_items_js(root_folder):
    items = []
    print("-" * 20)
    for subdir, _, files in os.walk(root_folder):
        print("检查目录:", subdir)
        print("包含文件:", files)
    for subdir, _, files in os.walk(root_folder):
        if "comparison.mp4" in files and "prompt.txt" in files and "model.glb" in files and "edit.glb" in files:
            rel_path = os.path.relpath(subdir, root_folder)

            # 读取 prompt.txt 内容
            prompt_file = os.path.join(subdir, "prompt.txt")
            with open(prompt_file, "r", encoding="utf-8") as f:
                prompt_text = f.read().strip()

            item = {
                "video": os.path.join("assets/text_condition_editing", rel_path, "comparison.mp4").replace("\\", "/"),
                "prompt": prompt_text,  # 直接存字符串
                "source_model": os.path.join("assets/text_condition_editing", rel_path, "model.glb").replace("\\", "/"),
                "edited_model": os.path.join("assets/text_condition_editing", rel_path, "edit.glb").replace("\\", "/"),
            }
            items.append(item)
            print(item)
        else:
            print(files)

    js_code = "var items = " + json.dumps(items, indent=4, ensure_ascii=False) + ";"
    return js_code


if __name__ == "__main__":
    root = "/vePFS-MLP/buaa/fenghaoran/workspace/VoxhammerPage/assets/text_condtion_editing"  # 换成你的文件夹路径
    print(root)
    js_string = generate_items_js(root)
    print(js_string)
    # 你也可以保存到文件
    with open("text_condition_editing_items.js", "w", encoding="utf-8") as f:
        f.write(js_string)

# For image condition
# def generate_items_js(root_folder):
#     items = []
#     for subdir, _, files in os.walk(root_folder):
#         if "comparison.mp4" in files and "prompt.png" in files and "model.glb" in files and "edit.glb" in files:
#             rel_path = os.path.relpath(subdir, root_folder)
#             item = {
#                 "video": os.path.join("assets/image_condition_editing", rel_path, "comparison.mp4").replace("\\", "/"),
#                 "prompt": os.path.join("assets/image_condition_editing", rel_path, "prompt.png").replace("\\", "/"),
#                 "source_model": os.path.join("assets/image_condition_editing", rel_path, "model.glb").replace("\\", "/"),
#                 "edited_model": os.path.join("assets/image_condition_editing", rel_path, "edit.glb").replace("\\", "/"),
#             }
#             items.append(item)

#     js_code = "var items = " + json.dumps(items, indent=4) + ";"
#     return js_code


# if __name__ == "__main__":
#     root = "/vePFS-MLP/buaa/fenghaoran/workspace/VoxhammerPage/assets/image_condition_editing"  # 换成你的文件夹路径
#     js_string = generate_items_js(root)
#     print(js_string)
#     # 你也可以保存到文件
#     with open("items.js", "w", encoding="utf-8") as f:
#         f.write(js_string)