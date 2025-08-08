###Loads the Court Image

import tkinter as tk
from PIL import Image, ImageTk 
import os 
from pathlib import Path

#Creating a reusable class that sets up for full court/half court selection
class CourtCanvas(tk.Frame):
    #Define a function that calls the window
    def __init__(self, master, court_type="half"):
        super().__init__(master)
        self.court_type = court_type 

        ##DEBUG##
        FILE_DIR = Path(__file__).resolve()
        PROJECT_ROOT = FILE_DIR.parents[2]
        ASSETS_DIR = PROJECT_ROOT / "assets"

        img_base = f"{self.court_type}_court"
        for ext in [".png", ".jpg", ".jpeg"]:
            candidate = ASSETS_DIR / (img_base + ext)
            if candidate.exists():
                self.image_path = candidate
                break
        else:
            print("DEBUG assets contents:", [p.name for p in ASSETS_DIR.glob("*")])
            raise FileNotFoundError(
                f"Could not find {img_base}.(jpeg|png|jpg) in {ASSETS_DIR}"
            )
        
        self.canvas = tk.Canvas(self)
        self.canvas.grid(row=0,column=0, sticky="nsew")
             
    
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