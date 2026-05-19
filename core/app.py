"""
KLIKE Healthcare – Face Recognition Login System
Entry point: run from project root using run.py
"""

import sys
import os

# ── Path setup so modules/ and config/ are reachable ──────────────────────────
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(ROOT, "modules"))

CONFIG_DIR = os.path.join(ROOT, "config")
ASSETS_DIR = os.path.join(ROOT, "assets")
NAMESLIST   = os.path.join(CONFIG_DIR, "nameslist.txt")

from detector          import main_app
from create_classifier import train_classifer
from create_dataset    import start_capture
import tkinter as tk
from tkinter import messagebox
import math

names = set()

# ─── Color Palette ─────────────────────────────────────────────────────────────
BG_DARK     = "#0A1628"
BG_CARD     = "#0F2040"
TEAL_BRIGHT = "#00D4C8"
TEAL_DIM    = "#00897B"
WHITE       = "#FFFFFF"
WHITE_DIM   = "#B0C4D8"
RED_ALERT   = "#FF4C6A"
GREEN_OK    = "#00E5A0"
BORDER      = "#1A3A5C"
INPUT_BG    = "#0D1F38"


# ─── Animated ECG Canvas ───────────────────────────────────────────────────────
class PulsingCanvas(tk.Canvas):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self._phase = 0
        self._animate()

    def _ecg_y(self, x, phase, width, height):
        t = ((x + phase) % max(width, 1)) / max(width, 1)
        if 0.38 < t < 0.42:
            return height / 2 - 26
        elif 0.42 < t < 0.46:
            return height / 2 + 13
        elif 0.46 < t < 0.50:
            return height / 2 - 6
        else:
            return height / 2 + math.sin(t * 2 * math.pi * 2) * 4

    def _animate(self):
        self.delete("ecg")
        w = self.winfo_reqwidth() or 780
        h = self.winfo_reqheight() or 50
        pts = []
        for x in range(0, w, 3):
            pts.extend([x, self._ecg_y(x, self._phase, w, h)])
        if len(pts) >= 4:
            self.create_line(pts, fill=TEAL_BRIGHT, width=2, smooth=True, tags="ecg")
        self._phase = (self._phase + 4) % w
        self.after(40, self._animate)


# ─── Helpers ───────────────────────────────────────────────────────────────────
def styled_btn(parent, text, command, bg=TEAL_BRIGHT, fg=BG_DARK, pad_x=22, pad_y=10):
    btn = tk.Button(parent, text=text, command=command, bg=bg, fg=fg,
                    font=("Segoe UI", 10, "bold"), relief="flat", bd=0,
                    cursor="hand2", padx=pad_x, pady=pad_y,
                    activebackground=TEAL_DIM, activeforeground=WHITE)
    btn.bind("<Enter>", lambda e: btn.config(bg=TEAL_DIM if bg == TEAL_BRIGHT else "#1A3A5C"))
    btn.bind("<Leave>", lambda e: btn.config(bg=bg))
    return btn

def ghost_btn(parent, text, command):
    btn = tk.Button(parent, text=text, command=command,
                    bg=BG_DARK, fg=WHITE_DIM, font=("Segoe UI", 10),
                    relief="flat", bd=0, cursor="hand2", padx=16, pady=8,
                    activebackground=BORDER, activeforeground=WHITE)
    btn.bind("<Enter>", lambda e: btn.config(bg=BORDER))
    btn.bind("<Leave>", lambda e: btn.config(bg=BG_DARK))
    return btn

def sep(parent):
    tk.Frame(parent, bg=BORDER, height=1).pack(fill="x", pady=8)

