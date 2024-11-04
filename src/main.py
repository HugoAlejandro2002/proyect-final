from fastapi import FastAPI
from src.core.init_app import create_app
from src.core.settings import get_settings
from src.api import routes

SETTINGS = get_settings()

app = create_app()

app.include_router(routes.router, prefix="/v1")

@app.get("/")
async def root():
    return {"message": f"Welcome to {SETTINGS.app_name} version {SETTINGS.version}"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=SETTINGS.debug)
