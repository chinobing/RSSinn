from fastapi import APIRouter, Request
from fastapi.routing import APIRoute
from fastapi.templating import Jinja2Templates
import markdown

detail = APIRouter()
templates = Jinja2Templates(directory='./templates')


@detail.get("/detail/{path:path}", include_in_schema=False)
async def detail_page(request: Request, path:str):
    data = {}
    reserved_routes = ["/docs","/redoc","/openapi.json", "/docs/oauth2-redirect", "/static", "/sitemap/{path:path}"]
    if path and path not in reserved_routes :
        for route in request.app.routes:
            if path in route.path and isinstance(route, APIRoute):
                data['path'] = f"{request.base_url}{route.path[1:]}"
                data['description'] = markdown.markdown(route.description)

                return templates.TemplateResponse("detail.html", {"request": request, "data": data})

    data['path'] = "N/A"
    data['description'] = "N/A"
    return templates.TemplateResponse("detail.html", {"request": request, "data": data})