def make_input(parent, placeholder=""):
    frame = tk.Frame(parent, bg=INPUT_BG, highlightthickness=1,
                     highlightbackground=BORDER, highlightcolor=TEAL_BRIGHT)
    entry = tk.Entry(frame, bg=INPUT_BG, fg=WHITE, font=("Segoe UI", 11),
                     relief="flat", bd=6, insertbackground=TEAL_BRIGHT,
                     selectbackground=TEAL_DIM)
    entry.pack(fill="x")
    entry.insert(0, placeholder)
    entry.config(fg=WHITE_DIM)
    def fi(e):
        if entry.get() == placeholder:
            entry.delete(0, "end"); entry.config(fg=WHITE)
        frame.config(highlightbackground=TEAL_BRIGHT)
    def fo(e):
        if not entry.get():
            entry.insert(0, placeholder); entry.config(fg=WHITE_DIM)
        frame.config(highlightbackground=BORDER)
    entry.bind("<FocusIn>", fi)
    entry.bind("<FocusOut>", fo)
    return frame, entry

def make_header(parent, subtitle="Healthcare Face Authentication"):
    hdr = tk.Frame(parent, bg=BG_CARD)
    hdr.pack(fill="x")
    PulsingCanvas(hdr, bg=BG_CARD, height=44, highlightthickness=0).pack(fill="x")
    row = tk.Frame(hdr, bg=BG_CARD)
    row.pack(fill="x", padx=28, pady=(0, 12))
    cross = tk.Frame(row, bg=TEAL_BRIGHT, width=36, height=36)
    cross.pack_propagate(False)
    cross.pack(side="left", padx=(0, 10))
    tk.Label(cross, text="✚", font=("Segoe UI", 18, "bold"),
             bg=TEAL_BRIGHT, fg=BG_DARK).place(relx=.5, rely=.5, anchor="center")
    col = tk.Frame(row, bg=BG_CARD)
    col.pack(side="left")
    tk.Label(col, text="KLIKE", font=("Segoe UI", 26, "bold"),
             bg=BG_CARD, fg=TEAL_BRIGHT).pack(anchor="w")
    tk.Label(col, text=subtitle, font=("Segoe UI", 9),
             bg=BG_CARD, fg=WHITE_DIM).pack(anchor="w")
    tk.Frame(hdr, bg=TEAL_BRIGHT, height=2).pack(fill="x")

def make_status(parent, text="System Ready  •  All Services Operational"):
    bar = tk.Frame(parent, bg=BG_CARD)
    bar.pack(fill="x", side="bottom")
    tk.Frame(bar, bg=TEAL_BRIGHT, height=1).pack(fill="x")
    row = tk.Frame(bar, bg=BG_CARD)
    row.pack(fill="x", padx=14, pady=5)
    tk.Label(row, text="●", font=("Segoe UI", 8), bg=BG_CARD, fg=GREEN_OK).pack(side="left")
    tk.Label(row, text=f"  {text}", font=("Segoe UI", 8), bg=BG_CARD, fg=WHITE_DIM).pack(side="left")
    tk.Label(row, text="KLIKE v2.1", font=("Segoe UI", 8), bg=BG_CARD, fg=WHITE_DIM).pack(side="right")


