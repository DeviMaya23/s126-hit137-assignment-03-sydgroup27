# will contains all the ui components
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog


def create_button(parent, text, command, width=12, style=None):
    """Create a primary button with optional ttk style."""
    if style:
        button = ttk.Button(parent, text=text, command=command, style=style, width=width)
    else:
        button = ttk.Button(parent, text=text, command=command, width=width)
    return button


def create_label(parent, text, anchor="w"):
    """Create a simple label."""
    label = ttk.Label(parent, text=text, anchor=anchor)
    return label


def create_labeled_frame(parent, text):
    """Create a ttk labeled frame used to group widgets."""
    frame = ttk.LabelFrame(parent, text=text, padding=(10, 6))
    return frame


def create_radio(parent, text, value, variable):
    """Create a ttk radio button bound to a `tk.StringVar`."""
    radio = ttk.Radiobutton(parent, text=text, value=value, variable=variable)
    return radio


def create_text_box(parent, height=8, width=50):
    """Create a read/write text box for logs or prompts."""
    text = tk.Text(parent, height=height, width=width)
    return text


def create_listbox(parent, height=6, width=40):
    listbox = tk.Listbox(parent, height=height, width=width)
    return listbox


def create_image_canvas(parent, width=300, height=300):
    """Create a canvas to preview images."""
    canvas = tk.Canvas(parent, width=width, height=height, bg="#ffffff", highlightthickness=1, highlightbackground="#cccccc")
    return canvas

def save_image(image):
    """Open save dialog and save PIL image"""
    file_path = filedialog.asksaveasfilename(
        defaultextension=".png",
        filetypes=[("PNG files", "*.png"), ("All files", "*.*")]
    )
    if file_path:
        image.save(file_path)