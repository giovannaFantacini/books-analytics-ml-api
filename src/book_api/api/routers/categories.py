from fastapi import APIRouter
from src.book_api.api .deps import get_books_cached

router = APIRouter(prefix="/api/v1/categories", tags=["Categories"])

@router.get("")
async def get_categories():
    books = get_books_cached()
    return list({book["Categoria"] for book in books})
