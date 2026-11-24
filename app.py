"""
WSGI entrypoint for Vercel Python runtime.
Serves index.html, llms.txt, and static data assets directly.
"""
import pathlib

ROOT = pathlib.Path(__file__).parent

def app(environ, start_response):
    path = environ.get("PATH_INFO", "/").lstrip("/")
    target = ROOT / path if path else ROOT / "index.html"
    
    if not target.exists() or target.is_dir():
        target = ROOT / "index.html"
        
    ext = target.suffix.lower()
    content_types = {
        ".html": "text/html; charset=utf-8",
        ".txt": "text/plain; charset=utf-8",
        ".css": "text/css; charset=utf-8",
        ".js": "application/javascript",
        ".json": "application/json",
        ".svg": "image/svg+xml",
        ".png": "image/png",
        ".ico": "image/x-icon"
    }
    content_type = content_types.get(ext, "application/octet-stream")
    
    try:
        content = target.read_bytes()
        status = "200 OK"
    except Exception as e:
        content = f"Error reading file: {e}".encode("utf-8")
        status = "500 Internal Server Error"
        content_type = "text/plain"
        
    headers = [
        ("Content-Type", content_type),
        ("Content-Length", str(len(content))),
        ("Cache-Control", "public, max-age=3600")
    ]
    start_response(status, headers)
    return [content]
