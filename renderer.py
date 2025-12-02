import tkinter as tk

def render_with_colors(text_widget, result_text, character_colors, mode="foreground"):
    text_widget.config(state="normal")

    # タグ定義（キャラごとに色設定） → 毎回上書き
    for name, color in character_colors.items():
        tag_name = f"char_{name}"
        if mode == "foreground":
            text_widget.tag_config(tag_name, foreground=color, background="white")
        elif mode == "background":
            r = int(color[1:3], 16)
            g = int(color[3:5], 16)
            b = int(color[5:7], 16)
            brightness = (r*299 + g*587 + b*114) / 1000
            fg = "black" if brightness > 128 else "white"
            text_widget.tag_config(tag_name, background=color, foreground=fg)

    # 行ごとに文字列を挿入 → その後に色付け
    text_widget.delete("1.0", "end")  # ← 前の内容を消す
    for line in result_text.split("\n"):
        start_index = text_widget.index("end-1c")   # 挿入前の位置
        text_widget.insert("end", line + "\n")
        end_index = text_widget.index("end-1c")     # 挿入後の位置

        for name, color in character_colors.items():
            if name in line:  # 行にキャラ名が含まれていれば色付け
                tag_name = f"char_{name}"
                text_widget.tag_add(tag_name, start_index, end_index)
                text_widget.tag_raise(tag_name)
                break