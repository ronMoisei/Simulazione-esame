from dataclasses import dataclass

@dataclass
class Prodotto:
    """
    Dataclass che rappresenta una riga della tabella `products`.
    """
    product_id: int      # PRIMARY KEY
    product_name: str
    brand_id: int
    category_id: int
    model_year: int
    list_price: float

    def __hash__(self):
        return hash(self.product_id)

    def __str__(self):
        return f"p:{self.product_name} - brand: {self.brand_id}"