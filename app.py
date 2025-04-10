import requests
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates


app = FastAPI()
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def index_page(request: Request):
    context = {}
    # TODO получить список книг и данные об их наличии в филиалах
    return templates.TemplateResponse(request=request, name="index.html", context=context)
