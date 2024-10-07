import customtkinter as ctk
from utils import MAIN_COLOR

class Heading1(ctk.CTkLabel):
    def __init__(self, parent, text, **kwargs):
        super().__init__(
            parent,
            text=text,
            font=("Arial", 34, "bold"),
            text_color=("#4f534d", MAIN_COLOR),
            **kwargs
        )

class Heading2(ctk.CTkLabel):
    def __init__(self, parent, text, **kwargs):
        super().__init__(
            parent,
            text=text,
            font=("Arial", 28, "bold"),
            text_color=("#4f534d", MAIN_COLOR),
            **kwargs
        )