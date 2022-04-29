from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from datetime import datetime

sitemap = APIRouter()
templates = Jinja2Templates(directory='./templates')

@sitemap.get("/sitemap", include_in_schema=False)
async def sitemap_page(request: Request):
    reserved_routes = ["/docs","/redoc","/openapi.json", "/docs/oauth2-redirect", "/static", "/sitemap/{path:path}"]
    all_routes = []
    for route in request.app.routes:
        if route.path not in reserved_routes:
            if route.name is not None:
                all_routes.append(f"detail{route.path}")
    data = {}
    data['base_url'] = request.base_url
    data['lastmod'] = datetime.today().strftime("%Y-%m-%d")
    data['routes'] = all_routes

    return templates.TemplateResponse("sitemap.xml",{"request": request, "data":data} , media_type="application/xml")
