/**
 * Student Information Portal - Client Application Logic
 * Interacts with FastAPI backend hosted on Render PaaS.
 */

// Application State
let allStudents = [];
let currentFilter = {
  search: "",
  department: "All",
  status: "All"
};

// DOM Elements
const studentsTableBody = document.getElementById("studentsTableBody");
const searchInput = document.getElementById("searchInput");
const departmentFilter = document.getElementById("departmentFilter");
const statusFilter = document.getElementById("statusFilter");
const resetFiltersBtn = document.getElementById("resetFiltersBtn");
const totalStudentsStat = document.getElementById("statTotalStudents");
const avgCgpaStat = document.getElementById("statAvgCgpa");
const highestCgpaStat = document.getElementById("statHighestCgpa");
const activeStudentsStat = document.getElementById("statActiveStudents");
const avgAttendanceStat = document.getElementById("statAvgAttendance");
const healthStatusBadge = document.getElementById("healthStatusBadge");

// Modal Elements
const studentModal = document.getElementById("studentModal");
const closeModalBtn = document.getElementById("closeModalBtn");

// API Console Elements
const consoleCode = document.getElementById("consoleCode");
const consoleStatus = document.getElementById("consoleStatus");
const consoleLatency = document.getElementById("consoleLatency");
const consoleUrl = document.getElementById("consoleUrl");

// -------------------------------------------------------------
// Initialization
// -------------------------------------------------------------
document.addEventListener("DOMContentLoaded", () => {
  fetchInitialData();
  setupEventListeners();
  testApiEndpoint("/health"); // Run initial health check in console
});

function setupEventListeners() {
  searchInput.addEventListener("input", (e) => {
    currentFilter.search = e.target.value;
    applyFilters();
  });

  departmentFilter.addEventListener("change", (e) => {
    currentFilter.department = e.target.value;
    applyFilters();
  });

  statusFilter.addEventListener("change", (e) => {
    currentFilter.status = e.target.value;
    applyFilters();
  });

  resetFiltersBtn.addEventListener("click", () => {
    searchInput.value = "";
    departmentFilter.value = "All";
    statusFilter.value = "All";
    currentFilter = { search: "", department: "All", status: "All" };
    applyFilters();
  });

  closeModalBtn.addEventListener("click", () => {
    studentModal.classList.remove("open");
  });

  studentModal.addEventListener("click", (e) => {
    if (e.target === studentModal) {
      studentModal.classList.remove("open");
    }
  });
}

// -------------------------------------------------------------
// Data Fetching
// -------------------------------------------------------------
async function fetchInitialData() {
  try {
    const [studentsRes, statsRes, healthRes] = await Promise.all([
      fetch("/api/students"),
      fetch("/api/stats"),
      fetch("/health")
    ]);

    if (studentsRes.ok) {
      allStudents = await studentsRes.json();
      renderStudents(allStudents);
    }

    if (statsRes.ok) {
      const stats = await statsRes.json();
      updateStatsCards(stats);
    }

    if (healthRes.ok) {
      const health = await healthRes.json();
      updateHealthBadge(health);
    }
  } catch (error) {
    console.error("Error fetching data:", error);
    studentsTableBody.innerHTML = `
      <tr>
        <td colspan="7" style="text-align: center; padding: 2rem; color: #ef4444;">
          ⚠️ Failed to connect to server. Ensure FastAPI backend is active.
        </td>
      </tr>
    `;
  }
}

// -------------------------------------------------------------
// Render Students Table
// -------------------------------------------------------------
function renderStudents(students) {
  if (!students || students.length === 0) {
    studentsTableBody.innerHTML = `
      <tr>
        <td colspan="7" style="text-align: center; padding: 2rem; color: #64748b;">
          🔍 No student records match the selected criteria.
        </td>
      </tr>
    `;
    return;
  }

  studentsTableBody.innerHTML = students.map(student => {
    // Status Badge Class
    let statusClass = "badge-active";
    if (student.status.toLowerCase() === "graduated") statusClass = "badge-graduated";
    if (student.status.toLowerCase() === "on-leave") statusClass = "badge-leave";

    // CGPA Class
    let cgpaClass = "cgpa-avg";
    if (student.cgpa >= 9.0) cgpaClass = "cgpa-high";
    else if (student.cgpa >= 8.0) cgpaClass = "cgpa-mid";

    return `
      <tr>
        <td>
          <span style="font-family: monospace; font-weight: 600; color: #334155;">
            ${escapeHtml(student.roll_number)}
          </span>
        </td>
        <td>
          <div class="student-meta">
            <span class="student-name">${escapeHtml(student.name)}</span>
            <span class="student-email">${escapeHtml(student.email)}</span>
          </div>
        </td>
        <td>${escapeHtml(student.department)}</td>
        <td>Sem ${student.semester}</td>
        <td>
          <span class="cgpa-pill ${cgpaClass}">${student.cgpa.toFixed(2)}</span>
        </td>
        <td>
          <div>
            <span>${student.attendance_pct}%</span>
            <div class="progress-bar-bg">
              <div class="progress-bar-fill" style="width: ${student.attendance_pct}%"></div>
            </div>
          </div>
        </td>
        <td>
          <span class="badge ${statusClass}">${escapeHtml(student.status)}</span>
        </td>
        <td>
          <button class="btn-action" onclick="viewStudentDetails(${student.id})">
            Profile
          </button>
        </td>
      </tr>
    `;
  }).join("");
}

