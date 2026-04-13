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
        
        self.app = None
        self.is_paused = False
        self.step_requested = False
        self.playback_speed = 1.0

    def toggle_pause(self):
        self.is_paused = not self.is_paused
        return self.is_paused

    def step_forward(self):
        if self.is_paused:
            self.step_requested = True

    def set_speed(self, value):
        self.playback_speed = max(0.1, float(value))

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
        """Draws an informative explanation text box at the top right of the canvas."""
        self.canvas.delete("explanation")
        if text:
            # Create text at top right corner
            self.canvas.create_text(
                self.width - 20, 20,
                text=text,
                fill="#FBBF24", # Amber for high visibility 
                font=("Inter", 16, "bold"),
                tags="explanation",
                justify="right",
                anchor="ne",
                width=max(200, self.width // 2.5) # enable text wrapping while keeping it to the right
            )
