from fastapi import APIRouter
from fastapi.responses import RedirectResponse



index = APIRouter()

@index.get("/", include_in_schema=False)
async def home_page():
    response = RedirectResponse(url='/status')
    return response