from app.api.router.admin.user import userrouter as user_router
from app.api.router.admin.auth import router as auth_router
from app.api.router.admin.blog import router as blog
from app.api.router.v1.blog import blog_router as Userblog
from app.api.router.admin.event import router as event_router
from app.api.router.v1.event import event_router as event_router_v1
from app.api.router.v1.enquiry import router as enquiry_router
from app.api.router.admin.enquiry import router as admin_enquiry_router

routers = [user_router,blog, auth_router,Userblog, event_router,event_router_v1,enquiry_router,admin_enquiry_router]