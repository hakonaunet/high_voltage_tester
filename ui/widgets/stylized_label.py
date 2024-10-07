import customtkinter as ctk
from utils import MAIN_COLOR

class StylizedLabel(ctk.CTkLabel):
    def __init__(self, parent, **kwargs):
        super().__init__(
            parent,
            font=("Arial", 16),
            anchor="w",
            **kwargs
        )