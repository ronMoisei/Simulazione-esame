from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Order:
    order_id: int
    customer_id: int
    order_status: int
    order_date: datetime
    required_date: datetime
    shipped_date: datetime
    store_id: int
    staff_id: int

    def __eq__(self, other) -> bool:
        if not isinstance(other, Order):
            return NotImplemented
        return self.order_id == other.order_id

    def __hash__(self) -> int:
        return hash(self.order_id)

    def __lt__(self, other) -> bool:
        if not isinstance(other, Order):
            return NotImplemented
        return self.order_id < other.order_id

    def __str__(self) -> str:
        return f"{self.order_id}"