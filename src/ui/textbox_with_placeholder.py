import customtkinter as ctk

class TextboxWithPlaceholder(ctk.CTkTextbox):
    def __init__(self, master, placeholder, **kwargs):
        super().__init__(master, **kwargs)
        self.placeholder = placeholder
        self.default_text_color = self.cget("text_color")
        self.placeholder_color = "gray"

        # On met le texte indicatif au démarrage
        self.put_placeholder()

        # On écoute les entrées et sorties de la zone de texte
        self.bind("<FocusIn>", self.remove_placeholder)
        self.bind("<FocusOut>", self.check_placeholder)

    def put_placeholder(self):
        self.insert("1.0", self.placeholder)
        self.configure(text_color=self.placeholder_color)

    def remove_placeholder(self, event=None):
        # Si le texte actuel est le hint, on l'efface quand l'utilisateur clique
        if self.get("1.0", "end-1c") == self.placeholder:
            self.delete("1.0", "end")
            self.configure(text_color=self.default_text_color)

    def check_placeholder(self, event=None):
        # Si l'utilisateur clique ailleurs et que la case est vide, on remet le hint
        if not self.get("1.0", "end-1c").strip():
            self.put_placeholder()

    def get_content(self):
        # Une méthode pratique pour ne pas récupérer le hint par erreur lors du parsing
        text = self.get("1.0", "end-1c")
        if text == self.placeholder:
            return ""
        return text