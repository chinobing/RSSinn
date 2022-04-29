from fastapi import APIRouter, Request
from fastapi.routing import APIRoute
from fastapi.templating import Jinja2Templates
from datetime import datetime
import markdown

sitemap = APIRouter()
templates = Jinja2Templates(directory='./templates')


@sitemap.get("/sitemap/{path:path}", include_in_schema=False)
async def sitemap_page(request: Request, path:str):
    reserved_routes = ["/docs","/redoc","/openapi.json", "/docs/oauth2-redirect", "/static", "/sitemap/{path:path}"]
    if path and path not in reserved_routes :
        for route in request.app.routes:
            if path in route.path and isinstance(route, APIRoute):
                data = {}
                data['path'] = f"{request.base_url}{route.path[1:]}"
                data['description'] = markdown.markdown(route.description)

                return templates.TemplateResponse("sitemap.html", {"request": request, "data": data})

    all_routes = []
    for route in request.app.routes:
        if route.path not in reserved_routes:
            if route.name is not None:
                all_routes.append(f"sitemap{route.path}")
    data = {}
    data['base_url'] = request.base_url
    data['lastmod'] = datetime.today().strftime("%Y-%m-%d")
    data['routes'] = all_routes

    return templates.TemplateResponse("sitemap.xml",{"request": request, "data":data} , media_type="application/xml")
