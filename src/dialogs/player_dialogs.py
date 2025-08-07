from tkinter import simpledialog, messagebox

def prompt_add_player(parent):
    return simpledialog.askstring("Add Player", "Enter Player Name:", parent=parent)

def confirm_remove_player(parent, player_name):
    return messagebox.askyesno("Confirm", f"Remove {player_name}?")

