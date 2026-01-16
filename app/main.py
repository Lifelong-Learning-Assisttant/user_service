from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api import auth, settings as settings_api, sessions

app = FastAPI(
    title=settings.app_name,
    openapi_url="/openapi.json",
    docs_url="/docs",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(settings_api.router, prefix="/settings", tags=["settings"])
app.include_router(sessions.router, prefix="/sessions", tags=["sessions"])

@app.get("/health")
async def health_check():
    return {"status": "ok", "service": "user-service"}