// -------------------------------------------------------------
// Filter Logic
// -------------------------------------------------------------
function applyFilters() {
  const q = currentFilter.search.trim().toLowerCase();
  const dept = currentFilter.department;
  const status = currentFilter.status;

  const filtered = allStudents.filter(student => {
    const matchesSearch = !q || 
      student.name.toLowerCase().includes(q) || 
      student.roll_number.toLowerCase().includes(q);

    const matchesDept = dept === "All" || student.department === dept;
    const matchesStatus = status === "All" || student.status.toLowerCase() === status.toLowerCase();

    return matchesSearch && matchesDept && matchesStatus;
  });

  renderStudents(filtered);
}

// -------------------------------------------------------------
// Update Stats Cards
// -------------------------------------------------------------
function updateStatsCards(stats) {
  if (totalStudentsStat) totalStudentsStat.textContent = stats.total_students;
  if (avgCgpaStat) avgCgpaStat.textContent = stats.average_cgpa.toFixed(2);
  if (highestCgpaStat) highestCgpaStat.textContent = stats.highest_cgpa.toFixed(2);
  if (activeStudentsStat) activeStudentsStat.textContent = stats.active_students_count;
  if (avgAttendanceStat) avgAttendanceStat.textContent = stats.average_attendance + "%";
}

function updateHealthBadge(health) {
  if (healthStatusBadge) {
    healthStatusBadge.innerHTML = `
      <span class="badge-pulse"></span>
      <span>${health.environment}</span>
    `;
  }
}

// -------------------------------------------------------------
// View Student Details Modal
// -------------------------------------------------------------
function viewStudentDetails(studentId) {
  const student = allStudents.find(s => s.id === studentId);
  if (!student) return;

  document.getElementById("modalStudentName").textContent = student.name;
  document.getElementById("modalStudentRoll").textContent = student.roll_number;
  document.getElementById("modalStudentEmail").textContent = student.email;
  document.getElementById("modalStudentDept").textContent = student.department;
  document.getElementById("modalStudentSem").textContent = `Semester ${student.semester}`;
  document.getElementById("modalStudentCgpa").textContent = `${student.cgpa} / 10.0`;
  document.getElementById("modalStudentAttendance").textContent = `${student.attendance_pct}%`;
  document.getElementById("modalStudentStatus").textContent = student.status;

  const skillsContainer = document.getElementById("modalStudentSkills");
  skillsContainer.innerHTML = student.skills.map(skill => 
    `<span class="skill-tag">${escapeHtml(skill)}</span>`
  ).join("");

  studentModal.classList.add("open");
}

// -------------------------------------------------------------
// Interactive API Testing Console
// -------------------------------------------------------------
async function testApiEndpoint(endpointPath) {
  // Update active button state
  document.querySelectorAll(".btn-endpoint").forEach(btn => {
    btn.classList.toggle("active", btn.dataset.endpoint === endpointPath);
  });

  consoleUrl.textContent = endpointPath;
  consoleStatus.textContent = "Connecting...";
  consoleLatency.textContent = "-";
  consoleCode.textContent = "Sending GET request to " + endpointPath + "...";

  const startTime = performance.now();
  try {
    const response = await fetch(endpointPath);
    const endTime = performance.now();
    const duration = Math.round(endTime - startTime);

    consoleLatency.textContent = `${duration} ms`;
    consoleStatus.textContent = `HTTP ${response.status} ${response.statusText}`;
    consoleStatus.style.color = response.ok ? "#34d399" : "#f87171";

    const json = await response.json();
    consoleCode.textContent = JSON.stringify(json, null, 2);
  } catch (err) {
    consoleStatus.textContent = "Request Failed";
    consoleStatus.style.color = "#f87171";
    consoleCode.textContent = `Error: ${err.message}`;
  }
}

// -------------------------------------------------------------
// Utility Functions
// -------------------------------------------------------------
function escapeHtml(str) {
  if (!str) return "";
  return String(str)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
}
