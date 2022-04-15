import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.exceptions import HTTPException
from routes import router as api_router
from models.http_error import http_exception_handler
from models.validation_error import http422_error_handler, RequestValidationError
from models.catch_exceptions import catch_exceptions_middleware
from models.singletonAiohttp import SingletonAiohttp
from models.read_yaml import parsing_yaml
from fastapi.logger import logger
fastAPI_logger = logger  # convenient name

async def on_start_up():
    fastAPI_logger.info("on_start_up")
    SingletonAiohttp.get_aiohttp_client()

async def on_shutdown():
    fastAPI_logger.info("on_shutdown")
    await SingletonAiohttp.close_aiohttp_client()

settings = parsing_yaml()['app_setting']
settings['on_startup'] = [on_start_up]
settings['on_shutdown'] = [on_shutdown]
app = FastAPI(**settings)

app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(api_router)
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, http422_error_handler)

# overwrite exceptions handler and catch all internal error, then return 404 page, please uncomment it when debugging
app.middleware('http')(catch_exceptions_middleware)


if __name__ == '__main__':
    uvicorn.run('run:app', host='localhost', port=28085, reload=True, debug=True)