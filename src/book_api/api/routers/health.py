from fastapi import APIRouter, HTTPException, status
from src.book_api.api .deps import get_books_cached

router = APIRouter(prefix="/api/v1/health", tags=["Health"])

@router.get("", status_code=status.HTTP_200_OK)
async def get_health():
    try:
        books = get_books_cached()
        if not books:
            raise ValueError("Books list is empty")

        required_fields = {"Título", "Preço", "Categoria"}
        if not required_fields.issubset(books[0].keys()):
            raise ValueError("Invalid data structure")

        return {"status": "healthy", "books_loaded": len(books)}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(e),
        )
