### Holds and organizes the UI elements (top bar, side bar, export area) 
### CourtCanvas is now part of court_frame

import tkinter as tk 
from src.user_interface.court_canvas import CourtCanvas

class CourtFrame(tk.Frame):
    def __init__(self, master, court_type):
        super().__init__(master)
        self.court_type = court_type

        #Layout grid of 3 columns (sidebar, canvas, and export) and 2 rows (top bar and content)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(1, weight=1)

        #PLACEHOLDER for top bar
        self.top_bar = tk.Frame(self, bg="lightgrey", height=50)
        self.top_bar.grid(row=0, column=0, columnspan=3, sticky="nsew")

        #PLACEHOLDER for side bar
        self.sidebar = tk.Frame(self, bg="pink", width=150)
        self.sidebar.grid(row=1, column=0, sticky="nsew")

        #PLACEHOLDER for court display
        self.canvas = CourtCanvas(self, court_type)
        self.canvas.grid(row=1, column=1, sticky="nsew")

        #PLACEHOLDER for Export Feature Panel
        self.export_panel = tk.Frame(self, bg="lightgrey", width=150)
        self.export_panel.grid(row=1, column=2, sticky="nsew")
        