# ═══════════════════════════════════════════════════════════════════════════════
class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=BG_DARK)
        self.controller = controller
        make_header(self)
        body = tk.Frame(self, bg=BG_DARK)
        body.pack(expand=True, fill="both", padx=36, pady=18)
        card = tk.Frame(body, bg=BG_CARD, highlightthickness=1, highlightbackground=BORDER)
        card.pack(expand=True, fill="both")
        inner = tk.Frame(card, bg=BG_CARD)
        inner.pack(expand=True)
        tk.Label(inner, text="Patient & Staff Portal", font=("Segoe UI", 16, "bold"),
                 bg=BG_CARD, fg=WHITE).pack(pady=(30, 4))
        tk.Label(inner, text="Secure biometric access for healthcare professionals\nand registered patients.",
                 font=("Segoe UI", 10), bg=BG_CARD, fg=WHITE_DIM, justify="center").pack(pady=(0, 20))
        sep(inner)
        pill_row = tk.Frame(inner, bg=BG_CARD)
        pill_row.pack(pady=(4, 18))
        for icon, txt in [("🔒", "Encrypted"), ("⚡", "Real-time"), ("🏥", "HIPAA Ready")]:
            p = tk.Frame(pill_row, bg=INPUT_BG, highlightthickness=1, highlightbackground=BORDER)
            p.pack(side="left", padx=6, ipadx=10, ipady=4)
            tk.Label(p, text=f"{icon}  {txt}", font=("Segoe UI", 8), bg=INPUT_BG, fg=WHITE_DIM).pack()
        sep(inner)
        btn_row = tk.Frame(inner, bg=BG_CARD)
        btn_row.pack(pady=18)
        styled_btn(btn_row, "  ＋  Register New User",
                   lambda: controller.show_frame("PageOne"), pad_x=26, pad_y=12).grid(row=0, column=0, padx=10)
        styled_btn(btn_row, "  ▶  Authenticate / Login",
                   lambda: controller.show_frame("PageTwo"),
                   bg=BG_CARD, fg=TEAL_BRIGHT, pad_x=20, pad_y=11).grid(row=0, column=1, padx=10)
        ghost_btn(inner, "✕  Exit System", self.on_closing).pack(pady=(0, 20))
        make_status(self)

    def on_closing(self):
        if messagebox.askokcancel("Exit KLIKE", "Securely close the system?"):
            global names
            with open(NAMESLIST, "w") as f:
                for n in names: f.write(n + " ")
            self.controller.destroy()


class PageOne(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=BG_DARK)
        self.controller = controller
        make_header(self, "New User Registration")
        body = tk.Frame(self, bg=BG_DARK)
        body.pack(expand=True, fill="both", padx=36, pady=18)
        card = tk.Frame(body, bg=BG_CARD, highlightthickness=1, highlightbackground=BORDER)
        card.pack(expand=True, fill="both")
        inner = tk.Frame(card, bg=BG_CARD)
        inner.pack(expand=True)
        # Step indicator
        step_row = tk.Frame(inner, bg=BG_CARD)
        step_row.pack(pady=(26, 4))
        for i, (num, label, active) in enumerate([("1","Register",True),("2","Capture",False),("3","Train",False),("4","Access",False)]):
            bg_c = TEAL_BRIGHT if active else INPUT_BG
            fg_c = BG_DARK if active else WHITE_DIM
            sf = tk.Frame(step_row, bg=BG_CARD); sf.pack(side="left", padx=6)
            c = tk.Frame(sf, bg=bg_c, width=26, height=26); c.pack_propagate(False); c.pack()
            tk.Label(c, text=num, font=("Segoe UI", 9, "bold"), bg=bg_c, fg=fg_c).place(relx=.5, rely=.5, anchor="center")
            tk.Label(sf, text=label, font=("Segoe UI", 8), bg=BG_CARD, fg=TEAL_BRIGHT if active else BORDER).pack()
            if i < 3: tk.Label(step_row, text="──", font=("Segoe UI", 8), bg=BG_CARD, fg=BORDER).pack(side="left")
        tk.Label(inner, text="Enter Patient / Staff Full Name", font=("Segoe UI", 13, "bold"),
                 bg=BG_CARD, fg=WHITE).pack(pady=(18, 6))
        tk.Label(inner, text="This name links to the biometric profile.",
                 font=("Segoe UI", 8), bg=BG_CARD, fg=WHITE_DIM).pack()
        sep(inner)
        wrap = tk.Frame(inner, bg=BG_CARD); wrap.pack(pady=14)
        tk.Label(wrap, text="Full Name", font=("Segoe UI", 9, "bold"), bg=BG_CARD, fg=WHITE_DIM).pack(anchor="w")
        self.name_frame, self.user_name = make_input(wrap, "e.g. John Doe")
        self.name_frame.pack(fill="x", ipady=2, pady=(4, 0), ipadx=110)
        sep(inner)
        btn_row = tk.Frame(inner, bg=BG_CARD); btn_row.pack(pady=14)
        ghost_btn(btn_row, "← Back", lambda: controller.show_frame("StartPage")).pack(side="left", padx=8)
        styled_btn(btn_row, "Next  →", self.start_training, pad_x=22, pad_y=10).pack(side="left", padx=8)
        ghost_btn(btn_row, "Clear", self._clear).pack(side="left", padx=8)
        make_status(self)

    def _clear(self):
        self.user_name.delete(0, "end")
        self.user_name.insert(0, "e.g. John Doe")
        self.user_name.config(fg=WHITE_DIM)

    def start_training(self):
        global names
        name = self.user_name.get().strip()
        if name in ("", "e.g. John Doe", "None"):
            messagebox.showerror("KLIKE", "Please enter a valid full name."); return
        if name in names:
            messagebox.showerror("KLIKE", f'Profile "{name}" already exists.'); return
        names.add(name)
        self.controller.active_name = name
        self.controller.frames["PageTwo"].refresh_names()
        self.controller.show_frame("PageThree")


