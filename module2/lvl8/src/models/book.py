from dataclasses import dataclass

@dataclass(frozen=True)
class Book:
    title: str
    rating: int
    price: float
    in_stock: bool
    img_path: str
    html_path: str