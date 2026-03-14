from fastapi import Request

def is_likely_browser(request: Request) -> bool:
    accept = request.headers.get("accept", "").lower()
    
    # Primary check: wants HTML
    wants_html = "text/html" in accept or "application/xhtml" in accept
    
    if not wants_html:
        return False
    
    # Secondary check: avoid obvious API clients
    user_agent = request.headers.get("user-agent", "").lower()
    is_suspicious = "postman" in user_agent or "insomnia" in user_agent
    
    return wants_html and not is_suspicious
