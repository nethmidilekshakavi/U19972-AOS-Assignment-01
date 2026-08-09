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
    # TODO: read and display job_queue.txt
    print("(not implemented yet)")


def submit_job():
    print("\n========== Submit a Job Request ==========")
    # TODO: ask for student ID, job name, exec time, priority
    print("(not implemented yet)")


def process_job_queue():
    print("\n========== Process Job Queue ==========")
    # TODO: ask for Round Robin or Priority, then run scheduling
    print("(not implemented yet)")


def view_completed_jobs():
    print("\n========== Completed Jobs ==========")
    # TODO: read and display completed_jobs.txt
    print("(not implemented yet)")


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
