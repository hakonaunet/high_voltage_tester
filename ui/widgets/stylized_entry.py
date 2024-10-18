from customtkinter import CTkEntry, CTk

class StylizedEntry(CTkEntry):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.configure(
            font=("Arial", 16),
            border_width=2,
            corner_radius=15,
        )

if __name__ == "__main__":
    app = CTk()
    app.geometry("300x200")
    app.title("Stylized Entry")

    # Create and place a StylizedEntry widget
    entry = StylizedEntry(app, placeholder_text="Enter text here")
    entry.pack(pady=20, padx=20, fill="x", expand=True)

    app.mainloop()
