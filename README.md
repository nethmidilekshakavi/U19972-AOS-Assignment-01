# U19972 – Advanced Operating Systems – Assessment 1
Author: Nethmi Dilekshakavi
Module: U19972 Advanced Operating Systems – Cohort 5, Trimester 1

This repository contains three scripting-based tasks that demonstrate operating
system management techniques and automation tools, developed for AOS Assessment 1.

## Repository Structure

```
AOS_Assignment_01/
├── Task1/
│   └── task1.sh          # Smart Campus IoT Device Management (Bash)
├── Task2/
│   └── scheduler.py       # University Research Cluster Job Scheduler (Python)
├── Task3/
│   └── submission.py      # Secure Student Project Submission System (Python)
├── .gitignore
└── README.md
```

Each task generates its own log/data files at runtime (e.g. `system_monitor_log.txt`,
`job_queue.txt`, `submissions_metadata.txt`). These are excluded from version control
via `.gitignore` since they are runtime output, not source code.

---

## Prerequisites

- A Linux environment (tested on Ubuntu via WSL)
- Bash shell (for Task 1)
- Python 3 (for Task 2 and Task 3) — no external packages required, only the
  standard library (`os`, `hashlib`, `shutil`, `datetime`)

---

## Task 1 – Smart Campus IoT Device Management

**How to run:**
```bash
cd Task1
chmod +x task1.sh
./task1.sh
```

**Menu options:**
1. Display CPU and Memory Usage
2. List Top 10 Memory Consuming Processes
3. Terminate a Process (requires PID + Y/N confirmation; protects critical
   processes with PID < 100)
4. Inspect Sensor Log Directory (enter a directory path, e.g. `SensorLogs`;
   also flags any `.log` file over 50MB in the output)
5. Archive Large Log Files (detects `.log` files over 50MB and compresses
   them into `ArchiveLogs/` with a timestamped filename)
6. Check ArchiveLogs Storage (warns if the archive exceeds 1GB)
7. Bye – Exit the system (requires Y/N confirmation)

All administrative actions are logged with timestamps in `system_monitor_log.txt`.

---

## Task 2 – University Research Cluster Job Scheduler

**How to run:**
```bash
cd Task2
python3 scheduler.py
```

**Menu options:**
1. View Pending Jobs
2. Submit a Job Request (Student ID, Job Name, Execution Time in seconds,
   Priority 1–10, where 1 = highest)
3. Process Job Queue – choose either:
   - **Round Robin** – 5 second time quantum, jobs cycle through the queue
     until complete
   - **Priority Scheduling** – jobs execute in order of priority (1 first)
4. View Completed Jobs
5. Exit (requires Y/N confirmation)

Pending jobs are stored in `job_queue.txt`, completed jobs in
`completed_jobs.txt`, and all scheduling events are logged with timestamps
in `scheduler_log.txt`.

---

## Task 3 – Secure Student Project Submission System

**How to run:**
```bash
cd Task3
python3 submission.py
```

**Menu options:**
1. Submit an Assignment – validates file extension (`.pdf`/`.docx` only),
   file size (max 5MB), and rejects duplicate submissions (same filename
   and identical content, verified via SHA-256 hash)
2. Check if a File has Already been Submitted
3. List all Submitted Assignments
4. Simulate Login Attempt – demo accounts: `student1/pass123`,
   `student2/pass456`, `student3/pass789`. Accounts lock after 3 failed
   attempts, and repeated failures within 60 seconds trigger a suspicious
   activity warning.
5. Exit (requires Y/N confirmation)

Submitted files are copied into `submissions/`, metadata is recorded in
`submissions_metadata.txt`. All submission **and** login events are logged
in `submission_log.txt` (per the assessment logging requirement); login
attempts are additionally mirrored into `login_log.txt` for a dedicated,
easier-to-audit login trail.

---

## Notes

- All three scripts implement input validation and will not crash on
  invalid input (non-numeric entries, out-of-range values, missing files, etc.)
- All administrative/scheduling/submission/login events are timestamped
  and written to their respective log files for auditability.
- **Account lockout state is in-memory only** — it resets each time
  `submission.py` is restarted (no persistence layer is used for this
  simulation). This is a known design limitation, discussed in the report.
