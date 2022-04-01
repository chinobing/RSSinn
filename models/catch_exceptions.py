from starlette.requests import Request
from fastapi.templating import Jinja2Templates


templates = Jinja2Templates(directory='./templates')

async def catch_exceptions_middleware(request: Request, call_next):
    """
    overwrite exceptions handler and catch all internal error, then return 404 page, please uncomment it when debugging

    内部出错返回404页面,debug调试的时候需要注释掉（overwritten exceptions handler）
    """
    try:
        return await call_next(request)
    except Exception as e:
        result = f'Opps！！！{e}'
        return templates.TemplateResponse("404.html",{"request": request, 'result': result}, status_code=404)