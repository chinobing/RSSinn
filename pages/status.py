from fastapi import Request, APIRouter
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates


status = APIRouter()
templates = Jinja2Templates(directory='./templates')
# status.mount("/static", StaticFiles(directory="static"), name="static")

@status.get("/status", include_in_schema=False)
async def status_page(request: Request):
    return templates.TemplateResponse("status.html",{"request": request})

