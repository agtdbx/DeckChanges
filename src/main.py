import os
import ctypes
import customtkinter as ctk

from define import VERSION
from deckChangesApp import DeckChangesApp

if __name__ == "__main__":
    if os.name == 'nt':
        myappid = f'agtdbx.deck_changes.app.{VERSION}'
        try:
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
        except Exception:
            pass

    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    app = DeckChangesApp()
    app.mainloop()
