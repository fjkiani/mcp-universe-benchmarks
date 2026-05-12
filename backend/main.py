"""Backend API Gateway - FastAPI server"""
from dotenv import load_dotenv
load_dotenv()  # Must be before any service imports that read env vars

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routers import servers, sprint, tasks, central, healthcare_demo, auth, users, patients, appointments, dashboard, video, video_consultations, demos, scoring
from api.routers.healthcare_agent import router as agent_router
from api.routers.identity_agent import router as identity_router
from api.routers.certification import router as certification_router
from database.session import init_db

app = FastAPI(
    title="Healthcare Receptionist AI API",
    description="Backend API Gateway for Healthcare Receptionist AI",
    version="1.0.0",
)

# Initialize database on startup
@app.on_event("startup")
async def startup_event():
    init_db()

# CORS — allow specific origins for production Vercel frontend and local dev
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:3001",
        "https://clear-mind-life.vercel.app",
        "https://zeta-saas-frontend.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(servers.router, prefix="/api/v1/servers", tags=["servers"])
app.include_router(sprint.router, prefix="/api/v1/sprint", tags=["sprint"])
app.include_router(tasks.router, prefix="/api/v1/tasks", tags=["tasks"])
app.include_router(central.router, prefix="/api/v1/central", tags=["central"])
app.include_router(demos.router, prefix="/api/v1/demos", tags=["demos"])
app.include_router(healthcare_demo.router)
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(patients.router)
app.include_router(appointments.router)
app.include_router(dashboard.router)
app.include_router(video.router)
app.include_router(video_consultations.router)
app.include_router(agent_router)    # Healthcare AI Agent (psychiatric + dental)
app.include_router(identity_router) # Identity Agent (MFA, RBAC, Compliance)
app.include_router(certification_router)  # Agent Governance Engine (UL for AI)
app.include_router(scoring.router, prefix="/api/v1", tags=["scoring"])  # FDA VVUQ Scoring Engine


@app.get("/")
async def root():
    return {
        "message": "Healthcare Receptionist AI API Gateway",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health",
    }


@app.get("/health")
async def health():
    return {"status": "healthy", "service": "api-gateway"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True)
