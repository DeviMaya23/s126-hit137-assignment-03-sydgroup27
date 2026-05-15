import tkinter as tk
from tkinter import filedialog, messagebox
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from PIL import ImageTk
from constants import CANVAS_WIDTH, CANVAS_HEIGHT


class GameUI(ttk.Window):
    """A class to represent the game UI."""

    def __init__(self, controller):
        super().__init__(themename="solar")
        self.controller = controller

        # Window
        self.title("Pictomatchy")
        self.geometry("1200x700")
        self.resizable(False, False)

        # Attributes & Window Variables

        self.tk_original_image_resized = None
        self.tk_altered_image_resized = None
        self.life_var = tk.StringVar(value="0")
        self.remaining_var = tk.StringVar(value="0")
        self.score_var = tk.StringVar(value="0")
        self.status_var = tk.StringVar(
           value="Welcome to Pictomatchy! Start by clicking the Browse button "
                 "(Ctrl+O) to select an image."
        )

        # UI Layout
        self._configure_styles()
        self._build_menu()
        self._build_header()
        ttk.Separator(self, orient="horizontal", bootstyle="secondary").pack(fill="x")
        self._build_status_bar()
        self._build_body()

        self.is_fullscreen = False

        # Event Bindings
        self.bind("<F11>", lambda e: self.toggle_fullscreen())
        self.bind("<Escape>", lambda e: self.exit_fullscreen())
        self.bind("<Control-o>", lambda e: self._on_browse_click())

    def _configure_styles(self):
        """Configures custom styles for the UI elements."""
        style = ttk.Style()
        style.configure("TLabel", font=("", 11))
        style.configure("TButton", font=("", 11))
        style.configure("TLabelframe.Label", font=("", 11, "bold"))

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
                """Pictomatchy - Spot the Difference Game
Upload an image and find 5 altered spots by clicking on the right-side image.

Developed by Sydney Group 27 for S126 HIT137 Assignment 3.
                """
            )
        )

        menubar.add_cascade(label="Help", menu=helpmenu)

        self.config(menu=menubar)

    def _build_header(self):
        """
        Builds the header section of the UI
        which includes the life, remaining,
        and score labels, as well as the browse button."""

        header = ttk.Frame(self)
        header.pack(fill="x", padx=20, pady=(10, 0))

        # Stat cards
        self.life_card = self._build_stat_card(header, "Life", self.life_var, "danger")
        self._build_stat_card(header, "Remaining", self.remaining_var, "warning")
        self.score_card = self._build_stat_card(header, "Score", self.score_var, "success")

        self.browse_btn = ttk.Button(
            header,
            text="📂  Browse",
            bootstyle="primary",
            command=self._on_browse_click,
            width=15
        )

        self.browse_btn.pack(side="right", padx=(10, 0), pady=10)

        self.reveal_btn = ttk.Button(
            header,
            text="👁  Reveal",
            bootstyle="warning",
            command=self._on_reveal_click,
            width=15,
            state="disabled"
        )

        self.reveal_btn.pack(side="right", padx=10, pady=10)

    def _build_stat_card(self, parent, title, var, bootstyle):
        """Helper function to build a stat card with a title and value."""
        card = ttk.Frame(parent, bootstyle=bootstyle, padding=(16, 4))
        card.pack(side="left", padx=(0, 20), pady=10)
        ttk.Label(
            card, text=title, font=("", 11, "bold"),
            bootstyle=f"{bootstyle}-inverse"
        ).pack()
        ttk.Label(
            card, textvariable=var, font=("", 24, "bold"),
            bootstyle=f"{bootstyle}-inverse"
        ).pack()
        return card

    def _flash_card(self, card, original_bootstyle):
        """Flashes a card by temporarily changing its style."""
        card.configure(bootstyle="light")
        for child in card.winfo_children():
            child.configure(bootstyle="light-inverse")

        def revert():
            card.configure(bootstyle=original_bootstyle)
            for child in card.winfo_children():
                child.configure(bootstyle=f"{original_bootstyle}-inverse")

        self.after(400, revert)

    def _build_body(self):
        """Builds the main body of the UI which contains the original and altered image canvases."""
        body = ttk.Frame(
            self,
        )

        body.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )

        left_frame = ttk.Labelframe(
            body,
            text="Original Image",
            bootstyle="info"
        )

        left_frame.pack(
            side="left",
            expand=True,
            fill="both",
            padx=10,
            pady=10
        )

        self.preview_canvas = tk.Canvas(
            left_frame,
            width=CANVAS_WIDTH,
            height=CANVAS_HEIGHT,
            highlightthickness=0
        )

        self.preview_canvas.pack(pady=10)
        self._draw_canvas_placeholder(
            self.preview_canvas,
            "Browse an image to get started\n(Ctrl+O)"
        )

        right_frame = ttk.Labelframe(
            body,
            text="Altered Image",
            bootstyle="info"
        )

        right_frame.pack(
            side="right",
            expand=True,
            fill="both",
            padx=10,
            pady=10
        )

        # OUTPUT IMAGE
        self.output_canvas = tk.Canvas(
            right_frame,
            width=CANVAS_WIDTH,
            height=CANVAS_HEIGHT,
            highlightthickness=0
        )

        self.output_canvas.pack(pady=10)
        self.output_canvas.bind("<Button-1>", self._on_canvas_click)
        self._draw_canvas_placeholder(
            self.output_canvas,
            "Altered image will appear here\nClick to find the differences"
        )

    def _draw_canvas_placeholder(self, canvas, message):
        """Draws a placeholder message on the given canvas."""
        canvas.create_text(
            CANVAS_WIDTH // 2, CANVAS_HEIGHT // 2,
            text=message,
            font=("", 10),
            fill="#888888",
            justify="center"
        )

    def _build_status_bar(self):
        """Builds a status bar frame at the bottom of the window."""
        status_bar = ttk.Frame(
            self,
            bootstyle="secondary",
            height=25
        )

        status_bar.pack(
            fill="x",
            side="bottom"
        )
        status_bar.pack_propagate(False)

        status_label = ttk.Label(
            status_bar,
            textvariable=self.status_var,
            bootstyle="secondary-inverse",
            font=("", 9)
        )

        status_label.pack(
            side="left",
            padx=20,
            pady=3
        )

    def toggle_fullscreen(self):
        self.is_fullscreen = not self.is_fullscreen
        self.attributes("-fullscreen", self.is_fullscreen)

    def exit_fullscreen(self):

        self.is_fullscreen = False
        self.attributes("-fullscreen", False)
        
    # Display functions
    def get_image_bounds(self):
        """Returns the current image bounds as a tuple (x1, y1, x2, y2)."""
        return self.image_bounds

    def load_new_images(self, img, altered_img):
        """Updates both canvases with original and altered images."""
        display_image = ImageTk.PhotoImage(img)
        self.tk_original_image_resized = display_image

        display_altered_image = ImageTk.PhotoImage(altered_img)
        self.tk_altered_image_resized = display_altered_image

        # get rectangle coordinates for image to save & compare with clicks
        img_w, img_h = altered_img.size
        offset_x = 250 - img_w // 2
        offset_y = 0
        self.image_bounds = (
            offset_x, offset_y, offset_x + img_w, offset_y + img_h)

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

    def update_display(
            self, score: int, life: int, remaining: int, game_over: bool
            ) -> None:
        """Updates all relevant UI elements based on the current game state."""

        self.life_var.set(str(life))
        self.remaining_var.set(str(remaining))
        self.score_var.set(str(score))

        if game_over:
            self.reveal_btn.config(state="disabled")
        else:
            self.reveal_btn.config(state="normal")

    def start_loading(self) -> None:
        """Disables browse button and shows loading state on canvases."""
        self.browse_btn.configure(state="disabled")
        for canvas in (self.preview_canvas, self.output_canvas):
            canvas.delete("all")
            self._draw_canvas_placeholder(canvas, "Loading image,\nplease wait...")
        self.update_status_bar("Loading image, please wait...")
        self.update_idletasks()

    def stop_loading(self, restore_placeholders: bool = False) -> None:
        """Re-enables browse button, optionally restoring canvas placeholders on failure."""
        self.browse_btn.configure(state="normal")
        if restore_placeholders:
            self.preview_canvas.delete("all")
            self._draw_canvas_placeholder(
                self.preview_canvas, "Browse an image to get started\n(Ctrl+O)"
            )
            self.output_canvas.delete("all")
            self._draw_canvas_placeholder(
                self.output_canvas, "Altered image will appear here\nClick to find the differences"
            )

    def update_status_bar(self, message: str) -> None:
        """Updates the status bar with the given message."""
        self.status_var.set(message)

    def draw_circle(self, x: int, y: int, color: str):
        """
        Draws a circle on the both canvas.
        Circle size is fixed at 50x50.
        Coordinates (x, y) represent the center of the circle.
        Args:
            x: The x-coordinate of the center of the circle.
            y: The y-coordinate of the center of the circle.
            color: The color of the circle outline.
        """
        self.preview_canvas.create_oval(
            x-25, y-25, x+25, y+25,
            outline=color,
            width=2
        )

        self.output_canvas.create_oval(
            x-25, y-25, x+25, y+25,
            outline=color,
            width=2
        )
    
    def flash_life_card(self):
        """Flashes the life card to indicate an incorrect guess"""
        self._flash_card(self.life_card, "danger")

    def flash_score_card(self):
        """Flashes the score card to indicate a correct guess."""
        self._flash_card(self.score_card, "success")

    def show_popup(self, title: str, message: str, kind: str = "info") -> None:
        """
        Displays a popup message to the user.
        Args:
            title: The title of the popup window.
            message: The message to display in the popup.
            kind: The type of popup to display ("info", "warning", "error").
        """
        match kind:
            case "warning": messagebox.showwarning(title, message)
            case "error": messagebox.showerror(title, message)
            case _: messagebox.showinfo(title, message)

    # Event Handlers
    def _on_canvas_click(self, event):
        """Handle click events on the output canvas and print coordinates."""
        if not self.controller.is_game_in_progress():
            return  # ignore clicks if game is not in progress
        x1, y1, x2, y2 = self.image_bounds
        if not (x1 <= event.x <= x2 and y1 <= event.y <= y2):
            return  # ignore clicks on non image area
        self.controller.handle_click(event.x, event.y)

    def _on_browse_click(self):
        """
        Opens a file dialog for the user to select an image,
        then passes it to controller for processing.
        """

        if self.controller.is_game_in_progress():
            result = messagebox.askyesno("Start New Game", "Are you sure you want to start a new game? Your current progress will be lost (scores are kept).")
            if not result:
                return

        file_path = filedialog.askopenfilename(
            filetypes=[
                ("Image files", "*.jpg *.jpeg *.png *.bmp"),
            ]
        )
        if not file_path:
            return
        self.controller.on_image_selected(file_path)

    def _on_reveal_click(self):
        """
        Reveals all altered regions to the player.
        Ends the game and disables further guesses.
        """
        self.reveal_btn.config(state="disabled")
        self.controller.reveal_altered_regions()
        self.update_status_bar("All altered regions revealed! You can start a new game with the Browse button (Ctrl+O).")
