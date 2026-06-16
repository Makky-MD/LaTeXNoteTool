import os
import subprocess

XELATEX_PATH = "./TinyTeX/bin/windows/xelatex.exe"

def clean_temp_files(tex_file):
    base = os.path.splitext(tex_file)[0]
    exts = [".aux", ".log", ".toc", ".out", ".synctex.gz", ".fls", ".fdb_latexmk"]
    for e in exts:
        f = base + e
        if os.path.exists(f):
            try: os.remove(f)
            except: pass

def compile_tex(tex_file, pdf_file, timeout=180):
    if not os.path.exists(XELATEX_PATH):
        return False, "未找到 TinyTeX 编译环境"

    clean_temp_files(tex_file)

    try:
        res = subprocess.run(
            [XELATEX_PATH, "-interaction=nonstopmode", tex_file],
            capture_output=True, text=True,
            timeout=timeout,
            creationflags=subprocess.CREATE_NO_WINDOW
        )
        ok = os.path.exists(pdf_file)
        return ok, res.stdout if ok else res.stderr
    except Exception as e:
        return False, str(e)