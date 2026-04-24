import tkinter as tk
from tkinter import ttk
import urllib.parse
import urllib.request
import json
import math

LANGUAGES = {
    "Auto Detect": "auto",
    "Indonesian": "id",
    "English": "en",
    "Japanese": "ja",
    "Korean": "ko",
    "French": "fr",
    "German": "de",
    "Spanish": "es",
    "Arabic": "ar",
    "Chinese (Simplified)": "zh-cn",
    "Russian": "ru",
    "Portuguese": "pt",
    "Hindi": "hi",
}

class APKTranslatorPro:
    def __init__(self, root):
        self.root = root
        self.root.title("APK Translator")
        self.root.geometry("720x520")
        self.root.configure(bg="#6e7a97")
        self.mode = "PC"

        self.setup_style()
        self.setup_ui()
        self.fade_in()

    # ===== STYLE =====
    def setup_style(self):
        style = ttk.Style()
        style.theme_use("default")

        style.configure("TCombobox",
                        fieldbackground="#1e293b",
                        background="#1e293b",
                        foreground="white")

    # ===== UI =====
    def setup_ui(self):
        self.main = tk.Frame(self.root, bg="#0f172a")
        self.main.place(relx=0, rely=1, relwidth=1, relheight=1)
        self.slide_in(self.main)

        tk.Label(self.main,
                 text="APK Translator",
                 font=("Segoe UI", 22, "bold"),
                 fg="#38bdf8",
                 bg="#0f172a").pack(pady=15)

        # INPUT
        self.input_text = tk.Text(self.main,
                                 height=4,
                                 bg="#1e293b",
                                 fg="white",
                                 insertbackground="white",
                                 bd=0,
                                 font=("Segoe UI", 11))
        self.input_text.pack(padx=30, pady=10, fill="x")

        # DROPDOWN
        self.lang_var = tk.StringVar(value="Indonesian")
        self.lang_menu = ttk.Combobox(self.main,
                                     textvariable=self.lang_var,
                                     values=list(LANGUAGES.keys()),
                                     state="readonly")
        self.lang_menu.pack(pady=5)

        # BUTTON FRAME
        btn_frame = tk.Frame(self.main, bg="#0f172a")
        btn_frame.pack(pady=15)

        self.create_button(btn_frame, "Translate", "#38bdf8", self.animate_translate, 0)
        self.create_button(btn_frame, "Copy", "#334155", self.copy_text, 1)
        self.create_button(btn_frame, "Switch Mode", "#22c55e", self.switch_mode, 2)

        # OUTPUT
        self.output_text = tk.Text(self.main,
                                  height=4,
                                  bg="#1e293b",
                                  fg="#22c55e",
                                  bd=0,
                                  font=("Segoe UI", 11))
        self.output_text.pack(padx=30, pady=10, fill="x")

        # CANVAS LOADING
        self.canvas = tk.Canvas(self.main,
                                width=700,
                                height=80,
                                bg="#0f172a",
                                highlightthickness=0)
        self.canvas.pack()

        # EXIT BUTTON
        self.exit_btn = tk.Label(self.main,
                                 text="Exit",
                                 bg="#ef4444",
                                 fg="white",
                                 font=("Segoe UI", 10, "bold"),
                                 padx=15,
                                 pady=5,
                                 cursor="hand2")
        self.exit_btn.pack(pady=10)
        self.exit_btn.bind("<Button-1>", lambda e: self.fade_out())

    # ===== BUTTON CUSTOM =====
    def create_button(self, parent, text, color, command, col):
        btn = tk.Label(parent,
                       text=text,
                       bg=color,
                       fg="black" if color == "#38bdf8" else "white",
                       font=("Segoe UI", 10, "bold"),
                       padx=12,
                       pady=6,
                       cursor="hand2")

        btn.grid(row=0, column=col, padx=8)

        # Hover effect
        btn.bind("<Enter>", lambda e: btn.config(bg="#0ea5e9"))
        btn.bind("<Leave>", lambda e: btn.config(bg=color))
        btn.bind("<Button-1>", lambda e: command())

    # ===== TRANSLATE =====
    def translate_online(self, text, target):
        try:
            url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl=auto&tl={target}&dt=t&q={urllib.parse.quote(text)}"
            response = urllib.request.urlopen(url)
            result = json.loads(response.read())
            return result[0][0][0]
        except:
            return "Error translate"

    def animate_translate(self):
        self.start_loading()
        self.root.after(200, self.do_translate)

    def do_translate(self):
        text = self.input_text.get("1.0", tk.END).strip()
        lang = LANGUAGES[self.lang_var.get()]

        result = self.translate_online(text, lang)

        self.stop_loading()
        self.output_text.delete("1.0", tk.END)
        self.output_text.insert(tk.END, result)

    # ===== LOADING SPINNER =====
    def start_loading(self):
        self.loading = True
        self.angle = 0
        self.animate_spinner()

    def stop_loading(self):
        self.loading = False
        self.canvas.delete("all")

    def animate_spinner(self):
        if not self.loading:
            return

        self.canvas.delete("all")

        x, y = 350, 40
        r = 18

        for i in range(12):
            angle = (self.angle + i * 30) * math.pi / 180
            x1 = x + r * 0.5 * math.cos(angle)
            y1 = y + r * 0.5 * math.sin(angle)
            x2 = x + r * math.cos(angle)
            y2 = y + r * math.sin(angle)

            self.canvas.create_line(x1, y1, x2, y2,
                                    fill="#38bdf8",
                                    width=3)

        self.angle += 15
        self.root.after(50, self.animate_spinner)

    # ===== COPY =====
    def copy_text(self):
        text = self.output_text.get("1.0", tk.END)
        self.root.clipboard_clear()
        self.root.clipboard_append(text)

    # ===== MODE =====
    def switch_mode(self):
        if self.mode == "PC":
            self.mode = "Mobile"
            self.root.geometry("360x640")
        else:
            self.mode = "PC"
            self.root.geometry("720x520")

    # ===== ANIMATION =====
    def slide_in(self, widget):
        for i in range(20):
            widget.place(relx=0, rely=1 - i * 0.05)
            self.root.update()
            self.root.after(10)

    def fade_in(self):
        for i in range(10):
            self.root.attributes("-alpha", i * 0.1)
            self.root.update()
            self.root.after(20)

    def fade_out(self):
        for i in range(10, -1, -1):
            self.root.attributes("-alpha", i * 0.1)
            self.root.update()
            self.root.after(20)
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = APKTranslatorPro(root)
    root.mainloop()