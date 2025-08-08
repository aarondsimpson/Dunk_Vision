from tkinter import simpledialog, messagebox

def prompt_user_for_court_type(self):
    self.lift()
    self.attributes('-topmost', True)
    self.after(100, lambda: self.attributes('-topmost', False))

    value = simpledialog.askstring(
        "Select Court Type",
        "Enter 'Half' or 'Full':",
        parent=self,
        initialvalue='Half',
    )   
    return value if value in ['Half', 'Full'] else "Half"


def prompt_add_player(parent):
    return simpledialog.askstring("Add Player", "Enter Player Name:", parent=parent)

def confirm_remove_player(parent, player_name):
    return messagebox.askyesno("Confirm", f"Remove {player_name}?")

