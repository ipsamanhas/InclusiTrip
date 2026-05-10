from app.routes.auth import router as auth_router
from app.routes.search import router as search_router
from app.routes.users import router as users_router

__all__ = ["auth_router", "search_router", "users_router"]
