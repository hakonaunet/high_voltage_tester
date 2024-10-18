import customtkinter as ctk

class StylizedButton(ctk.CTkButton):
    def __init__(self, master, **kwargs):
        super().__init__(
            master,
            corner_radius=15,
            height=60,
            font=("Arial", 18, "bold"),
            **kwargs
        )
