from fastapi import Request
from functools import lru_cache

import src.app.config as config


@lru_cache()
def get_settings():
    return config.Settings()


def get_db(request: Request):
    return request.state.db
