from fastapi import APIRouter
from fastapi.responses import RedirectResponse
from models.singletonAiohttp import SingletonAiohttp
from fastapi.logger import logger
fastAPI_logger = logger  # convenient name


async def on_start_up():
    fastAPI_logger.info("on_start_up")
    SingletonAiohttp.get_aiohttp_client()

async def on_shutdown():
    fastAPI_logger.info("on_shutdown")
    await SingletonAiohttp.close_aiohttp_client()

index = APIRouter(on_startup=[on_start_up], on_shutdown=[on_shutdown])


@index.get("/", include_in_schema=False)
async def home_page():
    response = RedirectResponse(url='/upptime')
    return response