class PageTwo(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=BG_DARK)
        self.controller = controller
        make_header(self, "Biometric Authentication")
        body = tk.Frame(self, bg=BG_DARK)
        body.pack(expand=True, fill="both", padx=36, pady=18)
        card = tk.Frame(body, bg=BG_CARD, highlightthickness=1, highlightbackground=BORDER)
        card.pack(expand=True, fill="both")
        inner = tk.Frame(card, bg=BG_CARD); inner.pack(expand=True)
        tk.Label(inner, text="🔍  Identity Verification", font=("Segoe UI", 15, "bold"),
                 bg=BG_CARD, fg=WHITE).pack(pady=(28, 6))
        tk.Label(inner, text="Enter or select a registered profile to begin authentication.",
                 font=("Segoe UI", 8), bg=BG_CARD, fg=WHITE_DIM).pack()
        sep(inner)
        wrap = tk.Frame(inner, bg=BG_CARD); wrap.pack(pady=10)
        tk.Label(wrap, text="Registered Name", font=("Segoe UI", 9, "bold"), bg=BG_CARD, fg=WHITE_DIM).pack(anchor="w")
        self.name_frame, self.user_name = make_input(wrap, "Type a registered name")
        self.name_frame.pack(fill="x", ipady=2, pady=(4, 0), ipadx=100)
        or_row = tk.Frame(inner, bg=BG_CARD); or_row.pack(fill="x", padx=70, pady=6)
        tk.Frame(or_row, bg=BORDER, height=1).pack(side="left", fill="x", expand=True)
        tk.Label(or_row, text="  OR  ", font=("Segoe UI", 8), bg=BG_CARD, fg=WHITE_DIM).pack(side="left")
        tk.Frame(or_row, bg=BORDER, height=1).pack(side="left", fill="x", expand=True)
        drop_wrap = tk.Frame(inner, bg=BG_CARD); drop_wrap.pack()
        tk.Label(drop_wrap, text="Select from Profiles", font=("Segoe UI", 9, "bold"),
                 bg=BG_CARD, fg=WHITE_DIM).pack(anchor="w")
        self.menuvar = tk.StringVar(self)
        self.menuvar.set("— choose a profile —")
        opts = list(names) if names else ["(no profiles yet)"]
        self.dropdown = tk.OptionMenu(drop_wrap, self.menuvar, *opts)
        self.dropdown.config(bg=INPUT_BG, fg=WHITE, font=("Segoe UI", 10), relief="flat", bd=0,
                             highlightthickness=1, highlightbackground=BORDER,
                             activebackground=BG_CARD, padx=12, pady=6, width=26)
        self.dropdown["menu"].config(bg=INPUT_BG, fg=WHITE, font=("Segoe UI", 10))
        self.dropdown.pack(pady=(4, 0))
        sep(inner)
        btn_row = tk.Frame(inner, bg=BG_CARD); btn_row.pack(pady=14)
        ghost_btn(btn_row, "← Back", lambda: controller.show_frame("StartPage")).pack(side="left", padx=8)
        styled_btn(btn_row, "🔓  Authenticate", self.next_foo, pad_x=24, pad_y=10).pack(side="left", padx=8)
        make_status(self)

    def next_foo(self):
        typed = self.user_name.get().strip()
        dropdown_val = self.menuvar.get()
        name = None
        if dropdown_val not in ("— choose a profile —", "(no profiles yet)"): name = dropdown_val
        elif typed and typed != "Type a registered name": name = typed
        if not name:
            messagebox.showerror("KLIKE", "Please enter or select a registered name."); return
        self.controller.active_name = name
        self.controller.show_frame("PageFour")

    def refresh_names(self):
        global names
        self.menuvar.set("— choose a profile —")
        self.dropdown["menu"].delete(0, "end")
        for n in sorted(names):
            self.dropdown["menu"].add_command(label=n, command=tk._setit(self.menuvar, n))


