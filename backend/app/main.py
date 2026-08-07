from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes.auth import router as auth_router
from app.api.routes.users import router as user_router
from app.api.routes.resumes import router as resume_router
from app.api.routes.jobs import router as job_router
from app.api.routes.recommendations import router as recommendation_router
# Application metadata is defined in one place so generated API docs and client
# integrations describe the backend consistently.
app = FastAPI(
    title="SIH PMIS - AI Job Recommendation Backend",
    description="Backend API for Smart India Hackathon PMIS project",
    version="1.0.0",
)
app.include_router(auth_router)
app.include_router(user_router)
app.include_router(resume_router)
app.include_router(job_router)
app.include_router(recommendation_router)

# CORS is configured for the local frontend development servers. Credentials,
# headers, and methods are enabled so browser-based clients can call the API
# during development without route-specific CORS setup.
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Routers will be included here as the API grows.


@app.get("/")
def read_root():
    # Basic health response used to confirm the backend process is running.
    return {
        "status": "healthy",
        "message": "SIH PMIS Backend Running",
        "version": "1.0.0",
    }
