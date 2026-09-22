from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from ..core.utils import render_template

router = APIRouter(prefix="/about", tags=["about"])


@router.get("/", response_class=HTMLResponse)
def about_page(request: Request) -> HTMLResponse:
    return render_template("about.html", request, title="About")