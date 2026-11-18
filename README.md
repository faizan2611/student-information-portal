# Student Information Portal 🎓☁️
### Exploration and Practical Implementation of Cloud Computing using Render (PaaS)

---

## 📌 1. Project Handover & Executive Summary

### What does this project do?
The **Student Information Portal** is a production-grade, lightweight academic management system and cloud diagnostic platform. It provides:
1. **Interactive Academic Dashboard:** Displays enrolled student profiles, academic standings (CGPA categories), attendance tracking, and individual department distribution.
2. **Real-Time Search & Multi-Criteria Filtering:** Live filtering of student records by student name, roll number, department, or enrollment status.
3. **Aggregate Analytics Engine:** Real-time calculation of campus-wide academic metrics (Average CGPA, Highest CGPA, Active student counts).
4. **Cloud Health & Liveness Probe (`/health`):** Diagnostic endpoint returning system uptime, process environment, and active listening port for cloud orchestrators.
5. **Interactive In-Browser REST API Explorer:** A live testing console directly inside the web UI where evaluators can trigger requests to backend endpoints and measure roundtrip network latency in milliseconds.
6. **Auto-Generated OpenAPI / Swagger Documentation (`/docs`):** Interactive API documentation for developers and examiners.

---

## ⚙️ 2. How Does This Project Work? (System Architecture)

```
[ User Web Browser / Client ]
             │
             │ HTTPS Request (e.g. GET /api/students)
             ▼
[ Render Cloud Edge: Cloudflare Reverse Proxy & TLS Termination ]
             │
             │ Internal TCP Routing to dynamic port (e.g. 10000)
             ▼
[ Isolated Linux Container Sandbox on Render ]
             │
             │ Environment: $PORT (assigned by Render orchestrator)
             ▼
[ ASGI Server: Uvicorn (Bound to 0.0.0.0:$PORT) ]
             │
             ▼
[ FastAPI Application Core (main.py) ]
   ├── Static File Handler (/) ─────────────► Serves static/index.html & CSS/JS
   ├── Health Check (/health) ──────────────► Orchestrator Liveness Probe
   ├── Students Resource (/api/students) ───► Query Parsing & JSON Serialization
   ├── Aggregate Stats (/api/stats) ────────► Computes CGPA & Dept Distribution
   └── Diagnostics (/api/cloud-info) ───────► PaaS Runtime Metadata
```

### Component Breakdown:
- **Backend Framework:** **FastAPI** (Python 3.9+). Provides native asynchronous request processing, automatic JSON schema serialization, and Pydantic validation.
- **Server Engine:** **Uvicorn**, a lightning-fast ASGI (Asynchronous Server Gateway Interface) web server implementation based on `uvloop` and `httptools`.
- **Frontend Architecture:** Modern HTML5, CSS3 (CSS Variables, Flexbox, Grid), and Vanilla JavaScript (Fetch API). Decoupled from backend templates, ensuring clean separation of concerns.
- **Data Layer:** High-cohesion in-memory data store containing realistic B.Tech student records. Eliminates external database dependencies, preventing database connection timeouts during college presentations.

---

## ☁️ 3. Where is the "Cloud" in This Project?

To explain this project to your professor, highlight these **5 concrete Cloud Computing pillars**:

### Pillar 1: Platform-as-a-Service (PaaS) Model
Instead of renting a bare-metal physical machine or unmanaged virtual machine (IaaS) where you must configure Linux kernels, firewalls, and systemd services, this application runs on **Render PaaS**. Render manages the physical hardware, hypervisors, OS patching, and network routing. You provide only source code and dependency manifests (`requirements.txt`).

### Pillar 2: Dynamic Port Binding (`$PORT`) & `0.0.0.0` Host
In cloud environments, containers do not run on fixed port 80 or 8000. The cloud orchestrator dynamically assigns an available port at container launch via the `PORT` environment variable.
- Our application dynamically reads this via `port = int(os.environ.get("PORT", 8000))`.
- Our application binds to `0.0.0.0` (all interfaces) rather than `127.0.0.1` (localhost only). This enables the cloud edge reverse proxy to forward external internet traffic into the container.

### Pillar 3: Cloud Liveness Probe (`/health`)
Modern cloud platforms (Render, Kubernetes, AWS ECS) require an automated health check probe. Render continuously sends HTTP GET requests to `/health`. If the endpoint returns HTTP 200, Render marks the container healthy and routes user traffic to it. During updates, Render performs **zero-downtime rolling deployments** by ensuring the new container passes `/health` before shutting down the old container.

### Pillar 4: Automated CI/CD (GitOps)
Whenever code is pushed to the GitHub repository, GitHub emits an automated webhook to Render. Render instantly spins up an isolated build container, executes `pip install -r requirements.txt`, runs health checks, and promotes the build to production automatically.

