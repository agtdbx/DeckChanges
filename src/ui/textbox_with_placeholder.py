import customtkinter as ctk

class TextboxWithPlaceholder(ctk.CTkTextbox):
    def __init__(self, master, placeholder, **kwargs):
        super().__init__(master, **kwargs)
        self.placeholder = placeholder
        self.default_text_color = self.cget("text_color")
        self.placeholder_color = "gray"

        # Setup placeholder
        self.put_placeholder()

        # Listen for focus events to manage the placeholder
        self.bind("<FocusIn>", self.remove_placeholder)
        self.bind("<FocusOut>", self.check_placeholder)

    def put_placeholder(self):
        self.insert("1.0", self.placeholder)
        self.configure(text_color=self.placeholder_color)

    def remove_placeholder(self, event=None):
        # If the user clicks and the current text is the hint, we clear it
        if self.get("1.0", "end-1c") == self.placeholder:
            self.delete("1.0", "end")
            self.configure(text_color=self.default_text_color)

    def check_placeholder(self, event=None):
        # Setup placeholder if the textbox is empty when it loses focus
        if not self.get("1.0", "end-1c").strip():
            self.put_placeholder()

    def get_content(self):
        # Avoid getting hint when getting content
        text = self.get("1.0", "end-1c")
        if text == self.placeholder:
            return ""
        return text