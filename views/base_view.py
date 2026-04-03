import tkinter as tk
import customtkinter as ctk

class BaseView(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        # using a deeper premium dark shade for the canvas
        self.canvas = tk.Canvas(self, bg="#0B0F19", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.bind("<Configure>", self.on_resize)
        
        self.width = 1
        self.height = 1
        self.animating = False

    def on_resize(self, event):
        self.width = event.width
        self.height = event.height
        self.draw_base()
        self.draw_items()

    def draw_base(self):
        pass

    def draw_items(self):
        pass

    def set_explanation(self, text):
        """Draws an informative explanation text box at the bottom of the canvas."""
        self.canvas.delete("explanation")
        if text:
            # Create text at bottom center
            self.canvas.create_text(
                self.width / 2, self.height - 40,
                text=text,
                fill="#FBBF24", # Amber for high visibility 
                font=("Inter", 16, "bold"),
                tags="explanation",
                justify="center",
                width=self.width - 40 # enable text wrapping
            )