### Pillar 5: Infrastructure as Code (IaC) via `render.yaml`
The entire cloud infrastructure is defined declaratively in [`render.yaml`](file:///Users/apple/Desktop/project/render.yaml). Render reads this file to provision the service, configure Python 3.11 runtime, set build/start commands, and apply the free tier automatically.

---

## 🚀 4. How to Upload Files to GitHub (Fastest 30-Second Web Method)

Because you are already logged in to GitHub in your browser, this is the quickest zero-error way:

1. Open your repository page in your browser:  
   👉 **[https://github.com/faizan2611/student-information-portal](https://github.com/faizan2611/student-information-portal)**
2. In the center of the empty repository page, click the link:  
   **"uploading an existing file"**  
   *(Direct URL: `https://github.com/faizan2611/student-information-portal/upload/main`)*
3. On your Mac, open Finder and navigate to:  
   `Desktop` &rarr; `project`
4. Select all these files and drag them into the GitHub upload box:
   - `main.py`
   - `requirements.txt`
   - `render.yaml`
   - `README.md`
   - `ASSIGNMENT_REPORT.md`
   - `.gitignore`
   - `static` folder (containing `index.html`, `css/`, `js/`)
5. Scroll down to **Commit changes**, leave it on *Commit directly to the `main` branch*, and click the green **Commit changes** button.

*(Alternatively, if you prefer terminal, run `git push -u origin main` in your terminal with your GitHub Personal Access Token).*

---

## 🌐 5. Exact Steps to Deploy on Render (1-Click Blueprint)

Once the files are on your GitHub repository:

### Method A: The 1-Click Blueprint Link (Recommended)
1. In your browser, open this exact URL:  
   👉 **[https://render.com/deploy?repo=https://github.com/faizan2611/student-information-portal](https://render.com/deploy?repo=https://github.com/faizan2611/student-information-portal)**
2. Render reads [`render.yaml`](file:///Users/apple/Desktop/project/render.yaml) automatically:
   - It pre-populates the service name: `student-information-portal`
   - It configures Python runtime, build command, and start command.
3. Click **Apply** or **Create Web Service**.

---

### Method B: Manual Dashboard Setup (Alternative)
1. Go to **[https://dashboard.render.com](https://dashboard.render.com)**.
2. Click **New +** (top right) &rarr; Select **Web Service**.
3. Choose **Build and deploy from a Git repository**.
4. Select your repository: `faizan2611/student-information-portal`.
5. Enter these exact parameters:
   - **Name:** `student-information-portal`
   - **Region:** `Oregon (US West)` or `Frankfurt (EU)`
   - **Branch:** `main`
   - **Runtime:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Plan:** `Free`
6. Click **Advanced** &rarr; In **Health Check Path**, enter: `/health`
7. Click **Create Web Service**.

---

## ⏱️ 6. What to Expect During Deployment & Getting Your Link

1. Render will spin up a build container and stream live logs:
   ```text
   ==> Cloning from https://github.com/faizan2611/student-information-portal...
   ==> Running build command 'pip install -r requirements.txt'...
   Successfully installed fastapi uvicorn pydantic aiofiles...
   ==> Running start command 'uvicorn main:app --host 0.0.0.0 --port $PORT'...
   INFO:     Started server process
   INFO:     Application startup complete.
   INFO:     Uvicorn running on http://0.0.0.0:10000
   ==> Your service is live 🎉
   ```
2. At the top left of the Render dashboard, you will see your live public URL:  
   **`https://student-information-portal-xxxx.onrender.com`**
3. Open that URL in your browser to verify:
   - **Web UI:** `https://<YOUR-RENDER-URL>.onrender.com/`
   - **Health Check:** `https://<YOUR-RENDER-URL>.onrender.com/health`
   - **Swagger Docs:** `https://<YOUR-RENDER-URL>.onrender.com/docs`

---

## 🎯 7. Viva Voce Cheat-Sheet (Full 2 Marks)

Be ready to answer these 4 questions when your professor evaluates your submission:

1. **Why is Render classified as PaaS?**  
   *Answer:* Render abstracts underlying hardware, hypervisors, OS security updates, and web server reverse proxies. We only supply source code and dependency manifests.
2. **Why must the server bind to `0.0.0.0`?**  
   *Answer:* `127.0.0.1` only accepts internal container connections. `0.0.0.0` listens on all network interfaces, allowing Render's edge reverse proxy to route public incoming traffic to Uvicorn.
3. **What is the function of `$PORT`?**  
   *Answer:* Render dynamically assigns a port at boot time (e.g. 10000). Our application reads `os.environ.get("PORT")` so it binds to the port assigned by the cloud orchestrator.
4. **What is the role of `/health`?**  
   *Answer:* It acts as a cloud liveness probe. Render continually pings `/health` to verify that the container is healthy before routing incoming traffic to it.
