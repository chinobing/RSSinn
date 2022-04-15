from fastapi import Request, APIRouter
from fastapi.templating import Jinja2Templates
import markdown
import requests
import re

status = APIRouter()
templates = Jinja2Templates(directory='./templates')


@status.get("/status", include_in_schema=False)
async def status_page(request: Request):
    return templates.TemplateResponse("status.html",{"request": request})


@status.get("/upptime", include_in_schema=False)
async def upptime_page(request: Request):
    purge = "https://purge.jsdelivr.net/gh/chinobing/upptime-rssinn@master/README.md"
    url = "https://cdn.jsdelivr.net/gh/chinobing/upptime-rssinn@master/README.md"
    requests.get(purge)
    response = requests.get(url)
    content = response.text
    content = content.split('status page.')[1].split('[**Visit')[0]
    html = markdown.markdown(content, extensions=['markdown.extensions.tables'])
    table = html.replace('./','https://cdn.jsdelivr.net/gh/chinobing/upptime-rssinn@master/')
    table = table.replace('https%3A%2F%2Fraw.githubusercontent.com%2Fchinobing%2Fupptime-rssinn%2FHEAD', 'https://cdn.jsdelivr.net/gh/chinobing/upptime-rssinn@master/')
    table = table.replace('<table>', '<table class="table is-striped is-fullwidth">')
    table = re.sub(r"<img(.*?)height=\"13\">","",table, re.MULTILINE)

    return templates.TemplateResponse("upptime.html",{"request": request, "table":table})

