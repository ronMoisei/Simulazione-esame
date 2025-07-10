from dataclasses import dataclass


@dataclass
class Store:
    store_id: int
    store_name: str
    phone: str
    email: str
    street: str
    city: str
    state: str
    zip_code: str

    def __eq__(self, other):
        if not isinstance(other, Store):
            return NotImplemented
        return self.store_id == other.store_id

    def __lt__(self, other):
        if not isinstance(other, Store):
            return NotImplemented
        return self.store_id < other.store_id

    def __hash__(self):
        # Permette di usare Store come chiave in dict o in set
        return hash(self.store_id)

    def __str__(self):
        # Rappresentazione “user-friendly”
        return (
            f"Store(id={self.store_id}, "
            f"name={self.store_name!r}, "
            f"phone={self.phone!r}, "
            f"email={self.email!r}, "
            f"address={self.street!r}, "
            f"{self.city!r}, {self.state!r} {self.zip_code!r})"
        )