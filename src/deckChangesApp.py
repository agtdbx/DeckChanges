import random as rd
import customtkinter as ctk

from define import APP_TITLES, WINDOW_START_SIZE, WINDOW_MIN_SIZE, ASYNC_PARSING_TIME, ARCHIDEKT_URL
from transformations import DeckParseError, parse_decklist, get_deck_changes, create_changes_copy
from ui.textbox_with_placeholder import TextboxWithPlaceholder
from scryfall_api import get_card_images
from archidekt_api import replace_url_by_decklist

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

        self._timer_old = None
        self.decklist_old = None
        self.textbox_old.bind("<KeyRelease>", lambda e: self.schedule_parsing('old'))

        self.btn_clear_old = ctk.CTkButton(self.frame_old, text="Vider", font=ctk.CTkFont(weight="bold"), command=lambda: self.clear_all(self.textbox_old, self.label_info_old))
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

        self._timer_new = None
        self.decklist_new = None
        self.textbox_new.bind("<KeyRelease>", lambda e: self.schedule_parsing('new'))

        self.btn_clear_new = ctk.CTkButton(self.frame_new, text="Vider", font=ctk.CTkFont(weight="bold"), command=lambda: self.clear_all(self.textbox_new, self.label_info_new))
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

        # ==========================================
        # Changes list
        # ==========================================
        self.scrollable_changes = ctk.CTkScrollableFrame(tab_changes)
        self.scrollable_changes.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        # ==========================================
        # Card image
        # ==========================================
        self.frame_card_image = ctk.CTkFrame(tab_changes)
        self.frame_card_image.grid(row=1, column=1, padx=10, pady=(10, 5), sticky="nsew")

        self.frame_card_image.grid_columnconfigure(0, weight=1)
        self.frame_card_image.grid_rowconfigure(0, weight=1)
        self.frame_card_image.grid_rowconfigure(1, weight=0)

        # Image for art of the card selected
        self.image_preview_label = ctk.CTkLabel(
            self.frame_card_image,
            text="Pas de carte\nsélectionnée",
            font=ctk.CTkFont(size=20, weight="bold"),
            fg_color=("gray80", "gray20"), # Fond visible pour prototyper
            corner_radius=10
        )
        self.image_preview_label.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Button switch image
        self.btn_flip_image = ctk.CTkButton(self.frame_card_image, text="Retourner la carte", command=self.flip_card_image)
        # self.btn_flip_image.grid(row=1, column=0, padx=10, pady=10, sticky="sew")
        self.card_images = None

        # ==========================================
        # Button
        # ==========================================
        self.btn_copy = ctk.CTkButton(tab_changes, text="Copier les changements", command=self.copy_to_clipboard)
        self.btn_copy.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="ew")
        self.changes_copy = ""


    def select_all(self, textbox):
        textbox.tag_add("sel", "1.0", "end")
        return "break"


    def clear_all(self, textbox, label_info):
        textbox.delete("1.0", "end")
        textbox.put_placeholder()
        self.update_deck_info(label_info, "")


    def update_deck_info(self, label, message: str, is_warning: bool = False):
        if message == "":
            label.grid_forget()
        else:
            color = "orange" if is_warning else "red"
            label.configure(text=message, text_color=color)
            label.grid(row=1, column=0, pady=(0, 5))


    def schedule_parsing(self, mode: str):
        if mode == 'old':
            if self._timer_old is not None:
                self.after_cancel(self._timer_old)
            self._timer_old = self.after(ASYNC_PARSING_TIME, lambda: self.async_parsing('old'))
            self.decklist_old = None

        else:
            if self._timer_new is not None:
                self.after_cancel(self._timer_new)
            self._timer_new = self.after(ASYNC_PARSING_TIME, lambda: self.async_parsing('new'))
            self.decklist_new = None


    def async_parsing(self, mode: str):
        if mode == 'old':
            raw_text = self.textbox_old.get_content()
            label = self.label_info_old
        else:
            raw_text = self.textbox_new.get_content()
            label = self.label_info_new

        if not raw_text.strip():
            self.update_deck_info(label, "")
            if mode == "old":
                self.decklist_old = None
            else:
                self.decklist_new = None
            return

        if ARCHIDEKT_URL in raw_text:
            raw_text = replace_url_by_decklist(raw_text)

            if mode == 'old':
                self.textbox_old.set_content(raw_text)
            else:
                self.textbox_new.set_content(raw_text)

        try:
            decklist, warning_message = parse_decklist(raw_text)
            self.update_deck_info(label, warning_message, is_warning=True)
            if mode == "old":
                self.decklist_old = decklist
            else:
                self.decklist_new = decklist
        except DeckParseError as e:
            # S'il y a une erreur de format, ça l'affiche en rouge
            self.update_deck_info(label, str(e), is_warning=False)


    def compute_changes(self):
        # Parse deck lists
        need_exit = False

        if self._timer_old is not None:
            self.after_cancel(self._timer_old)
            self._timer_old = None

        if self._timer_new is not None:
            self.after_cancel(self._timer_new)
            self._timer_new = None

        if self.decklist_old == None:
            decklist_old_raw = self.textbox_old.get_content()
            if ARCHIDEKT_URL in decklist_old_raw:
                decklist_old_raw = replace_url_by_decklist(decklist_old_raw)
                self.textbox_old.set_content(decklist_old_raw)

            try:
                decklist_old, warning_message = parse_decklist(decklist_old_raw)
                self.update_deck_info(self.label_info_old, warning_message, is_warning=True)
                self.decklist_old = decklist_old
            except DeckParseError as e:
                self.update_deck_info(self.label_info_old, str(e), is_warning=False)
                need_exit = True

        if self.decklist_new == None:
            decklist_new_raw = self.textbox_new.get_content()
            if ARCHIDEKT_URL in decklist_new_raw:
                decklist_new_raw = replace_url_by_decklist(decklist_new_raw)
                self.textbox_new.set_content(decklist_new_raw)

            try:
                decklist_new, warning_message = parse_decklist(decklist_new_raw)
                self.update_deck_info(self.label_info_new, warning_message, is_warning=True)
                self.decklist_new = decklist_new
            except DeckParseError as e:
                self.update_deck_info(self.label_info_new, str(e), is_warning=False)
                need_exit = True

        if need_exit:
            return

        # Get changes
        added_cards, removed_cards, number_of_changes = get_deck_changes(self.decklist_old, self.decklist_new)
        self.changes_copy = create_changes_copy(added_cards, removed_cards)

        # Clear changes list
        for widget in self.scrollable_changes.winfo_children():
            widget.destroy()

        # Clear image preview
        self.image_preview_label.configure(image="", text=f"Pas de carte\nsélectionnée")
        self.btn_flip_image.grid_remove()

        # Update label for nb changes
        if number_of_changes > 0:
            smart_s = "s" if number_of_changes > 1 else ""
            self.label_nb_changes.configure(text=f"{number_of_changes} changement{smart_s} :")
        else:
            self.label_nb_changes.configure(text="Pas de modifications")

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
                command=lambda name=card_name: self.on_card_click(name)
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
                command=lambda name=card_name: self.on_card_click(name)
            )
            btn.pack(fill="x", pady=2)

        self.tabview.set("changes")


    def copy_to_clipboard(self):
        self.clipboard_clear()
        self.clipboard_append(self.changes_copy)
        self.btn_copy.configure(text="Copié ! ✔️", fg_color="green")

        # Reset button style after 2 seconds
        self.after(2000, lambda: self.btn_copy.configure(text="Copier les changements", fg_color=["#3B8ED0", "#1F6AA5"]))


    def on_card_click(self, card_name):
        self.card_images = get_card_images(card_name)

        if self.card_images and self.card_images[0]:
            self.image_preview_label.configure(image=self.card_images[0], text="")
            if self.card_images[1]:
                self.btn_flip_image.grid(row=1, column=0, padx=10, pady=10, sticky="sew")
            else:
                self.btn_flip_image.grid_remove()
        else:
            self.image_preview_label.configure(image="", text=f"Impossible de trouver l'image pour :\n{card_name}")
            self.btn_flip_image.grid_remove()


    def flip_card_image(self):
        if not self.card_images or not self.card_images[1]:
            return

        self.card_images = (self.card_images[1], self.card_images[0])
        self.image_preview_label.configure(image=self.card_images[0], text="")
