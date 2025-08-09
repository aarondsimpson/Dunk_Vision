#Coordinates GUI window (size, title, layout)

import tkinter as tk
import traceback
from tkinter import messagebox, simpledialog
from src.user_interface.court_frame import CourtFrame

class DunkVisionApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Dunk Vision")
        self.resizable(True,True)
        self.protocol("WM_DELETE_WINDOW", self.on_app_close)

        #Global button styling for the whole app
        self.option_add("*Button.Background","#f0f0f0")
        self.option_add("*Button.Foreground", "#000000")
        self.option_add("*Button.ActiveBackground","#d9d9d9")
        self.option_add("*Button.ActiveForeground", "#000000")
       
        self.withdraw()
        self.after(0, self._choose_and_build)

    def _choose_and_build(self):
        try: 
            court_type = self.prompt_user_for_court_type()
            court_type = (court_type or "half").strip().lower()
            print(f"[DV] court_type -> {court_type}")
            self.build_ui(court_type)
            print(f"[DV] build_ui done, now showing window")
        except Exception:
           tb = traceback.format_exc()
           print(tb)
           messagebox.showerror("Startup Error", tb)
        finally:
            self.deiconify()
            self.update_idletasks()
            self.state("normal")
            self.lift()
            try:
                self.attributes("-topmost", True)
                self.after(200, lambda: self.attributes("-topmost", False))
            except Exception:
                pass

    def prompt_user_for_court_type(self) -> str:
        dlg = tk.Toplevel(self)
        dlg.title("Court Selection")
        dlg.resizable(False, False)
        dlg.transient(self)
        dlg.grab_set()
      
        width, height = 420, 220
        dlg.update_idletasks()  # Ensure geometry is updated
        screen_x = (dlg.winfo_screenwidth() - width) // 2
        screen_y = (dlg.winfo_screenheight() - height) // 2
        dlg.geometry(f"{width}x{height}+{screen_x}+{max(0,screen_y)}")

        tk.Label(dlg, text="Select Court Type:", font=("Arial", 18, "bold")).pack(pady=(20, 12))
        
        choice = tk.StringVar(value="Half")  # Default to Half Court
        
        def pick(val: str):
            choice.set(val)
            dlg.destroy()
        
        row = tk.Frame(dlg); row.pack(pady=8)
        tk.Button(row, text="Half Court", font=("Arial", 14), width=14,
                  command=lambda: pick("Half")).grid(row=0, column=0, padx=10)
        tk.Button(row, text="Full Court", font=("Arial", 14), width=14,
                  command=lambda: pick("Full")).grid(row=0, column=1, padx=10)
        
        dlg.protocol("WM_DELETE_WINDOW", lambda: pick("Half"))
        dlg.bind("<Escape>", lambda e: pick("Half"))  # Default to Half Court on Escape
        dlg.bind("<Return>", lambda e: pick(choice.get()))
        dlg.focus_force()

        dlg.wait_window(dlg)
        return choice["value"]

    def build_ui(self,court_type: str):
        self.grid_rowconfigure(0,weight=1)
        self.grid_columnconfigure(0,weight=1)
        self.court_frame = CourtFrame(self, court_type=court_type)
        self.court_frame.grid(row=0, column=0, sticky="nsew")

    def on_app_close(self): 
        if messagebox.askyesno("Quit", "Unsaved work will be lost. Quit?"):
            self.destroy()


