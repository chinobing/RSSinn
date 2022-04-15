from fastapi import Request, APIRouter
from fastapi.templating import Jinja2Templates
from models.read_yaml import parsing_yaml
import markdown
import requests
import re

status = APIRouter()
templates = Jinja2Templates(directory='./templates')
upptime_settings = parsing_yaml()['upptime']


@status.get("/upptime", include_in_schema=False)
async def upptime_page(request: Request):
    if upptime_settings['enabled']==False:
        table = ''
        return templates.TemplateResponse("upptime.html",{"request": request, "table":table})

    if upptime_settings['jsdelivr_CDN']==True:
        purge_url = f"https://purge.jsdelivr.net/gh/{upptime_settings['github']}/{upptime_settings['repo']}@master/README.md"
        readme_url = f"https://cdn.jsdelivr.net/gh/{upptime_settings['github']}/{upptime_settings['repo']}@master/README.md"
        requests.get(purge_url)
    else:
        readme_url = f"https://raw.githubusercontent.com/{upptime_settings['github']}/{upptime_settings['repo']}/master/README.md"

    response = requests.get(readme_url)
    content = response.text
    content = content.split('status page.')[1].split('[**Visit')[0]
    html = markdown.markdown(content, extensions=['markdown.extensions.tables'])
    table = html.replace('./',f"https://cdn.jsdelivr.net/gh/{upptime_settings['github']}/{upptime_settings['repo']}@master/")
    table = table.replace(f"https%3A%2F%2Fraw.githubusercontent.com%2F{upptime_settings['github']}%2F{upptime_settings['repo']}%2FHEAD", f"https://cdn.jsdelivr.net/gh/{upptime_settings['github']}/{upptime_settings['repo']}@master/")
    table = table.replace('<table>', '<table class="table is-striped is-fullwidth">')
    table = re.sub(r"<img(.*?)height=\"13\">","",table, re.MULTILINE)

    return templates.TemplateResponse("upptime.html",{"request": request, "table":table})

