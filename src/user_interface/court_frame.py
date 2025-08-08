# Holds and organizes the UI elements (top bar, side bar, export area) 

import tkinter as tk 
from tkinter import ttk, simpledialog, messagebox
from src.user_interface.court_canvas import CourtCanvas ### CourtCanvas is now part of court_frame
from src.dialogs.player_dialogs import prompt_add_player, confirm_remove_player

class CourtFrame(tk.Frame):
    def __init__(self, master, court_type):
        super().__init__(master)
        self.court_type = court_type

        # Layout grid of 3 columns (sidebar, canvas, and export) and 2 rows (top bar and content)
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
        
        #Provides room for middle section 
        self.top_bar.grid_columnconfigure(0,weight=0) # Left cluster
        self.top_bar.grid_columnconfigure(1,weight=1) # Center (Quarter Button) stretches
        self.top_bar.grid_columnconfigure(2,weight=0) # Game cluster
        self.top_bar.grid_columnconfigure(3,weight=0) # Export cluster 
        
        #Creates space for left section (undo/redo)
        left = tk.Frame(self.top_bar, bg="#BF9F8F")
        left.grid(row=0, column=0,padx=8,pady=6, sticky="w")
        self.undo_button = tk.Button(left, text="Undo", state="disabled", command=self.undo_action, width=6)
        self.undo_button.grid(row=0,column=1,padx=4)
        self.redo_button = tk.Button(left, text="Redo", state="disabled", command=self.redo_action, width=6)
        self.redo_button.grid(row=0,column=1,padx=4)
        
        #Creates space for center section (quarter buttons + end game)
        center = tk.Frame(self.top_bar,bg="#BF9F8F")
        center.grid(row=0, column=1,padx=8, pady=6, sticky="n")
        center.grid_columnconfigure(0,weight=1)
        tk.Label(center, text="Quarter").grid(row=0, column=0,columnspan=5,pady=(0,4))
        
        #Adding GAME QUARTER buttons
        quarters = ["Q1","Q2","Q3","Q4"]
        for i, q in enumerate(quarters):
            tk.Button(center, text=q,width=5,command=lambda v=q: self.on_quarter_change(v)).grid(row=1, column=i, padx=3)
              
        #Adding END GAME button 
        tk.Button(center, text="End Game", width=10,command=self.end_game).grid(row=1,column=4,padx=(10,0))
               
        #Add SAVE / RESET Button 
        game = tk.Frame(self.top_bar,bg="#BF9F8F")
        game.grid(row=0,column=2,padx=8,pady=6,sticky="e")
        tk.Button(game, text="Reset", width=7, command=self.save_session).grid(row=1, column=0,padx=4, pady=(4,0))
        
        #Add EXPORT Buttons
        export = tk.Frame(self.top_bar, bg="#BF9F8F")
        export.grid(row=0,column=3,padx=8,pady=6,sticky="e")
        for c in range(3):
            export.grid_columnconfigure(c,weight=1, uniform="Export")
        btn_img = tk.Button(export,text="Image", width=7, command=self.export_image)
        btn_json = tk.Button(export,text="JSON", width=7, command=self.export_json)
        btn_csv = tk.Button(export,text="CSV", width=7, command=self.export_csv)
        btn_img.grid(row=0,column=0,padx=3)
        btn_json.grid(row=0,column=1,padx=3)
        btn_csv.grid(row=0,column=2,padx=3) 
            

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
        

        #########################HELPER-FUNCTIONS####################     
    #when a different team (home/away) is selected, the current player deselects, the remove button becomes unclickable, and the team list refreshes 
    def on_team_change(self): 
        self.selected_player_button = None
        self.remove_button.config(state="disabled")
        self.refresh_player_list() 

    #When the player list refreshes, existing player buttons are removed and the correct roster is rebuilt
    def refresh_player_list(self):
        for b in self.player_buttons: 
            b.destroy()
        self.player_buttons.clear()

        roster = self.rosters[self.selected_team.get()]
        for idx, name in enumerate(roster):
            btn = tk.Button(self.player_list_frame, text=name, anchor="w")
            btn.grid(row=idx, column=0, sticky="ew", pady=2)
            btn.bind("<Button-1>", lambda e, b=btn: self.select_player(b))
            self.player_buttons.append(btn)

    #
    def select_player(self, button): 
        for b in self.player_buttons: 
            b.config(relief="raised")
        button.config(relief="sunken")
        self.selected_player_button = button
        self.remove_button.config(state="normal")


    def add_player_dialog(self):
        name = prompt_add_player(self)
        if name: 
            self.add_player(name.strip())
    #
    def add_player(self, name): 
        if not name: 
            return 
        roster = self.rosters[self.selected_team.get()]
        roster.append(name)
        self.refresh_player_list() 

    #
    def remove_selected_player(self):
        if not self.selected_player_button: 
            return
        name = self.selected_player_button["text"]
        if confirm_remove_player(self,name):
            roster = self.rosters[self.selected_team.get()]
            if name in roster: 
                roster.remove(name)
            self.selected_player_button = None
            self.remove_button.config(state="disabled")
            self.refresh_player_list()

    #Placeholders for top bar buttons
    def undo_action(self): print("Undo (todo)")
    def redo_action(self): print("Redo (todo)")
    def on_quarter_change(self,q): print(f"Quarter -> {q}")
    def end_game(self): print("End Game (todo)")
    def save_session(self): print("Save Session (todo)")
    def reset_session(self): print("Reset Session (todo)")
    def export_image(self): print("Export Image (todo)")
    def export_json(self): print("Export JSON (todo)")
    def export_csv(self): print("Export CSV (todo)")
    