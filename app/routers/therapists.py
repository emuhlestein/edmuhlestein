from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from ..core.utils import render_template

router = APIRouter(prefix="/therapists", tags=["therapists"])


@router.get("/", response_class=HTMLResponse)
def therapists_page(request: Request) -> HTMLResponse:
    return render_template("therapists.html", request, title="Therapists")