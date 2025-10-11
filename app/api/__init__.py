from app.api.router.admin.user import userrouter as user_router
from app.api.router.admin.auth import router as auth_router
from app.api.router.admin.blog import router as blog
from app.api.router.v1.blog import blog_router as Userblog


routers = [user_router,blog, auth_router,Userblog]