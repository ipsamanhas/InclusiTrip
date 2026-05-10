from pathlib import Path

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

from app.database import Base, engine, get_db, migrate_sqlite_users_table
from app.data.users import get_user_by_email, get_user_by_id, verify_password
from app.models.models import LoginRequest
from app.routes import auth_router

app = FastAPI(title="InclusiTrip API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)

BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = BASE_DIR / "frontend"

app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")


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
    return FileResponse(FRONTEND_DIR / "welcome.html")


@app.get("/login")
async def login():
    return FileResponse(FRONTEND_DIR / "login.html")


@app.get("/create-account")
async def create_account():
    return FileResponse(FRONTEND_DIR / "create-account.html")


@app.post("/api/login")
def login_user(credentials: LoginRequest, db: Session = Depends(get_db)):
    user = get_user_by_email(db, credentials.email)
    if user is None or not verify_password(credentials.password, user.password):
        raise HTTPException(
            status_code=404,
            detail=(
                "We could not find an account with those login details. "
                "Please create an account or continue as a guest."
            ),
        )

    return {
        "authenticated": True,
        "user_id": user.id,
        "profile_url": f"/api/users/{user.id}/profile",
    }


@app.get("/api/users/{user_id}/profile")
def get_user_profile(user_id: str, db: Session = Depends(get_db)):
    user = get_user_by_id(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User profile not found.")

    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "phone": getattr(user, "phone", None),
        "photo_url": getattr(user, "photo_url", None),
        "accessibility_profile": user.accessibility_profile,
    }
