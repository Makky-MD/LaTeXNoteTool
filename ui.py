import tkinter as tk
from tkinter import scrolledtext

class LaTeXUI:
    def __init__(self, root, on_compile, on_open_file, on_clean, on_open_pdf):
        self.root = root
        self.root.title("LaTeXNoteTool")
        self.root.geometry("1000x700")

        # 按钮回调（由外部传入，UI不关心实现）
        self.on_compile = on_compile
        self.on_open_file = on_open_file
        self.on_clean = on_clean
        self.on_open_pdf = on_open_pdf

        self.create_widgets()

    def create_widgets(self):
        # 按钮栏
        btn_frame = tk.Frame(self.root, padx=10, pady=10)
        btn_frame.pack(fill=tk.X)

        tk.Button(btn_frame, text="打开TEX文件", command=self.on_open_file, width=12, height=2)\
            .grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="编译生成PDF", command=self.on_compile, width=12, height=2, bg="#90EE90")\
            .grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="清理临时文件", command=self.on_clean, width=12, height=2)\
            .grid(row=0, column=2, padx=5)
        tk.Button(btn_frame, text="打开PDF", command=self.on_open_pdf, width=12, height=2, bg="#ADD8E6")\
            .grid(row=0, column=3, padx=5)

        # 编辑区
        self.text_editor = scrolledtext.ScrolledText(self.root, font=("Consolas", 11), wrap=tk.WORD)
        self.text_editor.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)

        # 状态栏
        self.status_label = tk.Label(self.root, text="就绪", anchor="w", padx=10, pady=5)
        self.status_label.pack(fill=tk.X)

    def set_status(self, text):
        self.status_label.config(text=text)

    def get_editor_content(self):
        return self.text_editor.get(1.0, tk.END)

    def set_editor_content(self, content):
        self.text_editor.delete(1.0, tk.END)
        self.text_editor.insert(1.0, content)