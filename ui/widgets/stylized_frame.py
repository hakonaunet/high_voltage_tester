import customtkinter as ctk
from utils import MAIN_COLOR

class StylizedFrame(ctk.CTkFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(
            parent,
            corner_radius=15,
            border_width=2,
            border_color=MAIN_COLOR,
            fg_color=("gray88", "gray17"),
            **kwargs
        )