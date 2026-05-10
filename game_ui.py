"""A class to represent the game user interface.
"""
import tkinter as tk

from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import numpy as np

from game_controller import GameController


class GameUI:
    """A class to represent the game UI.
    Attributes:
        root (tk.Tk): The main Tkinter window.
        original_canvas (tk.Canvas): Canvas displaying the original image.
        modified_canvas (tk.Canvas): Canvas displaying the modified image.
        remaining_label (tk.Label): Label showing remaining differences.
        mistakes_label (tk.Label): Label showing current mistakes.
        score_label (tk.Label): Label showing cumulative score.
        controller (GameController): The game controller that connects the UI and game logic.
    """
    root: tk.Tk
    original_canvas: tk.Canvas
    modified_canvas: tk.Canvas
    remaining_label: tk.Label
    mistakes_label: tk.Label
    score_label: tk.Label
    controller: GameController

    def __init__(self, controller: GameController):

        self.controller = controller

        # ================= WINDOW =================
        self.root = tk.Tk()
        self.root.title("Tkinter AI GUI")
        self.root.geometry("1200x700")
        self.root.configure(bg="#2b2b2b")

        # ================= TOP BAR =================
        top_frame = tk.Frame(self.root, bg="#333333", height=80)
        top_frame.pack(fill="x")

        self.mistakes_label = tk.Label(
            top_frame,
            text="Life: 0",
            fg="red",
            bg="#333333",
            font=("Arial", 18, "bold")
        )
        self.mistakes_label.pack(side="left", padx=30, pady=20)

        self.remaining_label = tk.Label(
            top_frame,
            text="Remaining: 5",
            fg="red",
            bg="#333333",
            font=("Arial", 18, "bold")
        )
        self.remaining_label.pack(side="left", padx=30)

        self.score_label = tk.Label(
            top_frame,
            text="Score: 0",
            fg="red",
            bg="#333333",
            font=("Arial", 18, "bold")
        )
        self.score_label.pack(side="left", padx=30)

        # Browse Button
        browse_btn = tk.Button(
            top_frame,
            text="Browse",
            command=self.load_image,
            bg="#555555",
            fg="white",
            font=("Arial", 12, "bold"),
            width=15
        )
        browse_btn.pack(side="right", padx=30)

        # ================= MAIN FRAME =================
        main_frame = tk.Frame(self.root, bg="#2b2b2b")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # ================= LEFT PANEL =================
        left_frame = tk.LabelFrame(
            main_frame,
            text="Original",
            fg="red",
            bg="#3a3a3a",
            font=("Arial", 18, "bold"),
            padx=10,
            pady=10
        )
        left_frame.pack(side="left", expand=True, fill="both", padx=10)

        self.original_canvas = tk.Canvas(
            left_frame,
            width=500,
            height=350,
            bg="black"
        )
        self.original_canvas.pack()

        # ================= RIGHT PANEL =================
        right_frame = tk.LabelFrame(
            main_frame,
            text="Altered",
            fg="red",
            bg="#3a3a3a",
            font=("Arial", 18, "bold"),
            padx=10,
            pady=10
        )
        right_frame.pack(side="right", expand=True, fill="both", padx=10)

        self.modified_canvas = tk.Canvas(
            right_frame,
            width=500,
            height=350,
            bg="black"
        )
        self.modified_canvas.pack()

        # CLICK EVENT
        self.modified_canvas.bind("<Button-1>", self.on_click)

        self.root.mainloop()

    def load_image(self) -> None:
        """Open image and start game"""

        path = filedialog.askopenfilename(
            filetypes=[("Image Files", "*.png *.jpg *.jpeg")]
        )

        if path:
            self.controller.load_image(path)

    def display_images(self, original: np.ndarray, modified: np.ndarray) -> None:
        """Display images on canvases"""

        # Convert numpy arrays to PIL images
        original_image = Image.fromarray(original)
        modified_image = Image.fromarray(modified)

        # Resize
        original_image = original_image.resize((500, 350))
        modified_image = modified_image.resize((500, 350))

        # Convert to Tkinter images
        self.original_photo = ImageTk.PhotoImage(original_image)
        self.modified_photo = ImageTk.PhotoImage(modified_image)

        # Display images
        self.original_canvas.create_image(
            0,
            0,
            anchor="nw",
            image=self.original_photo
        )

        self.modified_canvas.create_image(
            0,
            0,
            anchor="nw",
            image=self.modified_photo
        )

    def update_display(
        self,
        remaining: int,
        mistakes: int,
        score: int,
        found_regions: list,
        revealed_regions: list
    ) -> None:
        """Update game display"""

        self.remaining_label.config(text=f"Remaining: {remaining}")
        self.mistakes_label.config(text=f"Life: {mistakes}")
        self.score_label.config(text=f"Score: {score}")

        # Draw found regions
        for (x, y, w, h) in found_regions:
            self.draw_circle(
                self.modified_canvas,
                x + w // 2,
                y + h // 2,
                25,
                "red"
            )

        # Draw revealed regions
        for (x, y, w, h) in revealed_regions:
            self.draw_circle(
                self.modified_canvas,
                x + w // 2,
                y + h // 2,
                25,
                "blue"
            )

    def show_invalid_image_message(self) -> None:
        """Show invalid image popup"""

        messagebox.showerror(
            "Error",
            "Invalid image selected."
        )

    def show_game_over(self, win: bool) -> None:
        """Show game over popup"""

        if win:
            messagebox.showinfo(
                "Game Over",
                "You Win!"
            )
        else:
            messagebox.showinfo(
                "Game Over",
                "Game Over!"
            )

    def draw_circle(
        self,
        canvas: tk.Canvas,
        x: int,
        y: int,
        radius: int,
        colour: str
    ) -> None:
        """Draw circle"""

        canvas.create_oval(
            x - radius,
            y - radius,
            x + radius,
            y + radius,
            outline=colour,
            width=3
        )

    def on_click(self, event):
        """Handle mouse click"""

        self.controller.handle_click(event.x, event.y)