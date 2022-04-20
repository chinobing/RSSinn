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
from fastapi_cache import FastAPICache
from fastapi.logger import logger

fastAPI_logger = logger  # convenient name
yaml = parsing_yaml()
app_setting = yaml['app_setting']
cache_setting = yaml['related_settings']['cached']

async def on_start_up():
    fastAPI_logger.info("on_start_up")
    SingletonAiohttp.get_aiohttp_client()

async def on_shutdown():
    fastAPI_logger.info("on_shutdown")
    await SingletonAiohttp.close_aiohttp_client()

app_setting['on_startup'] = [on_start_up]
app_setting['on_shutdown'] = [on_shutdown]
app = FastAPI(**app_setting)

app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(api_router)
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, http422_error_handler)

# overwrite exceptions handler and catch all internal error, then return 404 page, please uncomment it when debugging
app.middleware('http')(catch_exceptions_middleware)

# Initialization for fastapi-cache
@app.on_event("startup")
async def startup():
    if cache_setting['enabled'] == False:
        return
    if cache_setting['enabled'] == True:
        if cache_setting['method'] =='in-memory':
            from fastapi_cache.backends.inmemory import InMemoryBackend
            FastAPICache.init(InMemoryBackend(), prefix="rssinn-cache")

        if cache_setting['method'] =='redis':
            import aioredis
            from fastapi_cache.backends.redis import RedisBackend
            redis_url = cache_setting['redis_url']
            redis =  aioredis.from_url(redis_url, encoding="utf8", decode_responses=False)
            FastAPICache.init(RedisBackend(redis), prefix="rssinn-cache")

if __name__ == '__main__':
    uvicorn.run('run:app', host='localhost', port=28085, reload=True, debug=True)