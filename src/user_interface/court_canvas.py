###Loads the Court Image

import tkinter as tk
from PIL import Image, ImageTk 
import os 

#Creating a reusable class that sets up for full court/half court selection
class CourtCanvas(tk.Frame):
    #Define a function that calls the window
    def __init__(self, master, court_type="half"):
        super().__init__(master)
        
        self.court_type = court_type 
        self.image_path = os.path.join("assets", f"{court_type}_court.jpeg")

        self.project_root = os.path.dirname(os.path.abspath(__file__))
        self._load_court_image()

        self.canvas = tk.Canvas(self)
        self.canvas.grid(row=0,column=0)
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