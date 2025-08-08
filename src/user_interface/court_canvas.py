###Loads the Court Image

import tkinter as tk
import os
from PIL import Image, ImageTk 
from pathlib import Path

#Creating a reusable class that sets up for full court/half court selection
class CourtCanvas(tk.Frame):
    
    def __init__(self, master, court_type="half"):
        super().__init__(master)
        court = (court_type or "half").strip().lower()
        if court not in ("half", "full"):
            court = "half" 
        self.on_shot = on_shot
        self.court_type = court
        

        assets_dir = self._find_assets_dir()
        
        img_base = f"{self.court_type}_court"
        self.image_path = None
        
        for ext in (".png", ".jpg", ".jpeg"):
            candidate = assets_dir / (img_base + ext)
            if candidate.exists():
                self.image_path = candidate
                break
        if self.image_path is None:
                available = ", ".join(p.name for p in assets_dir.glob("*"))
                raise FileNotFoundError(
                    f"Could not find {img_base}.(jpg|jpeg|png) in {assets_dir}. "
                    f"Found: [{available}]"
                )
                    
        self.canvas = tk.Canvas(self)
        self.canvas.grid(row=0,column=0, sticky="nsew")
             
        self.canvas.bind("<Button-1>", self.on_canvas_click)

        self.load_and_display_image()


    def load_and_display_image(self):
        image = Image.open(self.image_path)
        original_width, original_height = image.size
        aspect_ratio = original_width / original_height
    
        target_width = 700
        target_height = int(target_width / aspect_ratio)
        image = image.resize((target_width, target_height), Image.LANCZOS)

        self.photo_image = ImageTk.PhotoImage(image)
        self.canvas.config(width=target_width, height=target_height)
        self.canvas.create_image(0,0, anchor="nw", image=self.photo_image)


    def _find_assets_dir(self) -> Path:
        env = os.environ.get("DUNK_ASSETS")
        if env:
            p = Path(env).expanduser().resolve()
            if p.exists() and p.is_dir():
                return p
        
        here = Path(__file__).resolve()
        for ancestor in [here.parent] + list(here.parents)[:6]:
            cwd_candidate = ancestor/"assets"
            if cwd_candidate.exists() and cwd_candidate.is_dir():
                return cwd_candidate
            
            raise FileNotFoundError(
                f"Could not find an 'assets' folder from {here} or CWD {Path.cwd()}./n"
                "Set DUNK_ASSETS or create an 'assets' directory."
            )
    
    #Handler method for court clickability
    def on_canvas_click(self, event):
        #draw a tiny dot to check operational
        r =4
        self.canvas.create_oval(event.x-r, event.y-r, event.x+r, event.y+r, fill="#d9534f", outline="")
        #hand off to parent frame
        if self.on_shot: 
            self.on_shot(event.x, event.y)

    