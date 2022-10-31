from fastapi import APIRouter

from app.api.auth.view import auth_router

register_router = APIRouter()


register_router.include_router(auth_router, prefix="/auth", tags=["Auth"])
