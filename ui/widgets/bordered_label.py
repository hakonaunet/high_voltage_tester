import customtkinter as ctk

class BorderedLabel(ctk.CTkButton):
    def __init__(self, master, text, **kwargs):
        # Default settings for the BorderedLabel
        default_kwargs = {
            "fg_color": "transparent",
            "border_color": ("gray75", "gray30"),
            "border_width": 2,
            "corner_radius": 15,
            "height": 30,
            "text": text,
            "text_color": ("black", "white"),
            "font": ("Arial", 16),
            "hover": False,
        }

        # Update default_kwargs with any provided kwargs
        default_kwargs.update(kwargs)

        # Initialize the CTkButton parent class
        super().__init__(master, **default_kwargs)

    def configure(self, **kwargs):
        # Handle 'text_color' separately as CTkButton uses 'text_color' instead of 'fg_color' for text
        if "text_color" in kwargs:
            kwargs["text_color_disabled"] = kwargs["text_color"]
        super().configure(**kwargs)

    # No need to override cget as CTkButton already handles all attributes we're using