import customtkinter
from tkdial import Meter

# Initialize the main application window
app = customtkinter.CTk()
app.geometry("950x350")

# Create meter1 with specified configurations
meter1 = Meter(
    app,
    radius=250,
    start=0,
    end=12,
    border_width=2,
    major_divisions=2,
    minor_divisions=0.2,
    fg="black",
    text_color="white",
    start_angle=270,
    end_angle=-300,
    text_font="DS-Digital 20",
    scale_color="white",
    needle_color="white",
    axis_color="#e76a31",
    border_color="#e76a31",
    text="mA",
    state="Unbind",
    scroll_steps=0
)
meter1.set_mark(50, 60, "red")  # Set red marking from 130 to 160
meter1.set(0)  # Initialize meter1 to its maximum value
meter1.grid(row=0, column=1, padx=20, pady=30)

# Create meter2 with specified configurations
meter2 = Meter(
    app,
    radius=260,
    start=0,
    end=200,
    border_width=5,
    fg="black",
    text_color="white",
    start_angle=270,
    end_angle=-360,
    text_font="DS-Digital 30",
    scale_color="black",
    axis_color="white",
    needle_color="white"
)
meter2.set_mark(1, 100, "#92d050")
meter2.set_mark(105, 150, "yellow")
meter2.set_mark(155, 196, "red")
meter2.set(80)  # Set initial value
meter2.grid(row=0, column=0, padx=20, pady=30)

# Create meter3 with specified configurations
meter3 = Meter(
    app,
    fg="#242424",
    radius=250,
    start=0,
    end=12,
    start_angle=270,
    end_angle=-300,
    major_divisions=2,
    minor_divisions=0.2,
    border_width=0,
    text_color="white",
    text_font="DS-Digital 20",
    text="mA",
    scale_color="white",
    axis_color="cyan",
    needle_color="white",
    scroll_steps=0,
    state="Unbind"
)
meter3.set_mark(50, 60, "red")
meter3.set(5)
meter3.grid(row=0, column=2, pady=30)

# Function to animate meter1 from maximum to minimum
def animate_meter1():
    current_value = meter1.get()
    if current_value > meter1.start:
        # Decrement the meter's value
        meter1.set(current_value - 0.5)  # Change step size as needed
        # Schedule the function to run again after 50 milliseconds
        app.after(25, animate_meter1)
    else:
        # Optionally, you can restart the animation or perform another action
        print("Animation complete.")

# Start the animation after the main loop starts
app.after(1000, animate_meter1)  # Start after 1 second delay

# Run the application
app.mainloop()
