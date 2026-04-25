from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from backend.database import Base, engine
from backend.auth.auth_routes import router as auth_router
from backend.roles.role_test_routes import router as role_test_router
from backend.ai.ai_routes import router as ai_router

# ================================
# Database init
# ================================
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Crowd Monitoring Backend")

# ================================
# 🌐 CORS (REQUIRED FOR REACT)
# ================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ================================
# 🔹 Serve dataset images
# ================================
app.mount("/dataset", StaticFiles(directory="dataset"), name="dataset")

# ================================
# Register routers
# ================================
app.include_router(auth_router)
app.include_router(role_test_router)
app.include_router(ai_router)

# ================================
# 🔐 Swagger JWT Bearer Support
# ================================
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="Crowd Monitoring Backend",
        version="1.0.0",
        description="JWT-based Role Based Access Control (RBAC) + AI Crowd Analysis API",
        routes=app.routes,
    )

    openapi_schema.setdefault("components", {})
    openapi_schema["components"].setdefault("securitySchemes", {})

    openapi_schema["components"]["securitySchemes"]["BearerAuth"] = {
        "type": "http",
        "scheme": "bearer",
        "bearerFormat": "JWT",
    }

    for path, methods in openapi_schema["paths"].items():
        if path.startswith("/auth"):
            continue
        for method in methods.values():
            method["security"] = [{"BearerAuth": []}]

    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi
