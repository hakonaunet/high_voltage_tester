# batch_information.py
from dataclasses import dataclass

@dataclass
class BatchInformation:
    work_order_number: str = ''
    lot_hardener_number: str = ''
    lot_molding_compound_number: str = ''