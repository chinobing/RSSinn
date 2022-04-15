from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
import requests

index = APIRouter()
templates = Jinja2Templates(directory='./templates')


@index.get("/", include_in_schema=False)
async def home_page(request: Request):
    purge_url = "https://purge.jsdelivr.net/gh/chinobing/upptime-rssinn@master/history/summary.json"
    summary_url = "https://cdn.jsdelivr.net/gh/chinobing/upptime-rssinn@master/history/summary.json"
    requests.get(purge_url)
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

