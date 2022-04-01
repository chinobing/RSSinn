import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.exceptions import HTTPException
from routes import router as api_router
from models.http_error import http_exception_handler
from models.validation_error import http422_error_handler, RequestValidationError
from models.catch_exceptions import catch_exceptions_middleware

from settings import app_settings

settings = app_settings()
app = FastAPI(**settings)

app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(api_router)
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, http422_error_handler)

# overwrite exceptions handler and catch all internal error, then return 404 page, please uncomment it when debugging
app.middleware('http')(catch_exceptions_middleware)



if __name__ == '__main__':
    uvicorn.run('run:app', host='localhost', port=28085, reload=True, debug=True)