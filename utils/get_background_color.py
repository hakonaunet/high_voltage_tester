import customtkinter as ctk

def get_theme_background(new_theme=None):
    """
    Returns the appropriate background color based on the current appearance mode.
    If new_theme is provided, uses it instead of querying CustomTkinter.
    Modify the color codes as per your design requirements.
    """
    if new_theme is None:
        appearance_mode = ctk.get_appearance_mode()
    else:
        appearance_mode = new_theme

    if appearance_mode == "Dark":
        return "#1f1f1f"  # Example dark background color
    else:
        return "#f0f0f0"  # Example light background color