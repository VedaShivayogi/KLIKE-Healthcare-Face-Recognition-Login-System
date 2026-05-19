"""
KLIKE Healthcare – Face Recognition Login System
Run this file from the project root to launch the application.

    python run.py
"""
import sys
import os

# Ensure core/ and modules/ are on the path
ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(ROOT, "core"))
sys.path.insert(0, os.path.join(ROOT, "modules"))

from core.app import KlikeApp
import tkinter as tk

if __name__ == "__main__":
    app = KlikeApp()
    icon_path = os.path.join(ROOT, "assets", "icon.ico")
    try:
        app.iconphoto(True, tk.PhotoImage(file=icon_path))
    except Exception:
        pass
    app.mainloop()
