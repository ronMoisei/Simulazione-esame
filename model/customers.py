# file: model/customer.py

from dataclasses import dataclass

@dataclass
class Customer:
    """
    Rappresenta una riga della tabella `customers`.
    """
    customer_id: int    # PRIMARY KEY
    first_name: str
    last_name: str
    phone: str
    email: str
    street: str
    city: str
    state: str
    zip_code: str


    def __str__(self):
        return f"{self.customer_id} - {self.first_name} {self.last_name}"

    def __hash__(self):
        return hash(self.customer_id)