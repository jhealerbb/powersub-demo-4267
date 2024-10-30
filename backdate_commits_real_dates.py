import os
import subprocess
import random
from datetime import datetime, timedelta

# === CONFIGURATION ===
REPO_DIR = "."  # Use current directory
COMMIT_FILE = "commit_messages.txt"
NUM_COMMITS = 100

# 🗓️ SET YOUR DATE RANGE HERE
# Example: from October 21, 2024 to October 21, 2025
START_DATE = datetime(2024, 10, 25)
END_DATE = datetime(2025, 10, 25)

def load_commit_messages(path):
    with open(path, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]
    if len(lines) < NUM_COMMITS:
        raise ValueError(f"Expected at least {NUM_COMMITS} unique commit messages.")
    random.shuffle(lines)
    return lines[:NUM_COMMITS]

def generate_random_dates(n, start_date, end_date):
    delta = (end_date - start_date).days
    dates = set()
    while len(dates) < n:
        rand_day = start_date + timedelta(days=random.randint(0, delta))
        rand_time = timedelta(hours=random.randint(0, 23), minutes=random.randint(0, 59))
        full_datetime = rand_day + rand_time
        dates.add(full_datetime.strftime("%Y-%m-%dT%H:%M:%S"))
    return sorted(dates)

def setup_repo(path):
    if not os.path.exists(os.path.join(path, ".git")):
        subprocess.run(["git", "init"], cwd=path)

def make_commit(repo_path, message, date_iso):
    dummy_file = os.path.join(repo_path, "log.txt")
    with open(dummy_file, "a", encoding="utf-8") as f:
        f.write(f"{message}\n")

    env = os.environ.copy()
    env["GIT_AUTHOR_DATE"] = date_iso
    env["GIT_COMMITTER_DATE"] = date_iso

    subprocess.run(["git", "add", "."], cwd=repo_path, env=env)
    subprocess.run(["git", "commit", "-m", message], cwd=repo_path, env=env)

def main():
    print("📄 Loading commit messages...")
    messages = load_commit_messages(COMMIT_FILE)

    print(f"📅 Generating random commit dates between {START_DATE.date()} and {END_DATE.date()}...")
    dates = generate_random_dates(NUM_COMMITS, START_DATE, END_DATE)

    print(f"📁 Setting up Git repo at: {REPO_DIR}")
    setup_repo(REPO_DIR)

    print("⏳ Creating commits...")
    for i in range(NUM_COMMITS):
        print(f"📦 Commit {i+1}/{NUM_COMMITS} → {dates[i]} | {messages[i]}")
        make_commit(REPO_DIR, messages[i], dates[i])

    print(f"\n✅ Done! All commits backdated randomly between {START_DATE.date()} and {END_DATE.date()}.")

if __name__ == "__main__":
    main()
