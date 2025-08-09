#Coordinates GUI window (size, title, layout)

import tkinter as tk
from tkinter import messagebox, simpledialog
from src.user_interface.court_frame import CourtFrame

class DunkVisionApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Dunk Vision")
        self.resizable(True,True)

        #Global button styling for the whole app
        self.option_add("*Button.Background","#f0f0f0")
        self.option_add("*Button.Foreground", "#000000")
        self.option_add("*Button.ActiveBackground","#d9d9d9")
        self.option_add("*Button.ActiveForeground", "#000000")
        
        #Prepping for warning dialog box when app is closed 
        self.protocol("WM_DELETE_WINDOW", self.on_app_close)

        court_type = self.prompt_user_for_court_type()
        self.build_ui(court_type)

    def prompt_user_for_court_type(self) -> str:
        self.withdraw()

        dlg = tk.Toplevel(self)
        dlg.title("Court Selection")
        dlg.resizable(False, False)
        dlg.transient(self)
      
        width, height = 420, 220
        self.update_idletasks()  # Ensure geometry is updated
        x = self.winfo_rootx() + (self.winfo_width() - width) // 2
        y = self.winfo_rooty() + (self.winfo_height() - height) // 2
        dlg.geometry(f"{width}x{height}+{max(0,x)}+{max(0,y)}")

        dlg.grab_set()
        dlg.attributes("-topmost", True)
        dlg.after(200, lambda: dlg.attributes("-topmost", False))

        tk.Label(dlg, text="Select Court Type:", font=("Arial", 18, "bold")).pack(pady=(20, 12))
        choice = {"value": "Half"}  # 
       
        def pick(val: str):
            choice.set(val)
            dlg.destroy()
        
        btn_row = tk.Frame(dlg)
        btn_row.pack(pady=8)
        tk.Button(btn_row, text="Half Court", font=("Arial", 14), width=14,
                  command=lambda: pick("Half")).grid(row=0, column=0, padx=10)
        tk.Button(btn_row, text="Full Court", font=("Arial", 14), width=14,
                  command=lambda: pick("Full")).grid(row=0, column=1, padx=10)
        
        dlg.protocol("WM_DELETE_WINDOW", lambda: pick("Half"))
        dlg.bind("<Escape>", lambda e: pick("Half"))  # Default to Half Court on Escape
        dlg.bind("<Return>", lambda e: pick(choice.get()))
        dlg.focus_force()


        dlg.wait_window(dlg)

        self.deiconify()  # Show the main window again
        return choice["value"]
       

    def build_ui(self,court_type):
        #placeholder layout
        self.grid_rowconfigure(0,weight=1)
        self.grid_columnconfigure(0,weight=1)

        self.court_frame = CourtFrame(self, court_type=court_type)
        self.court_frame.grid(row=0, column=0, sticky="nsew")

    def on_app_close(self): 
        if messagebox.askyesno("Quit", "Unsaved work will be lost. Quit?"):
            self.destroy()


