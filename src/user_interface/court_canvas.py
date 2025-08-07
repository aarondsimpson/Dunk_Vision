import tkinter as tk
from PIL import Image, ImageTk 
import os 

#Creating a reusable class that sets up for full court/half court selection
class CourtCanvas(tk.Frame):
    #Define a function that calls the window
    def __init__(self, master, court_type="half"):
        super().__init__(master)
        self.master = master
        self.court_type = court_type

        #Sets the title of the window to display as the court selected + court viewer
        self.title(f"{court_type.capitalize()}-Court Viewer")
        self.resizable(True,True)
        self.court_type = court_type 

        self.project_root = os.path.dirname(os.path.abspath(__file__))
        self._load_court_image()

    #Define a function that loads the image into the window
    def _load_court_image(self):
        if self.court_type == "half":
        #Load half court image 
            image_filename = "half_court.jpg"
        else: 
        #Load the full court image
            image_filename = "full_court.jpg"

        image_path = os.path.join(self.project_root, "assets", image_filename)

        #Load and resize image 
        originial_image = Image.open(image_path)
        resized_image = originial_image.resize((800,500))  

        #Covert to PhotoImage
        self.photo = ImageTk.PhotoImage(resized_image)

        #Display on Cavnas
        self.canvas - tk.Canvas(self, width=self.photo.width(), height=self.photo.height())
        self.canvas.pack()
        self.canvas.create_image(0,0, anchor="nw", image=self.photo)