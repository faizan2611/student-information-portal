# Student Information Portal 🎓☁️

> **B.Tech Computer Science & Engineering — Cloud Computing Tool Explorer Assignment**  
> **Topic:** Exploration and Practical Implementation of Cloud Computing using Render (PaaS)  
> **Framework:** Python / FastAPI / Modern Responsive Vanilla JavaScript  

---

## 📌 Executive Summary

The **Student Information Portal** is a cloud-native, lightweight web application and REST API engineered to demonstrate modern **Platform-as-a-Service (PaaS)** hosting concepts using **Render**. It delivers an interactive academic records dashboard with live search, department filtering, aggregate academic statistics, and cloud health monitoring endpoints.

### 🌟 Key Capabilities
- **Responsive Dashboard:** Modern UI displaying enrolled students, CGPA classifications, attendance tracking, and individual academic profiles.
- **RESTful API Backend:** High-performance asynchronous endpoints powered by Python and FastAPI.
- **Cloud Health Diagnostics:** Automated `/health` endpoint returning uptime, deployment environment, and service status for cloud orchestrators.
- **Interactive REST Console:** Built-in live API playground allowing evaluators to execute requests and observe roundtrip network latency directly from the browser.
- **PaaS Optimized:** Designed with zero external database baggage for robust, zero-configuration cloud deployment on Render's free tier.

---

## 🏛️ System Architecture & Request Lifecycle

```
[ User Browser / Client ]
           │
           │  (HTTPS on Port 443)
           ▼
[ Cloudflare / Render Edge Reverse Proxy & TLS Termination ]
           │
           │  (Internal routing to container port)
           ▼
[ Render Managed Container Environment (Ubuntu / Linux) ]
           │
           │  (PORT Environment Variable, e.g., 10000)
           ▼
[ ASGI Server: Uvicorn (Bound to 0.0.0.0:$PORT) ]
           │
           ▼
[ FastAPI Application Core (main.py) ]
   ├── Static Files Route (/) ─────────────► Serves HTML / CSS / JS
   ├── Health Check Route (/health) ───────► Orchestrator Liveness Probe
   ├── Students Resource (/api/students) ──► Query Filtering & Serialization
   ├── Analytics (/api/stats) ─────────────► Real-time Academic Metrics
   └── Metadata (/api/cloud-info) ─────────► PaaS Runtime Diagnostics
```

---

## 📂 Repository File Structure

```
project/
├── main.py              # FastAPI application core, routes, and data models
├── requirements.txt     # Python production dependencies (FastAPI, Uvicorn, Pydantic)
├── render.yaml          # Render Blueprint (Infrastructure-as-Code specification)
├── .gitignore           # Git ignore rules for Python, virtual environments, and OS files
├── README.md            # Comprehensive project documentation & deployment guide
├── ASSIGNMENT_REPORT.md # 10-Mark Academic Submission Report
└── static/
    ├── index.html       # Single Page Application (SPA) dashboard & API console
    ├── css/
    │   └── style.css    # Responsive modern design system
    └── js/
        └── app.js       # Asynchronous client logic, filtering, and API runner
```

---

## 🚀 Local Development Setup

To test and run the project locally before deploying to the cloud:

### 1. Clone or Open the Workspace
```bash
cd /Users/apple/Desktop/project
```

