from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import sub apps
from ai_services.main import app as ai_app
from user.main import app as user_app

app = FastAPI(title="AI Crowd Monitoring System")

# Allow frontend access (React)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development only
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount AI routes
app.mount("/ai", ai_app)

# Mount Auth/User routes
app.mount("/auth", user_app)

@app.get("/")
def root():
    return {"message": "Main Backend Running"}
