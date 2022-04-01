from __future__ import annotations

from fastapi import FastAPI
# app = FastAPI(title='Rss inn - RSS小黑屋', description='Powered by FastAPI', swagger_ui_parameters={"defaultModelsExpandDepth": -1})


def app_settings() -> FastAPI():
    return {
        'title': 'Rss inn - RSS小黑屋',
        'description': 'Powered by FastAPI',
        'swagger_ui_parameters': {"defaultModelsExpandDepth": -1},
    }
