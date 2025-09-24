from app.handlers.auth import router as auth_router
from app.handlers.ping import router as ping_router
from app.handlers.tasks import router as tasks_router
from app.handlers.user import router as users_router

routers = [ping_router, tasks_router, users_router, auth_router]
