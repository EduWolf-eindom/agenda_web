from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/", response_class=HTMLResponse)
def calendar(request: Request):
    return templates.TemplateResponse(
        request,
        "calendar.html",
        {"request": request}
    )