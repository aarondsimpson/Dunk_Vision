###Loads the Court Image

import tkinter as tk
from PIL import Image, ImageTk 
from pathlib import Path

#Creating a reusable class that sets up for full court/half court selection
class CourtCanvas(tk.Frame):
    
    def __init__(self, master, court_type="half"):
        super().__init__(master)
        self.court_type = court_type 

        assets_dir = self._find_assets_dir()
        
        img_base = f"{self.court_type}_court"
        self.image_path = None
        
        for ext in (".png", ".jpg", ".jpeg"):
            candidate = assets_dir / (img_base + ext)
            if candidate.exists():
                self.image_path = candidate
                break
            if not self.image_path:
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
        here = Path(__file__).resolve()

        for ancestor in (here.parent, here.parent.parent,here.parent.parent.parent):       
            candidate = ancestor / "assets" 
            if candidate.exists() and candidate.is_dir():
                return candidate
        raise FileNotFoundError("Could not find 'assets' folder starting from {here}")
    
    #Handler method for court clickability
    def on_canvas_click(self, event):
        #draw a tiny dot to check operational
        r =4
        self.canvas.create_oval(event.x-r, event.y-r, event.x+r, event.y+r, fill="d9534f", outline="")
        #hand off to parent frame
        if hasattr(self.master, "record_shot"):
            self.master.record_shot(event.x, event.y)

    def __init__(self, master, court_type="half"):
        super().__init__(master)
        self.court_type = court_type

        assets_dir = self._find_assets_dir()

        court = (self.court_type or "half").strip().lower()
        img_name = "half_court.jpg" if court == "half" else "full_court.jpg"

        self.image_path = assets_dir / img_name
        if not self.image_path.exists():
            available = ", ".join(p.name for p in assets_dir.glob("*"))
            raise FileNotFoundError(f"Could not find {img_name} in {assets_dir}. Found: [{available}]")
        
        self.canvas = tk.Canvas(self)
        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.load_and_display_image()