import random as rd
import customtkinter as ctk

from define import APP_TITLES, WINDOW_START_SIZE, WINDOW_MIN_SIZE
from transformations import DeckParseError, parse_deck_list, get_deck_changes, create_changes_copy
from ui.textbox_with_placeholder import TextboxWithPlaceholder

class DeckChangesApp(ctk.CTk):
    def __init__(self):
        appName = rd.choice(APP_TITLES)

        super().__init__(className=appName)

        # Window configuration
        self.title(appName)
        self.geometry(f"{WINDOW_START_SIZE[0]}x{WINDOW_START_SIZE[1]}")
        self.minsize(WINDOW_MIN_SIZE[0], WINDOW_MIN_SIZE[1])

        # Ui configuration (1 row, 1 col)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Create tabs
        self.tabview = ctk.CTkTabview(self)
        self.tabview.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.tabview.add("decklists")
        self.tabview.add("changes")

        self.tabview.set("decklists")

        tab_decklists = self.tabview.tab("decklists")
        tab_changes = self.tabview.tab("changes")

        # ##############################################################################
        # TAB Deck lists
        # ##############################################################################

        # Ui configuration (1 row, 2 cols)
        tab_decklists.grid_columnconfigure(0, weight=1)
        tab_decklists.grid_columnconfigure(1, weight=1)
        tab_decklists.grid_rowconfigure(0, weight=1)

        # ==========================================
        # Old Deck
        # ==========================================
        self.frame_old = ctk.CTkFrame(tab_decklists)
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
        self.frame_new = ctk.CTkFrame(tab_decklists)
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
        # Button
        # ==========================================
        self.btn_changes = ctk.CTkButton(tab_decklists, text="Voir les changements", font=ctk.CTkFont(weight="bold"), command=self.compute_changes)
        self.btn_changes.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

        # ##############################################################################
        # TAB Changes
        # ##############################################################################

        # Ui configuration (3 rows, 2 cols)
        tab_changes.grid_columnconfigure(0, weight=1) # List col
        tab_changes.grid_columnconfigure(1, weight=1) # Image col
        tab_changes.grid_rowconfigure(0, weight=0) # Label
        tab_changes.grid_rowconfigure(1, weight=1) # List and Image
        tab_changes.grid_rowconfigure(2, weight=0) # Button

        # Label for changes numbers
        self.label_nb_changes = ctk.CTkLabel(tab_changes, text="Pas de modifications", font=ctk.CTkFont(weight="bold"))
        self.label_nb_changes.grid(row=0, column=0, columnspan=2, sticky="n")

        # Scroll list for changes
        self.scrollable_changes = ctk.CTkScrollableFrame(tab_changes)
        self.scrollable_changes.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        # Image for art of the card selected
        self.image_preview_label = ctk.CTkLabel(
            tab_changes,
            text="Aperçu de la carte\nIntrouvable",
            font=ctk.CTkFont(size=20, weight="bold"),
            fg_color=("gray80", "gray20"), # Fond visible pour prototyper
            corner_radius=10
        )
        self.image_preview_label.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

        # Button copy
        self.btn_copy = ctk.CTkButton(tab_changes, text="Copier les changements", command=self.copy_to_clipboard)
        self.btn_copy.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="ew")
        self.changes_copy = ""


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


    def compute_changes(self):
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
        added_cards, removed_cards, number_of_changes = get_deck_changes(deck_list_old, deck_list_new)
        self.changes_copy = create_changes_copy(added_cards, removed_cards)

        # Clear changes list
        for widget in self.scrollable_changes.winfo_children():
            widget.destroy()

        # Update label for nb changes
        if number_of_changes > 0:
            smart_s = "s" if number_of_changes > 1 else ""
            self.label_nb_changes.configure(text=f"{number_of_changes} changement{smart_s} :")
        else:
            self.label_nb_changes.configure(text="Pas de modifications")

        # Callback of card in changes
        def on_card_click(card_name):
            # Placeholder instead of api call
            self.image_preview_label.configure(text=f"Chargement de l'art pour :\n{card_name}")

        # Fill changes list with added cards
        for card_number, card_name in added_cards:
            text = ""
            if card_number > 1:
                text = f"+ {card_number} {card_name}"
            else:
                text = f"+ {card_name}"

            btn = ctk.CTkButton(
                self.scrollable_changes,
                text=text,
                text_color="lightgreen",
                fg_color="transparent",
                anchor="w",
                command=lambda name=card_name: on_card_click(name)
            )
            btn.pack(fill="x", pady=2)

        # Fill changes list with added cards
        for card_number, card_name in removed_cards:
            text = ""
            if card_number > 1:
                text = f"- {card_number} {card_name}"
            else:
                text = f"- {card_name}"

            btn = ctk.CTkButton(
                self.scrollable_changes,
                text=text,
                text_color="salmon",
                fg_color="transparent",
                anchor="w",
                command=lambda name=card_name: on_card_click(name)
            )
            btn.pack(fill="x", pady=2)

        self.tabview.set("changes")


    def copy_to_clipboard(self):
        self.clipboard_clear()
        self.clipboard_append(self.changes_copy)
        self.btn_copy.configure(text="Copié ! ✔️", fg_color="green")
        # Remet le bouton à son état normal après 2 secondes
        self.after(2000, lambda: self.btn_copy.configure(text="Copier les changements", fg_color=["#3B8ED0", "#1F6AA5"]))