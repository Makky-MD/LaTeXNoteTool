import os
import subprocess
import tkinter as tk
from tkinter import scrolledtext, messagebox, filedialog

XELATEX_PATH = r"./TinyTeX/bin/windows/xelatex.exe"
TEX_FILE = "main.tex"
PDF_FILE = "main.pdf"
TEMP_SUFFIXES = [".aux", ".log", ".toc", ".out", ".synctex.gz", ".fls", ".fdb_latexmk"]

def clean_temp_files():
    count = 0
    base_name = os.path.splitext(TEX_FILE)[0]
    for suffix in TEMP_SUFFIXES:
        file_path = f"{base_name}{suffix}"
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
                count += 1
            except Exception:
                pass
    return count

# 新增：打开外部tex文件
def open_tex_file():
    global TEX_FILE, PDF_FILE
    path = filedialog.askopenfilename(filetypes=[("LaTeX文件", "*.tex"), ("所有文件", "*.*")])
    if not path:
        return
    TEX_FILE = path
    PDF_FILE = os.path.splitext(TEX_FILE)[0] + ".pdf"
    with open(TEX_FILE, "r", encoding="utf-8") as f:
        text_editor.delete(1.0, tk.END)
        text_editor.insert(1.0, f.read())
    status_label.config(text=f"✅ 已加载文件：{os.path.basename(TEX_FILE)}")

def compile_latex():
    if not os.path.exists(XELATEX_PATH):
        messagebox.showerror("错误", "找不到编译工具！")
        return
    # 保存编辑器内容到当前tex文件
    content = text_editor.get(1.0, tk.END)
    with open(TEX_FILE, "w", encoding="utf-8") as f:
        f.write(content)

    clean_temp_files()
    status_label.config(text="⏳ 正在编译...")
    root.update()

    try:
        # 延长超时时间，适配大文件
        result = subprocess.run(
            [XELATEX_PATH, "-interaction=nonstopmode", TEX_FILE],
            cwd=os.getcwd(),
            timeout=180,  # 改成3分钟，大文件够用
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            creationflags=subprocess.CREATE_NO_WINDOW
        )
        if os.path.exists(PDF_FILE):
            clean_temp_files()
            status_label.config(text="🎉 编译成功，自动打开PDF")
            os.startfile(PDF_FILE)
        else:
            messagebox.showerror("编译失败", result.stderr)
    except subprocess.TimeoutExpired:
        status_label.config(text="❌ 编译超时")
        messagebox.showerror("超时", "文件过大/内容复杂，编译超时")
    except Exception as e:
        messagebox.showerror("错误", str(e))

def open_pdf():
    if os.path.exists(PDF_FILE):
        os.startfile(PDF_FILE)
    else:
        messagebox.showwarning("提示", "请先编译生成PDF")

def manual_clean():
    count = clean_temp_files()
    status_label.config(text=f"✅ 清理 {count} 个临时文件")

def load_template():
    if os.path.exists(TEX_FILE):
        with open(TEX_FILE, "r", encoding="utf-8") as f:
            text_editor.delete(1.0, tk.END)
            text_editor.insert(1.0, f.read())
        status_label.config(text="📄 默认模板已加载")

# UI
root = tk.Tk()
root.title("LaTeXNoteTool")
root.geometry("1000x700")

btn_frame = tk.Frame(root, padx=10, pady=10)
btn_frame.pack(fill=tk.X)

# 新增【打开TEX文件】按钮
tk.Button(btn_frame, text="打开TEX文件", command=open_tex_file, width=12, height=2).grid(row=0, column=0, padx=5)
tk.Button(btn_frame, text="编译生成PDF", command=compile_latex, width=12, height=2, bg="#90EE90").grid(row=0, column=1, padx=5)
tk.Button(btn_frame, text="清理临时文件", command=manual_clean, width=12, height=2).grid(row=0, column=2, padx=5)
tk.Button(btn_frame, text="打开PDF", command=open_pdf, width=12, height=2, bg="#ADD8E6").grid(row=0, column=3, padx=5)

text_editor = scrolledtext.ScrolledText(root, font=("Consolas", 11), wrap=tk.WORD)
text_editor.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)

status_label = tk.Label(root, text="就绪", anchor="w", padx=10, pady=5)
status_label.pack(fill=tk.X)

root.after(200, load_template)
root.mainloop()