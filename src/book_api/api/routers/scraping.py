from fastapi import APIRouter, Depends
from src.scraping import scraping
from src.auth.authentication import get_current_user

router = APIRouter(prefix="/api/v1/scraping", tags=["Scraping"])


@router.post("/trigger")
async def trigger_scraping(user: str = Depends(get_current_user)):
    return {"message": scraping.scrape_books()}
