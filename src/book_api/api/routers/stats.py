from fastapi import APIRouter
from src.book_api.api .deps import get_books_cached
from src.scripts import data_analysis

router = APIRouter(prefix="/api/v1/stats", tags=["Stats"])

@router.get("/overview")
async def get_stats_overview():
    books = get_books_cached()
    return data_analysis.analise_dados(books)

@router.get("/categories/{category}")
async def get_stats_by_category(category: str):
    books = get_books_cached()
    return data_analysis.analise_dados(books, categoria=category)
