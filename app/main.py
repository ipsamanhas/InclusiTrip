from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.database import Base, engine, migrate_sqlite_users_table
from app.routes import auth_router, hotels_router, search_router, users_router

app = FastAPI(title="InclusiTrip API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(hotels_router)
app.include_router(search_router)
app.include_router(users_router)

BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = BASE_DIR / "frontend"

app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")


def html_file(filename: str) -> FileResponse:
    """Serve frontend HTML without browser caching during local development."""
    return FileResponse(
        FRONTEND_DIR / filename,
        headers={"Cache-Control": "no-store"},
    )


@app.on_event("startup")
def on_startup() -> None:
    """Create database tables and seed initial data on server start."""
    Base.metadata.create_all(bind=engine)
    migrate_sqlite_users_table(engine)

    from app.data.seed import seed_database
    seed_database()


@app.get("/api/hello")
def read_root():
    return {"Hello": "World"}


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/")
async def home():
    return html_file("welcome.html")


@app.get("/login")
async def login():
    return html_file("login.html")


@app.get("/create-account")
async def create_account():
    return html_file("create-account.html")


@app.get("/hotels-search")
async def hotels_search():
    return html_file("hotels-search.html")


@app.get("/hotel")
async def hotel_detail():
    return html_file("hotel.html")
