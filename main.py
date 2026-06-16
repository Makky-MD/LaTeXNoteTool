import tkinter as tk
import os
from tkinter import filedialog, messagebox
from ui import LaTeXUI
import core

class App:
    def __init__(self, root):
        self.tex_file = "main.tex"
        self.pdf_file = "main.pdf"

        # UI 只负责界面，不负责逻辑
        self.ui = LaTeXUI(root,
            on_compile=self.compile,
            on_open_file=self.open_file,
            on_clean=self.clean,
            on_open_pdf=self.open_pdf
        )

        self.load_initial_file()

    def load_initial_file(self):
        if os.path.exists(self.tex_file):
            with open(self.tex_file, "r", encoding="utf-8") as f:
                self.ui.set_editor_content(f.read())

    def open_file(self):
        path = filedialog.askopenfilename(filetypes=[("TeX files", "*.tex")])
        if not path: return
        self.tex_file = path
        self.pdf_file = os.path.splitext(path)[0] + ".pdf"
        with open(path, "r", encoding="utf-8") as f:
            self.ui.set_editor_content(f.read())
        self.ui.set_status(f"已加载：{os.path.basename(path)}")

    def compile(self):
        content = self.ui.get_editor_content()
        with open(self.tex_file, "w", encoding="utf-8") as f:
            f.write(content)

        self.ui.set_status("编译中...")
        self.ui.root.update()

        ok, msg = core.compile_tex(self.tex_file, self.pdf_file)
        if ok:
            self.ui.set_status("编译完成，正在打开 PDF")
            os.startfile(self.pdf_file)
        else:
            messagebox.showerror("失败", msg)
            self.ui.set_status("编译失败")

    def clean(self):
        core.clean_temp_files(self.tex_file)
        self.ui.set_status("已清理临时文件")

    def open_pdf(self):
        if os.path.exists(self.pdf_file):
            os.startfile(self.pdf_file)
        else:
            messagebox.showwarning("提示", "PDF 未生成")

if __name__ == "__main__":
    root = tk.Tk()
    App(root)
    root.mainloop()