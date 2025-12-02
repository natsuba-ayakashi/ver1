import tkinter as tk
from tkinter import scrolledtext
from controller import run_analysis, save_text
from settings import open_settings
from renderer import render_with_colors

root = tk.Tk()
root.title("TRPGログ解析ツール（キャラ色切替対応・等幅フォント）")

display_mode = tk.StringVar(root, value="foreground")

# ✅ テキストエリアはここで一度だけ定義
output_area = scrolledtext.ScrolledText(
    root, width=100, height=40, font=("MS Gothic", 11), bg="white", fg="black"
)
output_area.config(tabs=("2c"))

frame = tk.Frame(root)
frame.pack(pady=10)

tk.Button(frame, text="ログファイルを選んで解析",
          command=lambda: run_analysis(output_area, display_mode)).pack(side=tk.LEFT, padx=5)
tk.Button(frame, text="設定",
          command=lambda: open_settings(root, output_area, display_mode)).pack(side=tk.LEFT, padx=5)
tk.Button(frame, text="結果をテキスト保存",
          command=lambda: save_text(output_area)).pack(side=tk.LEFT, padx=5)

# ✅ テキストエリアを最後に配置
output_area.pack(padx=10, pady=10)

root.mainloop()