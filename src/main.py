from fastapi import FastAPI
from src.core.init_app import create_app
from src.core.settings import get_settings
# from app.api.v1.endpoints import routine, models  # Importación de los routers

SETTINGS = get_settings()
# Crear la instancia de la aplicación
app = create_app()

# Incluir routers en la aplicación
# app.include_router(routine.router, prefix="/v1/routines", tags=["Routines"])
# app.include_router(models.router, prefix="/v1/models", tags=["Models"])

@app.get("/")
async def root():
    return {"message": f"Welcome to {SETTINGS.app_name} version {SETTINGS.version}"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=SETTINGS.debug)
