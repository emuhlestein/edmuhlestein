from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from ..core.utils import render_template

router = APIRouter(prefix="/study", tags=["study"])


@router.get("/", response_class=HTMLResponse)
def study_page(request: Request) -> HTMLResponse:
    documents = [
        {
            "title": "Employee handbook",
            "slug": "employee-handbook",
            "summary": "How we work.",
        },
        {
            "title": "Postgres notes",
            "slug": "postgres-notes",
            "summary": "Roles vs app users.",
        },
        {
            "title": "Docker compose",
            "slug": "docker-compose",
            "summary": "Dev vs prod.",
        },
    ]
    return render_template("doc-list.html", request, title="Study",documents=documents)

@router.get("/new", response_class=HTMLResponse)
def new_page(request: Request) -> HTMLResponse:
    return render_template("study.html", request, title="New Document")

@router.get("/search", response_class=HTMLResponse)
def search_page(request: Request) -> HTMLResponse:
    return render_template("study.html", request, title="Search")