from fastapi import Request, APIRouter
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import markdown
import requests


status = APIRouter()
templates = Jinja2Templates(directory='./templates')
# status.mount("/static", StaticFiles(directory="static"), name="static")

@status.get("/status", include_in_schema=False)
async def status_page(request: Request):
    return templates.TemplateResponse("status.html",{"request": request})

@status.get("/upptime", include_in_schema=False)
async def upptime_page(request: Request):
    url = "https://cdn.jsdelivr.net/gh/chinobing/upptime-rssinn@master/README.md"
    response = requests.get(url)
    md_content = response.text
    html = markdown.markdown(md_content, extensions=['markdown.extensions.tables'])
    html = html.replace('./','https://cdn.jsdelivr.net/gh/chinobing/upptime-rssinn@master/')
    html = html.replace('https%3A%2F%2Fraw.githubusercontent.com%2Fchinobing%2Fupptime-rssinn%2FHEAD', 'https://cdn.jsdelivr.net/gh/chinobing/upptime-rssinn@master/')
    print(html)

    return templates.TemplateResponse("upptime.html",{"request": request, "html":html})

