from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from datetime import datetime

sitemap = APIRouter()
templates = Jinja2Templates(directory='./templates')


@sitemap.get("/sitemap", include_in_schema=False)
async def home_page(request: Request):
    all_routes = []
    reserved_routes = ["/openapi.json", "/docs/oauth2-redirect", "/static", "/sitemap"]
    for route in request.app.routes:
        if route.path not in reserved_routes:
            if route.name is not None:
                all_routes.append(route.path[1:])

    data = {}
    data['base_url'] = request.base_url
    data['lastmod'] = datetime.now()
    data['routes'] = all_routes

    return templates.TemplateResponse("sitemap.xml",{"request": request, "data":data} , media_type="application/xml")

