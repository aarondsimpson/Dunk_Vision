import tkinter as tk
from src.user_interface.court_canvas import CourtCanvas

class DunkVisionApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Dunk Vision")
        self.resizable(True,True)

        court_type = self.prompt_user_for_court_type()
        self.build_ui(court_type)


    def prompt_user_for_court_type(self):
        from tkinter import simpledialog

        #PLACEHOLDER: Prompts the user to select court size
        court_type = simpledialog.askstring(
            "Select Court Type",
            "Enter 'Half' or 'Full':",
            initialvalue="half",
        )

        #If the user does not make a selection, half is the default selection
        if court_type not in ("half", "full"):
            court_type = "half"
        return court_type

    def build_ui(self,court_type):
        #placeholder layout
        self.grid_rowconfigure(0,weight=1)
        self.grid_columnconfigure(0,weight=1)

        self.court_canvas = CourtCanvas(self, court_type=court_type)
        self.court_canvas.grid(row=0, column=0, sticky="nsew")