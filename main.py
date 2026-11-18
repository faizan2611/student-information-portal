"""
Student Information Portal - Cloud Computing Practical Implementation
Platform: Render (PaaS)
Framework: FastAPI (Python 3)
Author: B.Tech Computer Science & Engineering
"""

import os
import time
from datetime import datetime
from typing import List, Optional
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel, Field

# ---------------------------------------------------------
# Application Initialization
# ---------------------------------------------------------
START_TIME = time.time()

app = FastAPI(
    title="Student Information Portal",
    description="A lightweight cloud-native Student Information Portal built with FastAPI and deployed on Render PaaS.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Enable CORS for cloud interoperability
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------
# Data Models (Pydantic)
# ---------------------------------------------------------
class Student(BaseModel):
    id: int
    roll_number: str
    name: str
    email: str
    department: str
    semester: int
    cgpa: float
    attendance_pct: float
    status: str = Field(description="Active, Graduated, or On-Leave")
    skills: List[str]

class HealthStatus(BaseModel):
    status: str
    service: str
    version: str
    uptime_seconds: float
    timestamp: str
    environment: str
    port: int

class StatsSummary(BaseModel):
    total_students: int
    average_cgpa: float
    highest_cgpa: float
    departments_count: int
    department_distribution: dict
    active_students_count: int
    average_attendance: float

# ---------------------------------------------------------
# Sample Dataset (In-Memory for simplicity & viva demonstration)
# ---------------------------------------------------------
STUDENTS_DATABASE: List[dict] = [
    {
        "id": 1,
        "roll_number": "21CS001",
        "name": "Aarav Sharma",
        "email": "aarav.sharma@college.edu",
        "department": "Computer Science & Engineering",
        "semester": 7,
        "cgpa": 9.42,
        "attendance_pct": 92.5,
        "status": "Active",
        "skills": ["Python", "Cloud Computing", "Docker", "FastAPI"]
    },
    {
        "id": 2,
        "roll_number": "21CS014",
        "name": "Ananya Patel",
        "email": "ananya.patel@college.edu",
        "department": "Computer Science & Engineering",
        "semester": 7,
        "cgpa": 8.85,
        "attendance_pct": 88.0,
        "status": "Active",
        "skills": ["React", "JavaScript", "REST APIs", "Git"]
    },
    {
        "id": 3,
        "roll_number": "21IT008",
        "name": "Rohan Deshmukh",
        "email": "rohan.deshmukh@college.edu",
        "department": "Information Technology",
        "semester": 7,
        "cgpa": 7.95,
        "attendance_pct": 81.2,
        "status": "Active",
        "skills": ["Networking", "Cybersecurity", "Linux", "Python"]
    },
    {
        "id": 4,
        "roll_number": "22AI003",
        "name": "Diya Nair",
        "email": "diya.nair@college.edu",
        "department": "Artificial Intelligence & Data Science",
        "semester": 5,
        "cgpa": 9.68,
        "attendance_pct": 96.0,
        "status": "Active",
        "skills": ["Machine Learning", "PyTorch", "Python", "Data Analysis"]
    },
    {
        "id": 5,
        "roll_number": "21EC025",
        "name": "Karthik Verma",
        "email": "karthik.verma@college.edu",
        "department": "Electronics & Communication",
        "semester": 7,
        "cgpa": 8.12,
        "attendance_pct": 84.5,
        "status": "Active",
        "skills": ["Embedded Systems", "IoT", "C++", "Signal Processing"]
    },
    {
        "id": 6,
        "roll_number": "22CS045",
        "name": "Sneha Mukherjee",
        "email": "sneha.m@college.edu",
        "department": "Computer Science & Engineering",
        "semester": 5,
        "cgpa": 8.70,
        "attendance_pct": 89.3,
        "status": "Active",
        "skills": ["Java", "Spring Boot", "PostgreSQL", "Cloud Basics"]
    },
    {
        "id": 7,
        "roll_number": "20CS089",
        "name": "Vikramaditya Rao",
        "email": "vikram.rao@college.edu",
        "department": "Computer Science & Engineering",
        "semester": 8,
        "cgpa": 9.15,
        "attendance_pct": 91.0,
        "status": "Graduated",
        "skills": ["Distributed Systems", "Go", "Kubernetes", "AWS"]
    },
    {
        "id": 8,
        "roll_number": "22IT019",
        "name": "Pooja Hegde",
        "email": "pooja.h@college.edu",
        "department": "Information Technology",
        "semester": 5,
        "cgpa": 8.35,
        "attendance_pct": 79.5,
        "status": "On-Leave",
        "skills": ["UI/UX Design", "Figma", "HTML/CSS", "JavaScript"]
    }
]

# Ensure static directory exists
STATIC_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")
os.makedirs(STATIC_DIR, exist_ok=True)

# Mount static directory for static assets
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# ---------------------------------------------------------
# Web Frontend Route
# ---------------------------------------------------------
@app.get("/", response_class=FileResponse, summary="Serve Web Dashboard")
def serve_dashboard():
    """Serves the primary single-page application dashboard."""
    index_file = os.path.join(STATIC_DIR, "index.html")
    if os.path.exists(index_file):
        return FileResponse(index_file)
    return JSONResponse(
        status_code=200,
        content={"message": "Student Information Portal API is running. UI template loading..."}
    )

# ---------------------------------------------------------
# Health Check Endpoint (/health) - Cloud Native Standard
# ---------------------------------------------------------
@app.get("/health", response_model=HealthStatus, tags=["Cloud Diagnostics"], summary="System Health Check")
def health_check():
    """
    Health check probe for Cloud Orchestrators (Render / Kubernetes).
    Returns uptime, service status, and deployment environment data.
    """
    current_port = int(os.environ.get("PORT", 8000))
    env_name = "Render PaaS (Production)" if os.environ.get("RENDER") else "Local Development"
    
    return HealthStatus(
        status="healthy",
        service="student-information-portal",
        version="1.0.0",
        uptime_seconds=round(time.time() - START_TIME, 2),
        timestamp=datetime.utcnow().isoformat() + "Z",
        environment=env_name,
        port=current_port
    )

# ---------------------------------------------------------
# REST API Endpoints
# ---------------------------------------------------------
@app.get("/api/students", response_model=List[Student], tags=["Students"], summary="Get All Students with Filters")
def get_students(
    search: Optional[str] = None,
    department: Optional[str] = None,
    status: Optional[str] = None,
    min_cgpa: Optional[float] = None
):
    """
    Returns list of students with optional query filtering.
    Demonstrates RESTful resource querying and query parameter parsing.
    """
    results = STUDENTS_DATABASE

    if search and isinstance(search, str):
        query = search.strip().lower()
        results = [
            s for s in results 
            if query in s["name"].lower() or query in s["roll_number"].lower()
        ]

    if department and isinstance(department, str) and department.strip() and department != "All":
        results = [s for s in results if s["department"].lower() == department.strip().lower()]

    if status and isinstance(status, str) and status.strip() and status != "All":
        results = [s for s in results if s["status"].lower() == status.strip().lower()]

    if min_cgpa is not None and isinstance(min_cgpa, (int, float)):
        results = [s for s in results if s["cgpa"] >= min_cgpa]

    return results

@app.get("/api/students/{student_id}", response_model=Student, tags=["Students"], summary="Get Student by ID")
def get_student_by_id(student_id: int):
    """
    Fetch a single student record by their primary identifier.
    Returns HTTP 404 if the student does not exist.
    """
    for student in STUDENTS_DATABASE:
        if student["id"] == student_id:
            return student
    raise HTTPException(status_code=404, detail=f"Student with ID {student_id} not found.")

@app.get("/api/stats", response_model=StatsSummary, tags=["Analytics"], summary="Get Student Statistics")
def get_statistics():
    """
    Computes aggregate metrics across student records:
    Total count, average CGPA, highest CGPA, department distribution.
    """
    total = len(STUDENTS_DATABASE)
    if total == 0:
        return StatsSummary(
            total_students=0,
            average_cgpa=0.0,
            highest_cgpa=0.0,
            departments_count=0,
            department_distribution={},
            active_students_count=0,
            average_attendance=0.0
        )

    cgpa_list = [s["cgpa"] for s in STUDENTS_DATABASE]
    attendance_list = [s["attendance_pct"] for s in STUDENTS_DATABASE]
    
    dept_dist = {}
    active_count = 0
    for s in STUDENTS_DATABASE:
        dept = s["department"]
        dept_dist[dept] = dept_dist.get(dept, 0) + 1
        if s["status"].lower() == "active":
            active_count += 1

    return StatsSummary(
        total_students=total,
        average_cgpa=round(sum(cgpa_list) / total, 2),
        highest_cgpa=round(max(cgpa_list), 2),
        departments_count=len(dept_dist),
        department_distribution=dept_dist,
        active_students_count=active_count,
        average_attendance=round(sum(attendance_list) / total, 2)
    )

@app.get("/api/cloud-info", tags=["Cloud Diagnostics"], summary="Cloud Host Environment Metadata")
def get_cloud_info():
    """
    Exposes PaaS hosting metadata to demonstrate cloud runtime awareness in viva.
    """
    return {
        "platform": "Render (Platform-as-a-Service)",
        "service_model": "PaaS (Application Managed Hosting)",
        "framework": "FastAPI (Asynchronous ASGI)",
        "server_engine": "Uvicorn",
        "python_version": os.sys.version.split()[0],
        "is_render_cloud": bool(os.environ.get("RENDER")),
        "instance_id": os.environ.get("RENDER_INSTANCE_ID", "local-dev-instance"),
        "service_id": os.environ.get("RENDER_SERVICE_ID", "local-dev-service"),
        "assigned_port": int(os.environ.get("PORT", 8000)),
        "host_bind": "0.0.0.0",
        "documentation_links": {
            "swagger_ui": "/docs",
            "redoc": "/redoc",
            "health_check": "/health"
        }
    }

# ---------------------------------------------------------
# Server Entrypoint
# ---------------------------------------------------------
if __name__ == "__main__":
    import uvicorn
    # Render dynamically assigns PORT via environment variable
    # PaaS applications MUST bind to 0.0.0.0 to receive external traffic
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False)
