### Holds and organizes the UI elements (top bar, side bar, export area) 

import tkinter as tk 
from tkinter import ttk
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
        self.grid_columnconfigure(2, weight=1) #Stretch Remainder

        
        #########################TOP-BAR#########################
        self.top_bar = tk.Frame(self, bg="#BF9F8F", height=50)
        self.top_bar.grid(row=0, column=0, columnspan=3, sticky="nsew")
        self.top_bar.grid_propagate(False) # Prevent shrinking if widgets are small

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
       
        #Add UNDO Buttons
        self.undo_button = tk.Button(self.top_bar, text="Undo", state="disabled", command=self.undo_action)
        self.undo_button.grid(row=0, column=0, padx=5, pady=5)
      
        #Add REDO Buttons
        self.redo_button = tk.Button(self.top_bar, text="Redo", state="disabled", command=self.undo_action)
        self.redo_button.grid(row=0, column=1, padx=5, pady=5) 
       

        #########################SIDE-BAR#########################
        self.sidebar = tk.Frame(self, bg="#BF9F8F", width=150)
        self.sidebar.grid(row=1, column=0, sticky="nsew")

        #Sidebar grid configuration
        self.sidebar.grid_rowconfigure(1, weight=1)
        self.sidebar.grid_columnconfigure(0, weight=1)

        #Team Selector
        self.selected_team = tk.StringVar(value="My Team")
        team_dropdown = ttk.OptionMenu(
            self.sidebar,
            self.selected_team,
            "My Team", 
            "My Team",
            "Their Team"
        )
        team_dropdown.grid(row=0, column=0, pady=(10, 5), sticky = "ew")

        #Home and Away Rosters 
        self.rosters = {
            "My Team": ["Point Guard", "Shooting Guard", "Small Forward", "Power Forward", "Center"],
            "Their Team": ["Point Guard", "Shooting Guard", "Small Forward", "Power Forward", "Center"],
        }

        #Player list container
        self.player_list_frame = tk.Frame(self.sidebar, bg="#BF9F8F")
        self.player_list_frame.grid(row=1, column=0, sticky="nsew", pady=(10,10))

        #Subframe for holding default player buttons 
        self.player_buttons = []
        self.selected_player_button = None #track selection

        #Add ADD PLAYER button 
        self.add_button = tk.Button(self.sidebar, text="Add", command=self.add_player_dialog)
        self.add_button.grid(row=2, column=0, pady=5, sticky="ew")
        
        #Add REMOVE PLAYER button
        self.remove_button = tk.Button(self.sidebar, text="Remove", state="disabled", command=self.remove_selected_player)
        self.remove_button.grid(row=3, column=0, pady=5, sticky="ew")

        #Populate initial list and team switch 
        self.refresh_player_list()
        self.selected_team.trace_add("write", lambda *_: self.on_team_changes())

    
        #########################COURT-DISPLAY####################
        self.canvas = CourtCanvas(self, court_type=self.court_type)
        self.canvas.grid(row=1, column=1, sticky="nsew")
        ##########################################################

        

 