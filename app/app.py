import utils.http_session
import utils.transport
import utils.session
from fastapi import FastAPI , Depends
from typing import Annotated

from app.config.app_config import getAppConfig
from app.routing import todo, auth
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
import os

app = FastAPI()
load_dotenv()  # Load environment variables from .env file
#include all routes here 
app.include_router(todo.router)
app.include_router(auth.router)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    errors = {}
    for error in exc.errors():
        print(f"The Error is {error}")
        errors[error['loc'][-1]] = error['msg']
    return JSONResponse({"message": "Validation Error", "errors": errors}, status_code=422)
@app.get("/")
def root():
    config=getAppConfig()
    return {"message": "Hello World"
            , "app_name":config.app_name,
            "database_url":config.database_url,
            "app_env":config.app_env
            }


@app.get("/{id:int}")
def root(id: int):
    return {"message": f"Hello World {id}"}


# @app.post("/todocreate")
# def create_todo(todo: dict):
#     return {"message": "Todo created", "todo": todo }

