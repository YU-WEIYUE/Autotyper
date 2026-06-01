import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from pynput.keyboard import Controller, Key
import pyperclip
import time
import threading

kb = Controller()

def smart_type(text, interval=0.08):
    i = 0
    length = len(text)
    while i < length:
        c = text[i]
        if ord(c) < 128:
            kb.type(c)
            time.sleep(interval)
            i += 1
        else:
            j = i
            while j < length and ord(text[j]) >= 128:
                j += 1
            part = text[i:j]
            pyperclip.copy(part)
            time.sleep(0.05)
            with kb.pressed(Key.ctrl):
                kb.press('v')
                kb.release('v')
            time.sleep(0.1)
            i = j

def typing_task(content, delay_sec, char_interval):
    for i in range(delay_sec, 0, -1):
        btn_text.set(f"剩余 {i} 秒")
        time.sleep(1)
    btn_text.set("正在输入...")
    try:
        smart_type(content, char_interval)
    except Exception as e:
        messagebox.showerror("错误", str(e))
    btn_text.set("开始自动输入")

def start_typing():
    content = text_area.get("1.0", tk.END).strip()
    if not content:
        messagebox.showwarning("警告", "请输入内容")
        return
    start_btn.config(state=tk.DISABLED)
    try:
        delay = int(delay_var.get())
    except:
        delay = 5
        delay_var.set("5")
    t = threading.Thread(target=typing_task, args=(content, delay, 0.08), daemon=True)
    t.start()
    def check_thread():
        if t.is_alive():
            root.after(200, check_thread)
        else:
            start_btn.config(state=tk.NORMAL)
    check_thread()

root = tk.Tk()
root.title("AutoTyper")
root.geometry("700x500")
root.resizable(True, True)

# 标题（修复字体，正常显示）
tk.Label(root, text="网页自动打字工具", font=("Microsoft YaHei", 13, "bold")).pack(pady=4)

# 内容标签（间距缩小）
tk.Label(root, text="待输入内容：", font=("Microsoft YaHei", 10)).pack(anchor="w", padx=18, pady=2)

# 文本框高度保持你要的 15，不动！
text_area = scrolledtext.ScrolledText(root, font=("Microsoft YaHei", 10), height=15)
text_area.pack(padx=18, pady=2, fill=tk.X)

# 倒计时（间距收紧）
frame = ttk.Frame(root)
frame.pack(pady=2, fill=tk.X, padx=18)
tk.Label(frame, text="倒计时(秒)：", font=("Microsoft YaHei", 10)).pack(side=tk.LEFT)
delay_var = tk.StringVar(value="5")
ttk.Entry(frame, textvariable=delay_var, width=8, font=("Microsoft YaHei", 10)).pack(side=tk.LEFT, padx=5)

# 按钮上移，打开窗口立刻看见！
btn_text = tk.StringVar(value="开始输入")
start_btn = ttk.Button(root, textvariable=btn_text, command=start_typing)
start_btn.pack(pady=6, ipadx=40, ipady=5)

# 提示文字
tk.Label(root, text="操作：输入内容 → 点击按钮 → 5秒内点击目标输入框",
         font=("Microsoft YaHei", 9), fg="#666").pack(pady=2)

root.mainloop()
