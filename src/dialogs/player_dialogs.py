from tkinter import simpledialog, messagebox


def add_player_dialog(self):
        name = simpledialog.askstring("Add Player", "Enter Player Name:", parent=self)
        if name: 
            self.add_player(name.strip())