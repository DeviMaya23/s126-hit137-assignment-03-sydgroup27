

import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import ImageTk

from config.settings import AVAILABLE_MODELS
from models.model_factory import get_model
from utils.image_utils import process_image


class MainWindow(tk.Tk):

    def __init__(self):
        super().__init__()

        # ================= WINDOW =================
        self.title("Tkinter AI GUI")
        self.geometry("1200x700")
        self.configure(bg="#2b2b2b")
        self.resizable(False, False)

        # ================= VARIABLES =================
        self.selected_model_key = tk.StringVar(value="vit")
        self.input_mode = tk.StringVar(value="image")

        self.loaded_model = None
        self.current_image_path = None
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

        # MODELS
        modelmenu = tk.Menu(menubar, tearoff=0)

        modelmenu.add_command(
            label="Load Model",
            command=self.load_model
        )

        menubar.add_cascade(label="Models", menu=modelmenu)

        # HELP
        helpmenu = tk.Menu(menubar, tearoff=0)

        helpmenu.add_command(
            label="About",
            command=lambda: messagebox.showinfo(
                "About",
                "Tkinter AI GUI"
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

        # MODEL COMBOBOX
        self.model_combo = tk.StringVar(value="ViT (Classify)")

        model_dropdown = tk.OptionMenu(
            header,
            self.model_combo,
            "ViT (Classify)",
            "DeiT (Classify)",
            "ResNet (Classify)",
            "Stable Diffusion (text2image)"
        )

        model_dropdown.config(
            bg="#555555",
            fg="white",
            font=("Arial", 11),
            width=25
        )

        model_dropdown.pack(
            side="right",
            padx=10
        )

        # LOAD MODEL BUTTON
        load_btn = tk.Button(
            header,
            text="Load Model",
            command=self.load_model,
            bg="#444444",
            fg="white",
            font=("Arial", 11, "bold"),
            width=12
        )

        load_btn.pack(
            side="right",
            padx=10
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

        # RADIO BUTTONS
        radio_frame = tk.Frame(
            left_frame,
            bg="#3a3a3a"
        )

        radio_frame.pack(anchor="w")

        tk.Radiobutton(
            radio_frame,
            text="Text",
            variable=self.input_mode,
            value="text",
            bg="#3a3a3a",
            fg="white",
            selectcolor="#444444",
            font=("Arial", 11)
        ).pack(side="left", padx=10)

        tk.Radiobutton(
            radio_frame,
            text="Image",
            variable=self.input_mode,
            value="image",
            bg="#3a3a3a",
            fg="white",
            selectcolor="#444444",
            font=("Arial", 11)
        ).pack(side="left")

        # TEXT BOX
        self.prompt_box = tk.Text(
            left_frame,
            bg="#1e1e1e",
            fg="white",
            insertbackground="white",
            font=("Arial", 12),
            height=8
        )

        self.prompt_box.pack(
            fill="x",
            pady=10
        )

        # BUTTONS
        button_frame = tk.Frame(
            left_frame,
            bg="#3a3a3a"
        )

        button_frame.pack(anchor="w", pady=10)

        run_btn = tk.Button(
            button_frame,
            text="Run Model",
            command=self.run_model,
            bg="#008CBA",
            fg="white",
            font=("Arial", 11, "bold"),
            width=15
        )

        run_btn.pack(side="left", padx=5)

        clear_btn = tk.Button(
            button_frame,
            text="Clear",
            command=self.clear_output,
            bg="#666666",
            fg="white",
            font=("Arial", 11, "bold"),
            width=15
        )

        clear_btn.pack(side="left", padx=5)

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

        # OUTPUT BOX
        self.output_box = tk.Text(
            right_frame,
            bg="#1e1e1e",
            fg="white",
            insertbackground="white",
            font=("Arial", 12),
            height=10
        )

        self.output_box.pack(
            fill="x",
            pady=10
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
    # MODEL FUNCTIONS
    # =========================================================

    def _parse_model_key(self):

        selection = self.model_combo.get()

        if "deit" in selection.lower():
            return "deit"

        if "resnet" in selection.lower():
            return "resnet"

        if "diffusion" in selection.lower():
            return "text2image"

        return "vit"

    def load_model(self):

        model_key = self._parse_model_key()

        try:
            self.loaded_model = get_model(model_key)

            self._append_output(
                f"Loaded model: {model_key}"
            )

        except Exception as exc:

            self._append_output(
                f"Error loading model: {exc}"
            )

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

        self.current_image_path = file_path

        self._show_preview(file_path)

        self._append_output(
            f"Selected image: {file_path}"
        )

    # =========================================================
    # RUN MODEL
    # =========================================================

    def run_model(self):

        if not self.loaded_model:

            self._append_output(
                "Please load a model first."
            )

            return

        model_key = self._parse_model_key()

        # TEXT TO IMAGE
        if model_key == "text2image":

            prompt = self.prompt_box.get(
                "1.0",
                tk.END
            ).strip()

            if not prompt:

                self._append_output(
                    "Please enter a prompt."
                )

                return

            image = self.loaded_model.predict(prompt)

            self.tk_preview_image = ImageTk.PhotoImage(
                image.resize((500, 350))
            )

            self.output_canvas.delete("all")

            self.output_canvas.create_image(
                0,
                0,
                anchor="nw",
                image=self.tk_preview_image
            )

            self._append_output(
                "Generated image from prompt."
            )

            return

        # IMAGE CLASSIFICATION
        if self.input_mode.get() == "image":

            if not self.current_image_path:

                self._append_output(
                    "Please browse and select an image."
                )

                return

            results = self.loaded_model.predict(
                self.current_image_path
            )

        else:

            self._append_output(
                "Text mode not supported for classification."
            )

            return

        if results:
            self._render_predictions(results)

    # =========================================================
    # OUTPUT FUNCTIONS
    # =========================================================

    def clear_output(self):

        self.output_box.delete("1.0", tk.END)

    def _append_output(self, text):

        self.output_box.insert(
            tk.END,
            text + "\n"
        )

        self.output_box.see(tk.END)

    # =========================================================
    # IMAGE DISPLAY
    # =========================================================

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

    # =========================================================
    # PREDICTIONS
    # =========================================================

    def _render_predictions(self, results):

        self._append_output("Predictions:")

        for pred in results:

            label = pred.get("label")
            score = pred.get("score")

            self._append_output(
                f"- {label}: {score:.4f}"
            )