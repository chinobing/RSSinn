from fastapi import HTTPException
from starlette.requests import Request
from fastapi.templating import Jinja2Templates
from fastapi.encoders import jsonable_encoder

templates = Jinja2Templates(directory='./templates')


async def http_exception_handler(request: Request, exc: HTTPException):
    """
    return 404 page when route is not available

    路径不存在时返回404页面
    """
    return templates.TemplateResponse("404.html",{"request": request, 'result': jsonable_encoder(exc)}, status_code=404)
