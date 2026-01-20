from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, HTMLResponse
from pathlib import Path

from .routers import auth, users, repair, towing, bookings

app = FastAPI()

# Get the base directory (parent of backend directory)
BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_DIR = BASE_DIR / "frontend" / "static"

# Mount static files (css, js, images, etc.)
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

# Important: Serve index.html for root path "/"
@app.get("/", response_class=HTMLResponse)
async def serve_index():
    index_path = STATIC_DIR / "index.html"
    if not index_path.exists():
        return HTMLResponse(content="<h1>index.html not found</h1>", status_code=404)
    return FileResponse(index_path)

# Optional: serve other HTML pages directly if you want clean URLs
# (you can also let the frontend router handle them later)
@app.get("/register", response_class=HTMLResponse)
async def serve_register():
    return FileResponse(STATIC_DIR / "register.html")

@app.get("/dashboard", response_class=HTMLResponse)
async def serve_dashboard():
    return FileResponse(STATIC_DIR / "dashboard.html")

# Your API routes
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(repair.router)
app.include_router(towing.router)
app.include_router(bookings.router)

@app.get("/health")
def health_check():
    return {"status": "ok"}
