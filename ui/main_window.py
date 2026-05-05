# will contains all the ui main window
# will contains all the ui main window
import tkinter as tk
from tkinter import filedialog
from .components import create_button
from config.settings import AVAILABLE_MODELS

# create a main window class
class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("AI Image Classification")
        
        self.label = tk.Label(self, text="Select an image to classify")
        self.label.pack(pady=10)

        self.upload_button = create_button(self, "Upload Image", self.load_image)
        self.upload_button.pack(pady=10)



    def load_image(self):
        print("load image is clicked")