class PageThree(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=BG_DARK)
        self.controller = controller
        make_header(self, "Biometric Data Capture")
        body = tk.Frame(self, bg=BG_DARK)
        body.pack(expand=True, fill="both", padx=36, pady=18)
        card = tk.Frame(body, bg=BG_CARD, highlightthickness=1, highlightbackground=BORDER)
        card.pack(expand=True, fill="both")
        inner = tk.Frame(card, bg=BG_CARD); inner.pack(expand=True)
        tk.Label(inner, text="📷  Facial Data Enrollment", font=("Segoe UI", 15, "bold"),
                 bg=BG_CARD, fg=WHITE).pack(pady=(26, 6))
        tk.Label(inner, text="Step 1: Capture 300 samples  →  Step 2: Train AI Model",
                 font=("Segoe UI", 8), bg=BG_CARD, fg=WHITE_DIM).pack()
        sep(inner)
        prog = tk.Frame(inner, bg=INPUT_BG, highlightthickness=1, highlightbackground=BORDER)
        prog.pack(padx=50, fill="x", pady=10)
        self.numimglabel = tk.Label(prog, text="  ⏳  Images captured:  0 / 300",
                                    font=("Segoe UI", 11, "bold"), bg=INPUT_BG, fg=TEAL_BRIGHT, pady=10)
        self.numimglabel.pack()
        inst = tk.Frame(inner, bg=BG_DARK, highlightthickness=1, highlightbackground=BORDER)
        inst.pack(padx=50, fill="x", pady=6)
        for line in ["👤  Look directly at the camera",
                     "💡  Ensure good lighting on your face",
                     "🔄  Slowly turn head left and right",
                     "✅  Press Q or wait for 300 images to complete"]:
            tk.Label(inst, text=line, font=("Segoe UI", 8), bg=BG_DARK, fg=WHITE_DIM,
                     anchor="w", padx=12, pady=3).pack(fill="x")
        sep(inner)
        btn_row = tk.Frame(inner, bg=BG_CARD); btn_row.pack(pady=14)
        styled_btn(btn_row, "📸  Capture Face Data", self.capimg, pad_x=20, pad_y=10).pack(side="left", padx=10)
        styled_btn(btn_row, "🧠  Train AI Model", self.trainmodel,
                   bg=GREEN_OK, fg=BG_DARK, pad_x=20, pad_y=10).pack(side="left", padx=10)
        make_status(self, "Enrollment Mode  •  Camera Ready")

    def capimg(self):
        self.numimglabel.config(text="  🔴  Capturing … please wait", fg=RED_ALERT)
        self.update()
        messagebox.showinfo("KLIKE – Instructions",
                            "300 facial samples will be captured.\nLook at the camera and move slightly.\nPress Q or ESC to stop early.")
        x = start_capture(self.controller.active_name)
        self.controller.num_of_images = x
        self.numimglabel.config(text=f"  ✅  Images captured:  {x} / 300",
                                fg=GREEN_OK if x >= 300 else TEAL_BRIGHT)

    def trainmodel(self):
        if self.controller.num_of_images < 300:
            messagebox.showerror("KLIKE", "Capture at least 300 face images first."); return
        self.numimglabel.config(text="  🧠  Training model … please wait", fg=TEAL_BRIGHT)
        self.update()
        train_classifer(self.controller.active_name)
        messagebox.showinfo("KLIKE – Success", "✅  Biometric model trained!\nProfile is active for authentication.")
        self.controller.show_frame("PageFour")


