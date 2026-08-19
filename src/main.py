import random as rd
import customtkinter as ctk

from define import APP_TITLES, WINDOW_START_SIZE, WINDOW_MIN_SIZE
from transformations import get_deck_changes

class DeckUpdaterApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Window configuration
        self.title(rd.choice(APP_TITLES))
        self.geometry(f"{WINDOW_START_SIZE[0]}x{WINDOW_START_SIZE[1]}")
        self.minsize(WINDOW_MIN_SIZE[0], WINDOW_MIN_SIZE[1])

        # Configuration ui configuration (1 row, 2 cols)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # ==========================================
        # Old Deck
        # ==========================================
        self.frame_old = ctk.CTkFrame(self)
        self.frame_old.grid(row=0, column=0, padx=10, pady=(10, 5), sticky="nsew")
        self.frame_old.grid_columnconfigure(0, weight=1)
        self.frame_old.grid_rowconfigure(1, weight=1)

        self.label_old = ctk.CTkLabel(self.frame_old, text="Old deck list", font=ctk.CTkFont(weight="bold"))
        self.label_old.grid(row=0, column=0, pady=5)

        self.textbox_old = ctk.CTkTextbox(self.frame_old)
        self.textbox_old.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        # ==========================================
        # New Deck
        # ==========================================
        self.frame_new = ctk.CTkFrame(self)
        self.frame_new.grid(row=0, column=1, padx=10, pady=(10, 5), sticky="nsew")
        self.frame_new.grid_columnconfigure(0, weight=1)
        self.frame_new.grid_rowconfigure(1, weight=1)

        self.label_new = ctk.CTkLabel(self.frame_new, text="New deck list", font=ctk.CTkFont(weight="bold"))
        self.label_new.grid(row=0, column=0, pady=5)

        self.textbox_new = ctk.CTkTextbox(self.frame_new)
        self.textbox_new.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        # ==========================================
        # BOUTON
        # ==========================================
        self.btn_changes = ctk.CTkButton(self, text="Get changes", font=ctk.CTkFont(weight="bold"), command=self.show_changes_popup)
        self.btn_changes.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="ew")


    def show_changes_popup(self):
        # Get raw deck lists from textboxes
        old_deck_list_raw = self.textbox_old.get("1.0", "end-1c")
        new_deck_list_raw = self.textbox_new.get("1.0", "end-1c")

        result = get_deck_changes(old_deck_list_raw, new_deck_list_raw)
        if result is None:
            return

        changes = result[0]
        nb_changes = result[1]

        result_text = f"Modifications ({nb_changes}):\n{changes}"

        # Create popup window
        popup = ctk.CTkToplevel(self)
        popup.title("Modifications")
        popup.geometry("400x300")
        popup.grab_set() # Make popup modal (block interaction with main window)
        popup.attributes('-topmost', True) # Make popup always on top of the main window

        popup.grid_columnconfigure(0, weight=1)
        popup.grid_rowconfigure(0, weight=1)

        # Create popup content
        result_box = ctk.CTkTextbox(popup)
        result_box.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        result_box.insert("1.0", result_text)
        result_box.configure(state="disabled") # Désactive la modification

        # Copy button callback
        def copy_to_clipboard():
            self.clipboard_clear()
            self.clipboard_append(changes)
            btn_copy.configure(text="Copié ! ✔️", fg_color="green")
            # Remet le bouton à son état normal après 2 secondes
            popup.after(2000, lambda: btn_copy.configure(text="Copier les changements", fg_color=["#3B8ED0", "#1F6AA5"]))

        # 5. Copy button
        btn_copy = ctk.CTkButton(popup, text="Copier les changements", command=copy_to_clipboard)
        btn_copy.grid(row=1, column=0, padx=10, pady=10, sticky="ew")


if __name__ == "__main__":
    # Set system theme for the app (light/dark mode)
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")

    app = DeckUpdaterApp()
    app.mainloop()