### 2. Create and Activate a Python Virtual Environment
```bash
# macOS / Linux
python3 -m venv venv
source venv/bin/activate

# Windows (PowerShell)
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Launch the Server
```bash
python main.py
```
*Alternatively, start using Uvicorn directly:*
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### 5. Access the Application
- **Web Dashboard:** [http://localhost:8000](http://localhost:8000)
- **Health Check Endpoint:** [http://localhost:8000/health](http://localhost:8000/health)
- **Interactive Swagger API Docs:** [http://localhost:8000/docs](http://localhost:8000/docs)
- **Alternative ReDoc UI:** [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## ☁️ Step-by-Step Render Cloud Deployment Guide

Follow these exact steps to deploy this application to Render:

### Step 1: Initialize Git and Commit the Project
Open your terminal in the project root:
```bash
git init
git add .
git commit -m "feat: initial release of student information portal for Render PaaS"
```

### Step 2: Push to GitHub
1. Open [GitHub](https://github.com) and create a new public repository named `student-information-portal`.
2. Link your local project to GitHub and push your code:
```bash
git branch -M main
git remote add origin https://github.com/<YOUR_GITHUB_USERNAME>/student-information-portal.git
git push -u origin main
```

### Step 3: Sign In to Render
1. Navigate to [https://render.com](https://render.com).
2. Click **Get Started** or **Sign In** using your GitHub account (this grants Render read access to your repositories).

### Step 4: Create a New Web Service
1. On the Render Dashboard, click the blue **New +** button in the upper right.
2. Select **Web Service**.
3. Choose **Build and deploy from a Git repository**.
4. Select your `student-information-portal` repository from the list.

### Step 5: Configure Service Parameters
Fill in the deployment configuration:

| Field | Configuration Value | Explanation |
| :--- | :--- | :--- |
| **Name** | `student-information-portal` | Unique service name (determines your URL) |
| **Region** | `Oregon (US West)` or `Frankfurt (EU)` | Pick the region closest to you |
| **Branch** | `main` | Production deployment branch |
| **Root Directory** | *(Leave blank)* | Uses root repository directory |
| **Runtime** | `Python 3` | Specifies the managed Python runtime environment |
| **Build Command** | `pip install -r requirements.txt` | Installs FastAPI, Uvicorn, and dependencies |
| **Start Command** | `uvicorn main:app --host 0.0.0.0 --port $PORT` | Binds server to Render's dynamic port |
| **Instance Type** | `Free` | Zero cost cloud tier (0.1 CPU, 512 MB RAM) |

> 💡 **Advanced Settings (Optional):**
> - Under **Health Check Path**, enter: `/health`
> - Under **Environment Variables**, you can optionally set:
>   - `PYTHON_VERSION`: `3.11.9`

### Step 6: Deploy and Monitor Logs
1. Click **Create Web Service**.
2. Render will trigger an automated build pipeline:
   - Cloning Git repository
   - Creating isolated container
   - Executing `pip install -r requirements.txt`
   - Executing start command
   - Polling `/health`
3. Watch the live **Logs** tab until you see:
   ```
   INFO:     Started server process [PID]
   INFO:     Waiting for application startup.
   INFO:     Application startup complete.
   INFO:     Uvicorn running on http://0.0.0.0:10000
   ==> Your service is live 🎉
   ```

### Step 7: Verify Public Production Endpoints
Render provisions a free public HTTPS domain:
`https://student-information-portal-<unique-hash>.onrender.com`

Verify each endpoint in your browser or with curl:
1. **Frontend Portal:** `https://<YOUR-RENDER-URL>.onrender.com/`
2. **Health Probe:** `https://<YOUR-RENDER-URL>.onrender.com/health`
3. **Student Roster API:** `https://<YOUR-RENDER-URL>.onrender.com/api/students`
4. **Statistics API:** `https://<YOUR-RENDER-URL>.onrender.com/api/stats`
5. **Interactive Swagger Docs:** `https://<YOUR-RENDER-URL>.onrender.com/docs`

---

## 🧪 REST API Reference Summary

| Method | Endpoint | Description | Sample Output / Query Params |
| :--- | :--- | :--- | :--- |
| `GET` | `/` | Web Application Dashboard | HTML / CSS / JS Single Page App |
| `GET` | `/health` | Cloud Liveness & Health Probe | `{"status": "healthy", "uptime_seconds": 124.5, "environment": "Render PaaS (Production)"}` |
| `GET` | `/api/students` | Get all students with filtering | Query params: `search`, `department`, `status`, `min_cgpa` |
| `GET` | `/api/students/{id}` | Get student profile by ID | Returns student object or 404 error |
| `GET` | `/api/stats` | Academic aggregate statistics | Total count, avg CGPA, dept distribution |
| `GET` | `/api/cloud-info` | PaaS runtime environment info | Host bind, assigned port, runtime info |
| `GET` | `/docs` | OpenAPI / Swagger UI | Interactive documentation |

---

## 🎯 Viva Quick Reference Cheatsheet

1. **Why is Render considered PaaS?**
   - Render abstracts hardware, OS patching, hypervisors, and network routing. Developers only supply their application code and a build/start command.
2. **Why must the server bind to `0.0.0.0` instead of `127.0.0.1`?**
   - `127.0.0.1` (localhost) only accepts connections originating from inside the container itself. `0.0.0.0` instructs the socket to listen on all network interfaces, allowing Render's external reverse proxy to route public traffic into the container.
3. **What is the function of the `PORT` environment variable?**
   - Render dynamically assigns a port (e.g., 10000) inside the container at startup. Hardcoding port 8000 would cause deployment failure; using `$PORT` ensures dynamic compatibility.
4. **What is a Cloud Health Check (`/health`)?**
   - A lightweight HTTP endpoint pinged periodically by cloud orchestrators. If it returns HTTP 200, the instance is marked healthy and receives incoming user traffic; otherwise, the orchestrator triggers a restart or routes traffic elsewhere.