class PageFour(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg=BG_DARK)
        self.controller = controller
        make_header(self, "Authentication Terminal")
        body = tk.Frame(self, bg=BG_DARK)
        body.pack(expand=True, fill="both", padx=36, pady=18)
        card = tk.Frame(body, bg=BG_CARD, highlightthickness=1, highlightbackground=BORDER)
        card.pack(expand=True, fill="both")
        inner = tk.Frame(card, bg=BG_CARD); inner.pack(expand=True)
        cam = tk.Frame(inner, bg=TEAL_BRIGHT, width=68, height=68)
        cam.pack_propagate(False); cam.pack(pady=(28, 10))
        tk.Label(cam, text="📷", font=("Segoe UI", 32), bg=TEAL_BRIGHT).place(relx=.5, rely=.5, anchor="center")
        tk.Label(inner, text="Ready to Authenticate", font=("Segoe UI", 15, "bold"),
                 bg=BG_CARD, fg=WHITE).pack(pady=(4, 4))
        self.name_label = tk.Label(inner, text="", font=("Segoe UI", 10), bg=BG_CARD, fg=TEAL_BRIGHT)
        self.name_label.pack()
        sep(inner)
        info = tk.Frame(inner, bg=BG_DARK, highlightthickness=1, highlightbackground=BORDER)
        info.pack(padx=70, fill="x", pady=8)
        for icon, txt in [("🎯", "Face recognition begins immediately"),
                           ("⏱️", "Session timeout: 5 seconds of inactivity"),
                           ("🔐", "All data processed locally — never uploaded")]:
            row = tk.Frame(info, bg=BG_DARK); row.pack(fill="x", padx=12, pady=4)
            tk.Label(row, text=icon, font=("Segoe UI", 11), bg=BG_DARK).pack(side="left")
            tk.Label(row, text=f"  {txt}", font=("Segoe UI", 8), bg=BG_DARK, fg=WHITE_DIM, anchor="w").pack(side="left")
        sep(inner)
        btn_row = tk.Frame(inner, bg=BG_CARD); btn_row.pack(pady=14)
        styled_btn(btn_row, "  ▶  Launch Face Recognition", self.openwebcam,
                   pad_x=26, pad_y=12).pack(side="left", padx=10)
        ghost_btn(btn_row, "🏠  Home", lambda: controller.show_frame("StartPage")).pack(side="left", padx=10)
        make_status(self, "Authentication Ready  •  Camera Standby")

    def tkraise(self, *args, **kwargs):
        super().tkraise(*args, **kwargs)
        self.name_label.config(text=f"Profile: {self.controller.active_name or '—'}")

    def openwebcam(self):
        main_app(self.controller.active_name)


# ═══════════════════════════════════════════════════════════════════════════════
class KlikeApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        global names
        try:
            with open(NAMESLIST, "r") as f:
                for n in f.read().split():
                    if n: names.add(n)
        except FileNotFoundError:
            pass
        self.title("KLIKE – Healthcare Face Recognition System")
        self.resizable(False, False)
        self.geometry("780x580")
        self.configure(bg=BG_DARK)
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.active_name  = None
        self.num_of_images = 0
        container = tk.Frame(self, bg=BG_DARK)
        container.pack(fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}
        for F in (StartPage, PageOne, PageTwo, PageThree, PageFour):
            frame = F(parent=container, controller=self)
            self.frames[F.__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame("StartPage")

    def show_frame(self, page_name):
        self.frames[page_name].tkraise()

    def on_closing(self):
        if messagebox.askokcancel("Exit KLIKE", "Securely exit the system?"):
            global names
            with open(NAMESLIST, "w") as f:
                for n in names: f.write(n + " ")
            self.destroy()


if __name__ == "__main__":
    app = KlikeApp()
    icon_path = os.path.join(ASSETS_DIR, "icon.ico")
    try:
        app.iconphoto(True, tk.PhotoImage(file=icon_path))
    except Exception:
        pass
    app.mainloop()
