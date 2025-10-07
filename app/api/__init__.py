from app.api.router.admin.user import userrouter as user_router
from app.api.router.admin.auth import router as auth_router

routers = [user_router, auth_router]