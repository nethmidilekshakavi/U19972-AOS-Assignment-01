#!/usr/bin/env python3

import os
import hashlib
from datetime import datetime

SUBMISSIONS_DIR = "submissions"
METADATA_FILE = "submissions_metadata.txt"
SUBMISSION_LOG_FILE = "submission_log.txt"
LOGIN_LOG_FILE = "login_log.txt"

MAX_FILE_SIZE_MB = 5
ALLOWED_EXTENSIONS = (".pdf", ".docx")
MAX_FAILED_ATTEMPTS = 3
SUSPICIOUS_WINDOW_SECONDS = 60

# Simulated user directory for the login demo (assignment says "simulate login attempt")
VALID_USERS = {
    "student1": "pass123",
    "student2": "pass456",
    "student3": "pass789"
}

# In-memory tracking for the current script session
failed_attempts = {}   # username -> list of datetime objects (failed attempt timestamps)
locked_accounts = set()  # usernames currently locked out


def ensure_setup():
    """Create required files/directories if they don't already exist"""
    os.makedirs(SUBMISSIONS_DIR, exist_ok=True)
    for filename in (METADATA_FILE, SUBMISSION_LOG_FILE, LOGIN_LOG_FILE):
        if not os.path.exists(filename):
            open(filename, "a").close()


def log_submission(event):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(SUBMISSION_LOG_FILE, "a") as f:
        f.write(f"{timestamp} - {event}\n")


def log_login(username, event):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOGIN_LOG_FILE, "a") as f:
        f.write(f"{timestamp} - User: {username} - {event}\n")


def submit_assignment():
    print("\n========== Submit an Assignment ==========")
    # TODO: ask for file path, validate extension/size, check duplicates, save
    print("(not implemented yet)")


def check_submission():
    print("\n========== Check if File Already Submitted ==========")
    # TODO: ask for filename, check metadata file
    print("(not implemented yet)")


def list_submissions():
    print("\n========== All Submitted Assignments ==========")
    # TODO: read and display metadata file
    print("(not implemented yet)")


def simulate_login():
    print("\n========== Simulate Login Attempt ==========")
    # TODO: username/password check, lockout logic, suspicious detection
    print("(not implemented yet)")


def main():
    ensure_setup()

    while True:
        print("\n======================================")
        print(" Secure Student Project Submission System")
        print("======================================")
        print("1. Submit an Assignment")
        print("2. Check if a File has Already been Submitted")
        print("3. List all Submitted Assignments")
        print("4. Simulate Login Attempt")
        print("5. Exit")
        print("======================================")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            submit_assignment()
        elif choice == "2":
            check_submission()
        elif choice == "3":
            list_submissions()
        elif choice == "4":
            simulate_login()
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
