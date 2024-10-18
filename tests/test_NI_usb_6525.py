import nidaqmx
from nidaqmx.constants import LineGrouping
import time

# Function to toggle all 8 relays on and off with keyboard interrupt handling
def toggle_all_relays():
    try:
        with nidaqmx.Task() as task:
            # Replace 'Dev1/port0/line0:7' with your actual device name and port in NI MAX
            task.do_channels.add_do_chan('Dev1/port0/line0:7', line_grouping=LineGrouping.CHAN_PER_LINE)

            print("Toggling all 8 relays every second. Press Ctrl+C to stop.")

            while True:
                # Turn all relays ON
                task.write([True]*8)  # Set all 8 relays to True (ON)
                print("All relays ON")
                time.sleep(1)

                # Turn all relays OFF
                task.write([False]*8)  # Set all 8 relays to False (OFF)
                print("All relays OFF")
                time.sleep(1)

    except KeyboardInterrupt:
        print("Script interrupted. Exiting...")

if __name__ == "__main__":
    toggle_all_relays()
