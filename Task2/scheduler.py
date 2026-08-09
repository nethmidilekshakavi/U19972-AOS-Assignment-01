#!/usr/bin/env python3

import os
from datetime import datetime

JOB_QUEUE_FILE = "job_queue.txt"
COMPLETED_JOBS_FILE = "completed_jobs.txt"
LOG_FILE = "scheduler_log.txt"


def log_action(student_id, job_name, scheduling_type, event):
    """Append a timestamped entry to scheduler_log.txt"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as f:
        f.write(f"{timestamp} - {event} | Student: {student_id} | Job: {job_name} | Type: {scheduling_type}\n")


def ensure_files_exist():
    """Create the data files if they don't already exist"""
    for filename in (JOB_QUEUE_FILE, COMPLETED_JOBS_FILE, LOG_FILE):
        if not os.path.exists(filename):
            open(filename, "a").close()


def view_pending_jobs():
    print("\n========== Pending Jobs ==========")

    if not os.path.exists(JOB_QUEUE_FILE) or os.path.getsize(JOB_QUEUE_FILE) == 0:
        print("No pending jobs.")
        return

    print(f"{'Student ID':<12}{'Job Name':<20}{'Exec Time(s)':<14}{'Priority':<10}")
    with open(JOB_QUEUE_FILE, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            student_id, job_name, exec_time, priority = line.split("|")
            print(f"{student_id:<12}{job_name:<20}{exec_time:<14}{priority:<10}")


def submit_job():
    print("\n========== Submit a Job Request ==========")

    student_id = input("Enter Student ID: ").strip()
    if not student_id:
        print("Student ID cannot be empty.")
        return

    job_name = input("Enter Job Name: ").strip()
    if not job_name:
        print("Job Name cannot be empty.")
        return

    exec_time_input = input("Enter Estimated Execution Time (seconds): ").strip()
    if not exec_time_input.isdigit() or int(exec_time_input) <= 0:
        print("Invalid execution time. Must be a positive whole number.")
        return
    exec_time = int(exec_time_input)

    priority_input = input("Enter Priority (1 = highest, 10 = lowest): ").strip()
    if not priority_input.isdigit() or not (1 <= int(priority_input) <= 10):
        print("Invalid priority. Must be a number between 1 and 10.")
        return
    priority = int(priority_input)

    with open(JOB_QUEUE_FILE, "a") as f:
        f.write(f"{student_id}|{job_name}|{exec_time}|{priority}\n")

    log_action(student_id, job_name, "N/A", "Job submitted")
    print(f"Job '{job_name}' submitted successfully for student {student_id}.")


def load_pending_jobs():
    """Read job_queue.txt into a list of job dicts"""
    jobs = []
    if os.path.exists(JOB_QUEUE_FILE):
        with open(JOB_QUEUE_FILE, "r") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                student_id, job_name, exec_time, priority = line.split("|")
                jobs.append({
                    "student_id": student_id,
                    "job_name": job_name,
                    "exec_time": int(exec_time),
                    "priority": int(priority)
                })
    return jobs


def save_pending_jobs(jobs):
    """Overwrite job_queue.txt with whatever jobs remain (usually empty after processing)"""
    with open(JOB_QUEUE_FILE, "w") as f:
        for job in jobs:
            f.write(f"{job['student_id']}|{job['job_name']}|{job['exec_time']}|{job['priority']}\n")


def mark_job_completed(job, scheduling_type):
    """Append a finished job to completed_jobs.txt and the scheduler log"""
    completion_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(COMPLETED_JOBS_FILE, "a") as f:
        f.write(f"{job['student_id']}|{job['job_name']}|{job['exec_time']}|{job['priority']}|{scheduling_type}|{completion_time}\n")
    log_action(job["student_id"], job["job_name"], scheduling_type, "Job completed")


def run_round_robin(jobs):
    QUANTUM = 5
    queue = jobs[:]  # simple list used as a FIFO queue
    for job in queue:
        job["remaining"] = job["exec_time"]

    print(f"\nRunning Round Robin scheduling (time quantum = {QUANTUM}s)...\n")

    while queue:
        job = queue.pop(0)
        if job["remaining"] <= QUANTUM:
            print(f"Job '{job['job_name']}' (Student {job['student_id']}) COMPLETED "
                  f"(ran final {job['remaining']}s).")
            mark_job_completed(job, "Round Robin")
        else:
            job["remaining"] -= QUANTUM
            print(f"Job '{job['job_name']}' (Student {job['student_id']}) ran {QUANTUM}s, "
                  f"{job['remaining']}s remaining - back of queue.")
            queue.append(job)


def run_priority_scheduling(jobs):
    print("\nRunning Priority scheduling (1 = highest priority first)...\n")

    sorted_jobs = sorted(jobs, key=lambda j: j["priority"])
    for job in sorted_jobs:
        print(f"Job '{job['job_name']}' (Student {job['student_id']}, Priority {job['priority']}) COMPLETED.")
        mark_job_completed(job, "Priority")


def process_job_queue():
    print("\n========== Process Job Queue ==========")

    jobs = load_pending_jobs()
    if not jobs:
        print("No pending jobs to process.")
        return

    print("1. Round Robin")
    print("2. Priority Scheduling")
    choice = input("Choose scheduling algorithm: ").strip()

    if choice == "1":
        run_round_robin(jobs)
    elif choice == "2":
        run_priority_scheduling(jobs)
    else:
        print("Invalid choice. Returning to menu.")
        return

    save_pending_jobs([])  # all jobs have been processed
    print("\nAll jobs processed. Queue is now empty.")


def view_completed_jobs():
    print("\n========== Completed Jobs ==========")

    if not os.path.exists(COMPLETED_JOBS_FILE) or os.path.getsize(COMPLETED_JOBS_FILE) == 0:
        print("No completed jobs yet.")
        return

    print(f"{'Student ID':<12}{'Job Name':<20}{'Exec Time(s)':<14}{'Priority':<10}{'Type':<14}{'Completed At'}")
    with open(COMPLETED_JOBS_FILE, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            student_id, job_name, exec_time, priority, sched_type, completed_at = line.split("|")
            print(f"{student_id:<12}{job_name:<20}{exec_time:<14}{priority:<10}{sched_type:<14}{completed_at}")


def main():
    ensure_files_exist()

    while True:
        print("\n======================================")
        print(" University Research Cluster Job Scheduler")
        print("======================================")
        print("1. View Pending Jobs")
        print("2. Submit a Job Request")
        print("3. Process Job Queue")
        print("4. View Completed Jobs")
        print("5. Exit")
        print("======================================")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            view_pending_jobs()
        elif choice == "2":
            submit_job()
        elif choice == "3":
            process_job_queue()
        elif choice == "4":
            view_completed_jobs()
        elif choice == "5":
            confirm = input("Are you sure you want to exit? (Y/N): ").strip().lower()
            if confirm == "y":
                print("Goodbye!")
                break
            else:
                print("Exit cancelled.")
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
