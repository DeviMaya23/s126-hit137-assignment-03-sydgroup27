

import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import ImageTk, Image


class GameUI(tk.Tk):
    """A class to represent the game UI."""

    def __init__(self, controller):
        super().__init__()
        self.controller = controller

        # ================= WINDOW =================
        self.title("Matching Game")
        self.geometry("1200x700")
        self.configure(bg="#2b2b2b")
        self.resizable(False, False)

        # ================= VARIABLES =================

        self.tk_preview_image = None

        # ================= UI =================
        self._build_menu()
        self._build_header()
        self._build_body()

        # ================= FULLSCREEN =================
        self.is_fullscreen = False

        self.bind("<F11>", lambda e: self.toggle_fullscreen())
        self.bind("<Escape>", lambda e: self.exit_fullscreen())

    # =========================================================
    # MENU
    # =========================================================

    def _build_menu(self):

        menubar = tk.Menu(self)

        # FILE
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Exit", command=self.destroy)
        menubar.add_cascade(label="File", menu=filemenu)

        # VIEW
        viewmenu = tk.Menu(menubar, tearoff=0)

        viewmenu.add_command(
            label="Toggle Full Screen (F11)",
            command=self.toggle_fullscreen
        )

        viewmenu.add_command(
            label="Exit Full Screen (Esc)",
            command=self.exit_fullscreen
        )

        menubar.add_cascade(label="View", menu=viewmenu)

        # HELP
        helpmenu = tk.Menu(menubar, tearoff=0)

        helpmenu.add_command(
            label="About",
            command=lambda: messagebox.showinfo(
                "About",
                "Matching Game"
            )
        )

        menubar.add_cascade(label="Help", menu=helpmenu)

        self.config(menu=menubar)

    # =========================================================
    # HEADER
    # =========================================================

    def _build_header(self):

        header = tk.Frame(
            self,
            bg="#333333",
            height=80
        )

        header.pack(fill="x")

        # LIFE
        self.life_label = tk.Label(
            header,
            text="Life: 0",
            fg="red",
            bg="#333333",
            font=("Arial", 18, "bold")
        )

        self.life_label.pack(
            side="left",
            padx=30,
            pady=20
        )

        # REMAINING
        self.remaining_label = tk.Label(
            header,
            text="Remaining: 5",
            fg="red",
            bg="#333333",
            font=("Arial", 18, "bold")
        )

        self.remaining_label.pack(
            side="left",
            padx=30
        )

        # SCORE
        self.score_label = tk.Label(
            header,
            text="Score: 10",
            fg="red",
            bg="#333333",
            font=("Arial", 18, "bold")
        )

        self.score_label.pack(
            side="left",
            padx=30
        )

        # BROWSE BUTTON
        browse_btn = tk.Button(
            header,
            text="Browse",
            command=self.browse_image,
            bg="#555555",
            fg="white",
            font=("Arial", 12, "bold"),
            width=15
        )

        browse_btn.pack(
            side="right",
            padx=20
        )

    # =========================================================
    # BODY
    # =========================================================

    def _build_body(self):

        body = tk.Frame(
            self,
            bg="#2b2b2b"
        )

        body.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )

        # ================= LEFT PANEL =================

        left_frame = tk.LabelFrame(
            body,
            text="User Input Section",
            fg="red",
            bg="#3a3a3a",
            font=("Arial", 18, "bold"),
            padx=10,
            pady=10
        )

        left_frame.pack(
            side="left",
            expand=True,
            fill="both",
            padx=10
        )

        # IMAGE PREVIEW
        self.preview_canvas = tk.Canvas(
            left_frame,
            width=500,
            height=350,
            bg="black",
            highlightthickness=0
        )

        self.preview_canvas.pack(pady=10)

        # ================= RIGHT PANEL =================

        right_frame = tk.LabelFrame(
            body,
            text="Model Output Section",
            fg="red",
            bg="#3a3a3a",
            font=("Arial", 18, "bold"),
            padx=10,
            pady=10
        )

        right_frame.pack(
            side="right",
            expand=True,
            fill="both",
            padx=10
        )

        # OUTPUT IMAGE
        self.output_canvas = tk.Canvas(
            right_frame,
            width=500,
            height=350,
            bg="black",
            highlightthickness=0
        )

        self.output_canvas.pack(pady=10)

    # =========================================================
    # FULLSCREEN
    # =========================================================

    def toggle_fullscreen(self):

        self.is_fullscreen = not self.is_fullscreen
        self.attributes("-fullscreen", self.is_fullscreen)

    def exit_fullscreen(self):

        self.is_fullscreen = False
        self.attributes("-fullscreen", False)

    # =========================================================
    # IMAGE BROWSING
    # =========================================================

    def browse_image(self):

        file_path = filedialog.askopenfilename(
            filetypes=[
                ("Image files", "*.jpg *.jpeg *.png")
            ]
        )

        if not file_path:
            return

        # self._show_preview(file_path)

        self.controller.on_image_selected(file_path)

    # =========================================================
    # IMAGE DISPLAY
    # =========================================================

    def update_display(self, img):
        self.preview_canvas.delete("all")
        self.preview_canvas.create_image(
            0,
            0,
            anchor="nw",
            image=img
        )

    def _show_preview(self, image_path):

        img = process_image(
            image_path,
            (500, 350)
        )
        self.tk_preview_image = ImageTk.PhotoImage(img)
        self.preview_canvas.delete("all")
        self.preview_canvas.create_image(
            0,
            0,
            anchor="nw",
            image=self.tk_preview_image
        )


def process_image(image_path, size=(224, 224)):
    image = Image.open(image_path).convert("RGB")
    image = image.resize(size)
    return image
