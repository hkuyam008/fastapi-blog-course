from fastapi import APIRouter

from apps.v1 import route_blog, route_login


apps_router = APIRouter()

apps_router.include_router(router = route_blog.router, prefix="", tags=[""], include_in_schema=False)
apps_router.include_router(router = route_login.router, prefix="/auth", tags=[""], include_in_schema=False)
