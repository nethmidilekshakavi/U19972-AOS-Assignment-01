#!/usr/bin/env python3

import os
import shutil
import hashlib
from datetime import datetime, timedelta

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
    """
    Login events are written to BOTH files:
      - submission_log.txt  -> required by the assignment rubric, which states
        that ALL submission AND login events must be recorded in submission_log.txt
      - login_log.txt       -> kept as a dedicated, easier-to-audit login trail
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(LOGIN_LOG_FILE, "a") as f:
        f.write(f"{timestamp} - User: {username} - {event}\n")

    # Mirror into submission_log.txt to satisfy the rubric wording
    log_submission(f"LOGIN - User: {username} - {event}")


def compute_file_hash(filepath):
    """Compute a SHA-256 hash of the file's content for duplicate detection"""
    sha256 = hashlib.sha256()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            sha256.update(chunk)
    return sha256.hexdigest()


def load_metadata():
    """Read submissions_metadata.txt into a list of dicts"""
    records = []
    if os.path.exists(METADATA_FILE):
        with open(METADATA_FILE, "r") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                student_id, filename, size_bytes, file_hash, timestamp = line.split("|")
                records.append({
                    "student_id": student_id,
                    "filename": filename,
                    "size_bytes": int(size_bytes),
                    "hash": file_hash,
                    "timestamp": timestamp
                })
    return records


def append_metadata(student_id, filename, size_bytes, file_hash):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(METADATA_FILE, "a") as f:
        f.write(f"{student_id}|{filename}|{size_bytes}|{file_hash}|{timestamp}\n")


def submit_assignment():
    print("\n========== Submit an Assignment ==========")

    student_id = input("Enter Student ID: ").strip()
    if not student_id:
        print("Student ID cannot be empty.")
        return

    file_path = input("Enter path to the file you want to submit: ").strip()

    if not os.path.isfile(file_path):
        print("File does not exist.")
        log_submission(f"FAILED - Student: {student_id} - File not found: {file_path}")
        return

    filename = os.path.basename(file_path)
    ext = os.path.splitext(filename)[1].lower()

    # 1. Validate extension
    if ext not in ALLOWED_EXTENSIONS:
        print(f"Invalid file type '{ext}'. Only {', '.join(ALLOWED_EXTENSIONS)} files are accepted.")
        log_submission(f"REJECTED - Student: {student_id} - File: {filename} - Reason: invalid extension")
        return

    # 2. Validate size
    size_bytes = os.path.getsize(file_path)
    size_mb = size_bytes / (1024 * 1024)
    if size_mb > MAX_FILE_SIZE_MB:
        print(f"File too large ({size_mb:.2f} MB). Maximum allowed size is {MAX_FILE_SIZE_MB} MB.")
        log_submission(f"REJECTED - Student: {student_id} - File: {filename} - Reason: exceeds {MAX_FILE_SIZE_MB}MB")
        return

    # 3. Duplicate detection (same filename AND same content)
    file_hash = compute_file_hash(file_path)
    existing_records = load_metadata()

    for record in existing_records:
        if record["filename"] == filename and record["hash"] == file_hash:
            print(f"Duplicate submission detected. '{filename}' with identical content was already "
                  f"submitted by {record['student_id']} on {record['timestamp']}.")
            log_submission(f"REJECTED - Student: {student_id} - File: {filename} - Reason: duplicate filename+content")
            return

    # 4. Save the file into the submissions directory
    # If the same filename already exists but with different content, store the new
    # copy with a timestamp suffix so nothing is overwritten
    dest_path = os.path.join(SUBMISSIONS_DIR, filename)
    if os.path.exists(dest_path):
        name_only, ext_only = os.path.splitext(filename)
        timestamp_suffix = datetime.now().strftime("%Y%m%d_%H%M%S")
        stored_filename = f"{name_only}_{timestamp_suffix}{ext_only}"
        dest_path = os.path.join(SUBMISSIONS_DIR, stored_filename)
    else:
        stored_filename = filename

    shutil.copy2(file_path, dest_path)

    # 5. Record metadata under the ORIGINAL filename (so duplicate checks stay accurate)
    append_metadata(student_id, filename, size_bytes, file_hash)

    print(f"File '{filename}' submitted successfully by student {student_id}.")
    log_submission(f"SUCCESS - Student: {student_id} - File: {filename} - Size: {size_bytes} bytes - Stored as: {stored_filename}")


def check_submission():
    print("\n========== Check if File Already Submitted ==========")

    filename = input("Enter filename to check: ").strip()
    if not filename:
        print("Filename cannot be empty.")
        return

    records = load_metadata()
    matches = [r for r in records if r["filename"] == filename]

    if not matches:
        print(f"No submission found for '{filename}'.")
        log_submission(f"CHECK - File: {filename} - Result: not found")
    else:
        print(f"\n'{filename}' has been submitted {len(matches)} time(s):\n")
        print(f"{'Student ID':<12}{'Size (bytes)':<14}{'Submitted At'}")
        for r in matches:
            print(f"{r['student_id']:<12}{r['size_bytes']:<14}{r['timestamp']}")
        log_submission(f"CHECK - File: {filename} - Result: found ({len(matches)} match(es))")


def list_submissions():
    print("\n========== All Submitted Assignments ==========")

    records = load_metadata()
    if not records:
        print("No submissions yet.")
        return

    print(f"{'Student ID':<12}{'Filename':<25}{'Size (bytes)':<14}{'Submitted At'}")
    for r in records:
        print(f"{r['student_id']:<12}{r['filename']:<25}{r['size_bytes']:<14}{r['timestamp']}")


def simulate_login():
    print("\n========== Simulate Login Attempt ==========")

    username = input("Enter username: ").strip()

    if username in locked_accounts:
        print(f"ERROR: Account '{username}' is locked due to too many failed login attempts.")
        log_login(username, "Login blocked - account locked")
        return

    password = input("Enter password: ").strip()

    now = datetime.now()

    if VALID_USERS.get(username) == password:
        print(f"Login successful. Welcome, {username}!")
        log_login(username, "Login successful")
        # Reset failed attempt history on a successful login
        failed_attempts[username] = []
        return

    # --- Failed login ---
    print("Invalid username or password.")

    if username not in failed_attempts:
        failed_attempts[username] = []
    failed_attempts[username].append(now)

    log_login(username, "Login failed")

    # Suspicious activity: repeated failed attempts within the time window
    recent_attempts = [
        t for t in failed_attempts[username]
        if now - t <= timedelta(seconds=SUSPICIOUS_WINDOW_SECONDS)
    ]
    failed_attempts[username] = recent_attempts

    if len(recent_attempts) >= 2:
        print(f"WARNING: Multiple failed login attempts for '{username}' within "
              f"{SUSPICIOUS_WINDOW_SECONDS} seconds - suspicious activity detected.")
        log_login(username, f"Suspicious activity detected - {len(recent_attempts)} failed attempts within {SUSPICIOUS_WINDOW_SECONDS}s")

    # Lock the account after MAX_FAILED_ATTEMPTS consecutive failures
    if len(recent_attempts) >= MAX_FAILED_ATTEMPTS:
        locked_accounts.add(username)
        print(f"ERROR: Account '{username}' has been locked after {MAX_FAILED_ATTEMPTS} failed attempts.")
        log_login(username, f"Account locked after {MAX_FAILED_ATTEMPTS} failed attempts")
    else:
        remaining = MAX_FAILED_ATTEMPTS - len(recent_attempts)
        print(f"{remaining} attempt(s) remaining before the account is locked.")


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
