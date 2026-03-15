from fastapi import Request
from ..core.auth import get_current_user_optional
from ..templates.config import templates

def is_likely_browser(request: Request) -> bool:
    accept = request.headers.get("accept", "").lower()

    print(request)
    
    # Primary check: wants HTML
    wants_html = request.headers.get("HX-Request")

    print("wants_html: " + wants_html)
    
    if not wants_html:
        return False
    
    # Secondary check: avoid obvious API clients
    user_agent = request.headers.get("user-agent", "").lower()
    is_suspicious = "postman" in user_agent or "insomnia" in user_agent
    
    return wants_html and not is_suspicious

def render_template(
    template_name: str,
    request: Request,
    **kwargs
):
    context = {
        "request": request,
        "current_user": get_current_user_optional(request),
        **kwargs
    }
    return templates.TemplateResponse(template_name, context)

