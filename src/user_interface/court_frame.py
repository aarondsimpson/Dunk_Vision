### Holds and organizes the UI elements (top bar, side bar, export area) 

import tkinter as tk 
from src.user_interface.court_canvas import CourtCanvas ### CourtCanvas is now part of court_frame

class CourtFrame(tk.Frame):
    def __init__(self, master, court_type):
        super().__init__(master)
        self.court_type = court_type

        #Layout grid of 3 columns (sidebar, canvas, and export) and 2 rows (top bar and content)
        self.grid_rowconfigure(0, weight=0) # Top Bar 
        self.grid_rowconfigure(1, weight=1) # Main Content
        
        self.grid_columnconfigure(0, weight=0) #Side Bar
        self.grid_columnconfigure(1, weight=1) #Court Canvas
        self.grid_columnconfigure(2, weight=0) #Export Panel


        #########################TOP-BAR#########################
        self.top_bar = tk.Frame(self, bg="lightgrey", height=50)
        self.top_bar.grid(row=0, column=0, columnspan=3, sticky="nsew")
        #Adding GAME QUARTER buttons
        for i, q in enumerate(["Q1","Q2","Q3","Q4"]):
            btn = tk.Button(self.top_bar, text=q, width=6)
            btn.grid(row=0, column=i, padx=2)
        #Adding END GAME button 
        end_btn = tk.Button(self.top_bar,text="End Game", width=6)
        end_btn.grid(row=0, column=4, padx=10)
        #Add SAVE Button 
        save_btn = tk.Button(self.top_bar, text="Save", width=6)
        save_btn.grid(row=0,column=5, padx=2)
        #Add RESET Button 
        reset_btn = tk.Button(self.top_bar, text="Reset", width=6)
        reset_btn.grid(row=0,column=6, padx=2)
        #Add EXPORT Buttons
        for i, export_type in enumerate(["Image", "JSON", "CSV"]):
            export_btn = tk.Button(self.top_bar, text=export_type, width=6)
            export_btn.grid(row=0, column=7+i, padx=2)
        

        #########################SIDE-BAR#########################
        self.sidebar = tk.Frame(self, bg="pink", width=150)
        self.sidebar.grid(row=1, column=0, sticky="nsew")



        #########################COURT-DISPLAY#########################
        self.canvas = CourtCanvas(self, court_type=self.court_type)
        self.canvas.grid(row=1, column=1, sticky="nsew")


        

 