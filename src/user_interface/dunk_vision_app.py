#Coordinates GUI window (size, title, layout)

import tkinter as tk
from tkinter import messagebox
from src.user_interface.court_frame import CourtFrame

class DunkVisionApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Dunk Vision")
        self.resizable(True,True)

        #Global button styling for the whole app
        self.option_add("*Button.Background","#f0f0f0")
        self.option_add("*Button.Foreground", "#000000")
        self.option_add("*Button.ActiveBackground","#d9d9d9")
        self.option_add("*Button.ActiveForeground", "#000000")
        
        #Prepping for warning dialog box when app is closed 
        self.protocol("WM_DELETE_WINDOW", self.on_app_close)

        court_type = self.prompt_user_for_court_type()
        self.build_ui(court_type)

    def prompt_user_for_court_type(self):
        from tkinter import simpledialog

        #PLACEHOLDER: Prompts the user to select court size
        court_type = simpledialog.askstring(
            title="Court Selection",
            prompt="Enter 'Half' or 'Full':",
            parent=self,
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

        self.court_frame = CourtFrame(self, court_type=court_type)
        self.court_frame.grid(row=0, column=0, sticky="nsew")

    def on_app_close(self): 
        if messagebox.askyesno("Quit", "Unsaved work will be lost. Quit?"):
            self.destroy()


