from typing import Optional
from fastapi import APIRouter, Query, HTTPException
from src.api.deps import get_books_cached

router = APIRouter(prefix="/api/v1/books", tags=["Books"])

@router.get("")
async def get_books():
    return get_books_cached()

@router.get("/search")
async def search_books(
    title: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
):
    books = get_books_cached()
    filtered = books

    if title:
        filtered = [b for b in filtered if title.lower() in b["Título"].lower()]

    if category:
        filtered = [b for b in filtered if category.lower() in b["Categoria"].lower()]

    return filtered

@router.get("/top-rated")
async def get_top_rated_books(limit: int = 5):
    books = get_books_cached()
    order = ["Zero", "One", "Two", "Three", "Four", "Five"]
    sorted_books = sorted(
        books,
        key=lambda x: order.index(x["Avaliação"]),
        reverse=True
    )
    return sorted_books[:int(limit)]

@router.get("/price-range")
async def get_books_by_price_range(min: float = 0, max: float = 100000):
    books = get_books_cached()
    return [
        b for b in books
        if min <= float(b["Preço"][1:]) <= max
    ]

@router.get("/{item_id}")
async def get_books_by_id(item_id: int):
    books = get_books_cached()
    if item_id < 0 or item_id >= len(books):
        raise HTTPException(status_code=404, detail="Book not found")
    return books[item_id]
