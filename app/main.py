from pathlib import Path
from uuid import UUID

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.data.seed import USERS
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
def login_user(credentials: LoginRequest):
    for user in USERS:
        if user.email == credentials.email and user.password == credentials.password:
            return {
                "authenticated": True,
                "user_id": str(user.id),
                "profile_url": f"/api/users/{user.id}/profile",
            }

    raise HTTPException(
        status_code=404,
        detail=(
            "We could not find an account with those login details. "
            "Please create an account or continue as a guest."
        ),
    )


@app.get("/api/users/{user_id}/profile")
def get_user_profile(user_id: UUID):
    for user in USERS:
        if user.id == user_id:
            return {
                "id": str(user.id),
                "name": user.name,
                "email": user.email,
                "accessibility_profile": user.accessibility_profile,
            }

    raise HTTPException(status_code=404, detail="User profile not found.")
