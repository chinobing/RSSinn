from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
import requests
from models.read_yaml import parsing_yaml

index = APIRouter()
templates = Jinja2Templates(directory='./templates')
upptime_settings = parsing_yaml()['upptime']

@index.get("/", include_in_schema=False)
async def home_page(request: Request):
    if upptime_settings['enabled']==False:
        data = dict.fromkeys(['total_routes_numbers', 'routes_status_up', 'routes_status_down'], 'N/A')
        return templates.TemplateResponse("index.html",{"request": request, "data":data})

    if upptime_settings['jsdelivr_CDN']==True:
        purge_url = f"https://purge.jsdelivr.net/gh/{upptime_settings['github']}/{upptime_settings['repo']}@master/history/summary.json"
        summary_url = f"https://cdn.jsdelivr.net/gh/{upptime_settings['github']}/{upptime_settings['repo']}@master/history/summary.json"
        requests.get(purge_url)
    else:
        summary_url = f"https://raw.githubusercontent.com/{upptime_settings['github']}/{upptime_settings['repo']}/master/history/summary.json"

    response = requests.get(summary_url)
    up_down = response.json()
    routes_status_up =len([True for x in up_down if x['status']=='up'])
    routes_status_down = len([True for x in up_down if x['status'] == 'down'])
    total_routes_numbers = len(up_down)

    data = {}
    data['total_routes_numbers'] = total_routes_numbers
    data['routes_status_up'] = routes_status_up
    data['routes_status_down'] = routes_status_down

    return templates.TemplateResponse("index.html",{"request": request, "data":data})

