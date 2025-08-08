# Holds and organizes the UI elements (top bar, side bar, export area) 
import json, csv
import tkinter as tk 
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter import simpledialog, messagebox
from PIL import Image, ImageDraw
from src.user_interface.court_canvas import CourtCanvas ### CourtCanvas is now part of court_frame
from src.dialogs.player_dialogs import prompt_add_player, confirm_remove_player
from src.logic.zoning import get_zone

class CourtFrame(tk.Frame):
    def __init__(self, master, court_type):
        super().__init__(master)
        self.court_type = court_type

        #For court clickability handoff from court_canvas.py
        self.history = []
        self.redo_stack = []

        # Layout grid of 3 columns (sidebar, canvas, and export) and 2 rows (top bar and content)
        self.grid_rowconfigure(0, weight=0) # Top Bar 
        self.grid_rowconfigure(1, weight=1) # Main Content
        
        self.grid_columnconfigure(0, weight=0) #Side Bar
        self.grid_columnconfigure(1, weight=1) #Court Canvas
        self.grid_columnconfigure(2, weight=0) #Export Panel
        self.grid_columnconfigure(2, weight=1) #Stretch Remainder
        
        #Colors for player buttons
        self.player_btn_bg = "#e9e9e9"
        self.player_btn_selected_bg = "#ffd966"
        self.player_buttons = []
        self.selected_player_button = None

        #########################TOP-BAR#########################
        self.top_bar = tk.Frame(self, bg="#BF9F8F", height=50)
        self.top_bar.grid(row=0, column=0, columnspan=3, sticky="nsew")
        self.top_bar.grid_propagate(False) # Prevent shrinking if widgets are small
        
        #Provides room for middle section 
        self.top_bar.grid_columnconfigure(0,weight=0) # Left cluster
        self.top_bar.grid_columnconfigure(1,weight=1) # Center (Quarter Button) stretches
        self.top_bar.grid_columnconfigure(2,weight=0) # Game cluster
        self.top_bar.grid_columnconfigure(3,weight=0) # Export cluster 
        
        #Creates space for left section (undo/redo)//Adding UNDO REDO 
        left = tk.Frame(self.top_bar, bg="#BF9F8F")
        left.grid(row=0, column=0,padx=8,pady=6, sticky="w")
        self.undo_button = tk.Button(left, text="Undo", state="disabled", command=self.undo_action, width=6)
        self.undo_button.grid(row=0,column=1,padx=4)
        self.redo_button = tk.Button(left, text="Redo", state="disabled", command=self.redo_action, width=6)
        self.redo_button.grid(row=0,column=2,padx=4)
        
        #Creates space for center section (quarter buttons + end game)
        center = tk.Frame(self.top_bar,bg="#BF9F8F")
        center.grid(row=0, column=1,padx=8, pady=6, sticky="n")
        center.grid_columnconfigure(0,weight=1)
        tk.Label(center, text="Quarter").grid(row=0, column=0,columnspan=5,pady=(0,4))
        
        #Adding GAME QUARTER buttons
        self.current_quarter = tk.StringVar(value="Q1")
        self.quarter_buttons = {}

        quarters = ["Q1","Q2","Q3","Q4"]
        for i, q in enumerate(quarters):
            btn = tk.Button(center, text=q, width=5,command=lambda v=q: self.on_quarter_change(v))
            btn.grid(row=1, column=i, padx=3)
            self.quarter_buttons[q] = btn 
              
        #Adding END GAME button 
        tk.Button(center, text="End Game", width=10,command=self.end_game).grid(row=1,column=4,padx=(10,0))
               
        #Add SAVE / RESET Button 
        game = tk.Frame(self.top_bar,bg="#BF9F8F")
        game.grid(row=0,column=2,padx=8,pady=6,sticky="e")
        tk.Button(game, text="Reset", width=7, command=self.reset_session).grid(row=1, column=0,padx=4, pady=(4,0))
        
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
        self.selected_team.trace_add("write", lambda *_: self.on_team_change())

    

        #########################COURT-DISPLAY####################
        self.canvas = CourtCanvas(self, court_type=self.court_type, on_shot=self.record_shot)
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
            if b.winfo_exists():
                b.destroy()
        self.player_buttons.clear()

        roster = self.rosters[self.selected_team.get()]
        for idx, name in enumerate(roster):
            btn = tk.Button(
                self.player_list_frame,
                text=name,
                bg=self.player_btn_bg,
                relief="raised",
            )
            btn.config(command=lambda b=btn: self.select_player(b))
            btn.grid(row=idx, column=0, sticky="ew", pady=2)
            self.player_buttons.append(btn)

        if not (self.selected_player_button and self.selected_player_button.winfo_exists()):
            self.selected_player_button=None 
            self.remove_button.config(state="disabled")


    def select_player(self, button): 
        for b in self.player_buttons: 
            if b.winfo_exists():
                b.config(bg=self.player_btn_bg, relief="raised")
        #set selection
        self.selected_player_button = button 
        button.config(bg=self.player_btn_selected_bg, relief="sunken")
        #allow removal
        self.remove_button.config(state="normal")      


    def add_player_dialog(self):
        name = prompt_add_player(self)
        if name: 
            self.add_player(name.strip())
    

    def add_player(self, name): 
        if not name: 
            return 
        roster = self.rosters[self.selected_team.get()]
        roster.append(name)
        self.refresh_player_list() 


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
    def undo_action(self):
        if not self.history: 
            return
        evt = self.history.pop()
        self.redo_stack.append(evt)
        
        c = getattr(self.canvas, "canvas", None)
        if c is not None:
            items = c.find_all()
            if items: 
                c.delete(items[-1])

        self.undo_button.config(state=("normal" if self.history else "disabled"))
        self.redo_button.config(state=("normal" if self.redo_stack else "disabled"))
       

    def redo_action(self):
        if not self.redo_stack: 
            return 
        
        evt = self.redo_stack.pop()
        self.history.append(evt)
        
        #redraw dot
        c = getattr(self.canvas, "canvas", None)
        if c is not None:
            r =4
            c.create_oval(
                evt["x"]-r, evt["y"]-r, 
                evt["x"]+r, evt["y"]+r, 
                fill="d9534f", outline="",
                tags=("shot"),
            )
        self.undo_button.cofig(state=("normal" if self.history else "disabled"))
        self.redo_button.cofig(state=("normal" if self.redo_stack else "disabled"))


    def on_quarter_change(self,q):
        self.current_quarter.set(q)
        for name, btn in self.quarter_buttons.items():
            if name == q:
                btn.config(relief="sunken")
            else: 
                btn.config(relief="raised")
        print(f"Quarter -> {q}")


    def end_game(self):
        if messagebox.askyesno("End Game", "End the game and clear the current session?"):
            self.export_json()
            self.reset_session()

    def save_session(self):
        if not self.history:
            messagebox.showinfo("Save", "Nothing to save.")
            return
        path = fd.asksaveasfilename(
            title="Save Session (JSON)",
            defaultextension=".json",
            filetypes=[("JSON files", "*json")]
        )  
        if not path:
            return
        payload = {
            "meta": {
                "team_selected": self.selected_team.get(),
                "court_type": self.court_type,
            },
            "events": self.history,
        }
        with open(path,"w",encoding="utf-8") as f:
            json.dump(payload, f, indent=2)
        messagebox.showinfo("Saved", f"Session saved to:\n{path}")

    def reset_session(self): 
        self.history.clear()
        self.redo_stack.clear()
        inner_canvas = getattr(self.canvas, "canvas", None)
        if inner_canvas is not None:
            inner_canvas.delete("shot")
        self.undo_button.config(state="disabled")
        self.redo_button.config(state="disabled")

    def export_image(self): 
        inner_canvas = getattr(self.canvas, "canvas", None)
        if inner_canvas is None or not hasattr(self.canvas,"image_path"):
            messagebox.showerror("Export Image", "Canvas Not Ready")
            return
        out_path = fd.asksaveasfilename(
            title="Export Court Image",
            defaultextension = ".png",
            filetypes=[("PNG Image", "*.png")]
            )
        if not out_path:
            return
    
        base = Image.open(self.canvas.image_path).convert("RBGA")
        width = inner_canvas.winfo_width()
        height = inner_canvas.winfo_height()
        if width and height: 
            base = base.resize((width, height), Image.LANCZOS)

        draw = ImageDraw.Draw(base)
        r = 4
        for evt in self.history:
            x, y = evt["x"], evt ["y"]
            draw.ellipse((x - r, y - r, x + r, y + r), fill="#d9534f", outline=None)

        base.save(out_path, "PNG")
        messagebox.showinfo("Export Image", f"Image exported to:\n{out_path}")


    def export_json(self): 
        if not self.history:
            messagebox.showinfo("Export JSON", "No events to export.")
            return
        path = fd.asksaveasfilename(
            title="Export JSON",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json")],
        )
        if not path:
            return
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.history, f, indent=2)
        messagebox.showinfo("Export JSON", f"Events exported to:\n{path}")
        

    def export_csv(self): 
        if not self.history:
            messagebox.showinfo("Export CSV", "No events to export.")
            return 
        path = fd.asksaveasfilename(
            title="Export CSV",
            defaultextension=".csv",
            filetypes=[("CSV Files", "*.csv")]
        )
        if not path:
            return
        
        fieldnames = ["x","y","player","team","quarter"]
        with open(path, "w", newline="",encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for evt in self.history:
                writer.writerow({k: evt.get(k, "") for k in fieldnames})
        messagebox.showinfo("Export CSV", f"CSV exported to:\n {path}")


    def record_shot(self,x,y):
        player = self.selected_player_button["text"] if self.selected_player_button else None
        team = self.selected_team.get()
        quarter = self.current_quarter.get()
        
        #normalize click to 0..1 based on canvas size
        width = self.canvas.canvas.winfo_width()
        height = self.canvas.canvas.winfo_height()
        nx, ny = x / width, y / height

        #determine zone + points 
        zone, points = get_zone(nx, ny, court_type=self.court_type)
        
        evt = {
            "x": x, "y":y, 
            "nx": nx, "ny": ny,
            "player": player, 
            "team": team, 
            "quarter": quarter,
            "points": points,
            }
        self.history.append(evt)
        self.redo_stack.clear()
        print(f"SHOT: {evt}")
    