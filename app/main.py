from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import users, emotions, plans, auth, admin, context
# from app.models import users
# from app.schemas import users
# from app.database import create_db_and_tables
from app.database import create_db_and_tables

app= FastAPI(title="MENTA Backend")
origins = [
    "http://localhost:5173",  # Dirección de tu frontend
    "http://localhost",       # Opcional, si usas sin puerto explícito
    # Puedes agregar otros dominios si necesitas producción o pruebas
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Permitir estos orígenes
    allow_credentials=True,
    allow_methods=["*"],    # Permitir todos los métodos (GET, POST, etc)
    allow_headers=["*"],    # Permitir todas las cabeceras
)

@app.on_event("startup")
async def startup_event():
    await create_db_and_tables()

app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(emotions.router, prefix="/emotions", tags=["Emotions"])
app.include_router(plans.router, prefix="/plans", tags=["Plans"])
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(admin.router, prefix="/admin", tags=["Admin"])
app.include_router(context.router, prefix="/context", tags=["Context"])
