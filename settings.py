import tkinter as tk
from tkinter import messagebox
from analyzer.analyzer import config
from controller import re_run_analysis

def open_settings(root, output_area, display_mode):
    win = tk.Toplevel(root)
    win.title("設定")
    win.grab_set()

    tk.Label(win, text="最小判定数").grid(row=0, column=0, sticky="w")
    min_rolls_var = tk.StringVar(win, value=str(config["min_rolls"]))
    tk.Entry(win, textvariable=min_rolls_var, width=10).grid(row=0, column=1, sticky="w")

    tk.Label(win, text="除外タグ（カンマ区切り）").grid(row=1, column=0, sticky="w")
    exclude_var = tk.StringVar(win, value=",".join(config["exclude_tags"]))
    tk.Entry(win, textvariable=exclude_var, width=30).grid(row=1, column=1, sticky="w")

    show_skill_var = tk.BooleanVar(win, value=config["show_skill_stats"])
    tk.Checkbutton(win, text="技能別集計を表示", variable=show_skill_var).grid(row=2, column=0, columnspan=2, sticky="w")

    show_unknown_var = tk.BooleanVar(win, value=config["show_unknown_details"])
    tk.Checkbutton(win, text="不明技能詳細を表示", variable=show_unknown_var).grid(row=3, column=0, columnspan=2, sticky="w")

    tk.Label(win, text="色の表示モード").grid(row=4, column=0, sticky="w")
    display_mode.set(display_mode.get())
    tk.Radiobutton(win, text="文字色のみ", variable=display_mode, value="foreground").grid(row=4, column=1, sticky="w")
    tk.Radiobutton(win, text="背景色＋自動文字色", variable=display_mode, value="background").grid(row=5, column=1, sticky="w")

    def save():
        try:
            config["min_rolls"] = int(min_rolls_var.get())
        except ValueError:
            messagebox.showerror("設定エラー", "最小判定数には整数を入力してください。")
            return
        config["exclude_tags"] = [t.strip() for t in exclude_var.get().split(",") if t.strip()]
        config["show_skill_stats"] = show_skill_var.get()
        config["show_unknown_details"] = show_unknown_var.get()
        win.destroy()

        # ✅ 設定保存後に再解析
        re_run_analysis(output_area, display_mode)

    tk.Button(win, text="保存", command=save).grid(row=6, column=0, pady=5)
    tk.Button(win, text="キャンセル", command=win.destroy).grid(row=6, column=1, pady=5)