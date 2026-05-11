import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import ImageTk, Image
from constants import CANVAS_WIDTH, CANVAS_HEIGHT


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

        self.tk_original_image_resized = None
        self.tk_altered_image_resized = None
        self.life_var = tk.StringVar(value="Life: 0")
        self.remaining_var = tk.StringVar(value="Remaining: 0")
        self.score_var = tk.StringVar(value="Score: 0")

        # ================= UI =================
        self._build_menu()
        self._build_header()
        self._build_body()

        # ================= FULLSCREEN =================
        self.is_fullscreen = False

        self.bind("<F11>", lambda e: self.toggle_fullscreen())
        self.bind("<Escape>", lambda e: self.exit_fullscreen())

    def _build_menu(self):
        """Builds the menu bar with File, View, and Help options."""
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

    def _build_header(self):
        """
        Builds the header section of the UI
        which includes the life, remaining, 
        and score labels, as well as the browse button."""

        header = tk.Frame(
            self,
            bg="#333333",
            height=80
        )

        header.pack(fill="x")

        # LIFE
        self.life_label = tk.Label(
            header,
            textvariable=self.life_var,
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
            textvariable=self.remaining_var,
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
            textvariable=self.score_var,
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
            text="Original Image",
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
            width=CANVAS_WIDTH,
            height=CANVAS_HEIGHT,
            bg="black",
            highlightthickness=0
        )

        self.preview_canvas.pack(pady=10)

        # ================= RIGHT PANEL =================

        right_frame = tk.LabelFrame(
            body,
            text="Altered Image",
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
            width=CANVAS_WIDTH,
            height=CANVAS_HEIGHT,
            bg="black",
            highlightthickness=0
        )

        self.output_canvas.pack(pady=10)
        self.output_canvas.bind("<Button-1>", self._on_canvas_click)

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
        """
        Opens a file dialog for the user to select an image,
        then passes it to controller for processing.
        """
        file_path = filedialog.askopenfilename(
            filetypes=[
                ("Image files", "*.jpg *.jpeg *.png")
            ]
        )
        if not file_path:
            return
        self.controller.on_image_selected(file_path)

    # =========================================================
    # DISPLAY
    # =========================================================

    def load_new_images(self, img, altered_img):
        """Updates the preview canvas with the new image."""
        display_image = ImageTk.PhotoImage(img)
        self.tk_original_image_resized = display_image

        display_altered_image = ImageTk.PhotoImage(altered_img)
        self.tk_altered_image_resized = display_altered_image

        # get rectangle coordinates for image to save & compare with clicks later
        img_w, img_h = altered_img.size
        offset_x = 250 - img_w // 2
        offset_y = 0
        self.image_bounds = (offset_x, offset_y, offset_x + img_w, offset_y + img_h)

        # update canvas image
        self.preview_canvas.delete("all")
        self.preview_canvas.create_image(
            250,
            0,
            anchor="n",
            image=display_image
        )
        self.output_canvas.delete("all")
        self.output_canvas.create_image(
            250,
            0,
            anchor="n",
            image=display_altered_image
        )
        

    def update_display(self, score: int, life: int, remaining: int, found_regions: list, revealed_regions: list, revealed: bool) -> None:
        self.life_var.set(f"Life: {life}")
        self.remaining_var.set(f"Remaining: {remaining}")
        self.score_var.set(f"Score: {score}")

    # =========================================================
    # EVENT HANDLERS
    # =========================================================

    def _on_canvas_click(self, event):
        """Handle click events on the output canvas and print coordinates."""
        print(f"Canvas clicked at coordinates: ({event.x}, {event.y})")

        x1, y1, x2, y2 = self.image_bounds
        if not (x1 <= event.x <= x2 and y1 <= event.y <= y2):
            return  # ignore clicks on non image area
        self.controller.handle_click(event.x - x1, event.y - y1) # adjust click coordinates to be relative to the image
    
    def draw_circle(self, x: int, y: int, color: str):
        self.output_canvas.create_oval(
            x-25, y-25, x+25, y+25,
            outline=color,
            width=2
        )