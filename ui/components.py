import tkinter as tk

# create a button function
def create_button(parent, text, command):
    button = tk.Button(parent, text=text, command=command)
    return button