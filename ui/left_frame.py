# left_frame.py
import customtkinter as ctk
from ui.widgets import StylizedFrame, StylizedLabel, StylizedEntry, StylizedButton
from ui.widgets.headings import Heading2
from dataclasses import dataclass
from test_logic import BatchInformation
from utils import event_system

class LeftFrame(StylizedFrame):
    def __init__(self, parent):
        super().__init__(parent)
        
        # Initialize batch information
        self.batch_info = None

        # Configure grid
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure((1, 2, 3), weight=1)
        self.grid_rowconfigure(4, weight=0)
        
        # Change heading to "Batch Information"
        self.heading = Heading2(self, text="Batch Information")
        self.heading.grid(row=0, column=0, columnspan=2, pady=(20, 10), padx=(20, 20), sticky="ew")
        
        # Add "Work order nr." label and entry
        self.work_order_label = StylizedLabel(
            self,
            text="Work order nr.:"
        )
        self.work_order_label.grid(row=1, column=0, sticky="w", padx=(20, 5), pady=(10, 5))
        
        self.work_order_entry = StylizedEntry(
            self,
            placeholder_text="Enter here..."
        )
        self.work_order_entry.grid(row=1, column=1, sticky="ew", padx=(5, 20), pady=(10, 5))
        
        # Add "LOT hardener nr." label and entry
        self.lot_hardener_label = StylizedLabel(
            self,
            text="LOT hardener nr.:"
        )
        self.lot_hardener_label.grid(row=2, column=0, sticky="w", padx=(20, 5), pady=(5, 5))
        
        self.lot_hardener_entry = StylizedEntry(
            self,
            placeholder_text="Enter here..."
        )
        self.lot_hardener_entry.grid(row=2, column=1, sticky="ew", padx=(5, 20), pady=(5, 5))
        
        # Add "LOT molding compound nr." label and entry
        self.lot_molding_compound_label = StylizedLabel(
            self,
            text="LOT molding compound nr.:"
        )
        self.lot_molding_compound_label.grid(row=3, column=0, sticky="w", padx=(20, 5), pady=(5, 10))
        
        self.lot_molding_compound_entry = StylizedEntry(
            self,
            placeholder_text="Enter here..."
        )
        self.lot_molding_compound_entry.grid(row=3, column=1, sticky="ew", padx=(5, 20), pady=(5, 10))
        
        # Create a transparent frame for buttons
        self.button_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.button_frame.grid(row=4, column=0, columnspan=2, pady=(0, 10), padx=20, sticky="ew")
        self.button_frame.grid_columnconfigure((0, 1), weight=1)
        
        # Add "Confirm" and "Re-enter" buttons to the button frame
        self.confirm_button = StylizedButton(
            self.button_frame,
            text="Confirm",
            command=self.on_confirm
        )
        self.confirm_button.grid(row=0, column=0, pady=(0, 10), padx=(0, 5), sticky="ew")
        
        self.reenter_button = StylizedButton(
            self.button_frame,
            text="Re-enter",
            command=self.on_reenter
        )
        self.reenter_button.grid(row=0, column=1, pady=(0, 10), padx=(5, 0), sticky="ew")
        
        # Set initial button states
        self.confirm_button.configure(state='normal')
        self.reenter_button.configure(state='disabled')

    def update_button_states(self, confirmed=False):
        state_confirmed = 'disabled' if confirmed else 'normal'
        state_reenter = 'normal' if confirmed else 'disabled'

        self.confirm_button.configure(state=state_confirmed)
        self.work_order_entry.configure(state=state_confirmed)
        self.lot_hardener_entry.configure(state=state_confirmed)
        self.lot_molding_compound_entry.configure(state=state_confirmed)
        self.reenter_button.configure(state=state_reenter)

    def on_confirm(self):
        # Read entries
        work_order_number = self.work_order_entry.get().strip()
        lot_hardener_number = self.lot_hardener_entry.get().strip()
        lot_molding_compound_number = self.lot_molding_compound_entry.get().strip()
        
        # Validate entries (ensure they are not empty)
        if not all([work_order_number, lot_hardener_number, lot_molding_compound_number]):
            # Dispatch an error event or show a message to the user
            event_system.dispatch_event('error_occurred', {'error_message': 'All fields must be filled out.'})
            return
        
        # Store in BatchInformation
        self.batch_info = BatchInformation(
            work_order_number=work_order_number,
            lot_hardener_number=lot_hardener_number,
            lot_molding_compound_number=lot_molding_compound_number
        )
        
        # Update button states
        self.update_button_states(confirmed=True)
        
        # Dispatch an event to indicate that batch information is confirmed
        event_system.dispatch_event('batch_info_confirmed', {'batch_info': self.batch_info})

    def on_reenter(self):
        # Clear entries
        self.work_order_entry.delete(0, 'end')
        self.lot_hardener_entry.delete(0, 'end')
        self.lot_molding_compound_entry.delete(0, 'end')
        
        # Clear batch_info
        self.batch_info = None
        
        # Update button states
        self.update_button_states(confirmed=False)
        
        # Dispatch an event to indicate that batch information is cleared
        event_system.dispatch_event('batch_info_cleared')
