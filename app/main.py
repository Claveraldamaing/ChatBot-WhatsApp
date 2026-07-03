from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.api.router import api_router
from app.core.database import init_pool
from app.core.scheduler import iniciar_scheduler
app = FastAPI(
    title="ChatBot WhatsApp API",
    version="1.0.0",
)
init_pool()
@app.on_event("startup")
async def startup():
    iniciar_scheduler()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount("/static", StaticFiles(directory="frontend"), name="frontend")
app.mount("/views", StaticFiles(directory="frontend/views", html=True), name="views")
app.include_router(api_router)