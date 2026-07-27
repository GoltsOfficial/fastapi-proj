from fastapi import APIRouter

from fastapi_proj.apps.auth.routes import auth_router
from fastapi_proj.apps.profile.routes import profile_router

apps_router = APIRouter(prefix="/api/v1")

apps_router.include_router(router=auth_router)
apps_router.include_router(router=profile_router)
