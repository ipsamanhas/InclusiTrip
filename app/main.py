from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse

app = FastAPI()

BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = BASE_DIR / "frontend"


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/health")
def health_check():
    return {"status": "ok"}


async def home():
    return FileResponse(FRONTEND_DIR / "welcome.html")


@app.get("/login")
async def login():
    return FileResponse(FRONTEND_DIR / "login.html")


@app.get("/create-account")
async def create_account():
    return FileResponse(FRONTEND_DIR / "create-account.html")

