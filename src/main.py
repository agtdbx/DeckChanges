import os
import ctypes
import random as rd
import customtkinter as ctk

from define import VERSION, APP_TITLES, WINDOW_START_SIZE, WINDOW_MIN_SIZE
from transformations import DeckParseError, parse_deck_list, get_deck_changes
from ui.textbox_with_placeholder import TextboxWithPlaceholder

class DeckUpdaterApp(ctk.CTk):
    def __init__(self):
        appName = rd.choice(APP_TITLES)

        super().__init__(className=appName)

        # Window configuration
        self.title(appName)
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
        self.frame_old.grid_rowconfigure(2, weight=1)

        self.label_old = ctk.CTkLabel(self.frame_old, text="Ancienne deck list", font=ctk.CTkFont(weight="bold"))
        self.label_old.grid(row=0, column=0, pady=(5, 0))

        self.label_info_old = ctk.CTkLabel(self.frame_old, text="", text_color="red")

        self.textbox_old = TextboxWithPlaceholder(self.frame_old, placeholder="1x Approach of the Second Sun")
        self.textbox_old.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
        self.textbox_old.bind("<Control-a>", lambda e: self.select_all(self.textbox_old))

        self.btn_clear_old = ctk.CTkButton(self.frame_old, text="Vider", font=ctk.CTkFont(weight="bold"), command=lambda: self.clear_all(self.textbox_old))
        self.btn_clear_old.grid(row=3, column=0, columnspan=1, padx=10, pady=10, sticky="ew")

        # ==========================================
        # New Deck
        # ==========================================
        self.frame_new = ctk.CTkFrame(self)
        self.frame_new.grid(row=0, column=1, padx=10, pady=(10, 5), sticky="nsew")
        self.frame_new.grid_columnconfigure(0, weight=1)
        self.frame_new.grid_rowconfigure(2, weight=1)

        self.label_new = ctk.CTkLabel(self.frame_new, text="Nouvelle deck list", font=ctk.CTkFont(weight="bold"))
        self.label_new.grid(row=0, column=0, pady=(5, 0))

        self.label_info_new = ctk.CTkLabel(self.frame_new, text="", text_color="red")

        self.textbox_new = TextboxWithPlaceholder(self.frame_new, placeholder="2x Island\n1x Counterspell")
        self.textbox_new.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
        self.textbox_new.bind("<Control-a>", lambda e: self.select_all(self.textbox_new))

        self.btn_clear_new = ctk.CTkButton(self.frame_new, text="Vider", font=ctk.CTkFont(weight="bold"), command=lambda: self.clear_all(self.textbox_new))
        self.btn_clear_new.grid(row=3, column=0, columnspan=1, padx=10, pady=10, sticky="ew")

        # ==========================================
        # BOUTON
        # ==========================================
        self.btn_changes = ctk.CTkButton(self, text="Voir les changements", font=ctk.CTkFont(weight="bold"), command=self.show_changes_popup)
        self.btn_changes.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="ew")


    def select_all(self, textbox):
        textbox.tag_add("sel", "1.0", "end")
        return "break"


    def clear_all(self, textbox):
        textbox.delete("1.0", "end")


    def update_deck_info(self, label, message: str, is_warning: bool = False):
        if message == "":
            label.grid_forget()
        else:
            color = "orange" if is_warning else "red"
            label.configure(text=message, text_color=color)
            label.grid(row=1, column=0, pady=(0, 5))


    def show_changes_popup(self):
        # Get raw deck lists from textboxes
        deck_list_old_raw = self.textbox_old.get_content()
        deck_list_new_raw = self.textbox_new.get_content()

        # Parse deck lists
        need_exit = False

        deck_list_old = None
        try:
            deck_list_old, warning_message = parse_deck_list(deck_list_old_raw)
            self.update_deck_info(self.label_info_old, warning_message, is_warning=True)
        except DeckParseError as e:
            self.update_deck_info(self.label_info_old, str(e), is_warning=False)
            need_exit = True

        deck_list_new = None
        try:
            deck_list_new, warning_message = parse_deck_list(deck_list_new_raw)
            self.update_deck_info(self.label_info_new, warning_message, is_warning=True)
        except DeckParseError as e:
            self.update_deck_info(self.label_info_new, str(e), is_warning=False)
            need_exit = True

        if need_exit:
            return

        # Get changes
        changes_display, changes_copy = get_deck_changes(deck_list_old, deck_list_new)

        # Create popup window
        popup = ctk.CTkToplevel(self)
        popup.title("Changements")
        popup.geometry("400x300")
        popup.grab_set() # Make popup modal (block interaction with main window)
        popup.attributes('-topmost', True) # Make popup always on top of the main window

        popup.grid_columnconfigure(0, weight=1)
        popup.grid_rowconfigure(0, weight=1)

        # Create popup content
        result_box = ctk.CTkTextbox(popup)
        result_box.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        text_widget = result_box._textbox
        text_widget.tag_config("add", foreground="lightgreen")
        text_widget.tag_config("sub", foreground="salmon")

        for line in changes_display.split('\n'):
            if line.startswith('+'):
                result_box.insert("end", line + '\n', "add")
            elif line.startswith('-'):
                result_box.insert("end", line + '\n', "sub")
            else:
                result_box.insert("end", line + '\n')

        result_box.configure(state="disabled") # Désactive la modification

        # Copy button callback
        def copy_to_clipboard():
            self.clipboard_clear()
            self.clipboard_append(changes_copy)
            btn_copy.configure(text="Copié ! ✔️", fg_color="green")
            # Remet le bouton à son état normal après 2 secondes
            popup.after(2000, lambda: btn_copy.configure(text="Copier les changements", fg_color=["#3B8ED0", "#1F6AA5"]))

        # 5. Copy button
        btn_copy = ctk.CTkButton(popup, text="Copier les changements", command=copy_to_clipboard)
        btn_copy.grid(row=1, column=0, padx=10, pady=10, sticky="ew")


if __name__ == "__main__":
    if os.name == 'nt':
        myappid = f'agtdbx.deck_changes.app.{VERSION}'
        try:
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
        except Exception:
            pass

    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    app = DeckUpdaterApp()
    app.mainloop()
