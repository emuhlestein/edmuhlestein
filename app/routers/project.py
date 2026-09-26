from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from ..core.utils import render_template

router = APIRouter(prefix="/project", tags=["project"])


@router.get("/", response_class=HTMLResponse)
def project_page(request: Request) -> HTMLResponse:
    return render_template("project.html", request, title="Project")