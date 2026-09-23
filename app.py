import json
import os

import requests


API_URL = "https://himalayas.app/jobs/api"
SAVED_FILE = "saved_jobs.json"


def get_jobs():
    print("\nConnecting to Jobs API...")

    try:
        response = requests.get(
            API_URL,
            params={"limit": 50},
            timeout=15
        )

        response.raise_for_status()

        data = response.json()

        return data.get("jobs", [])

    except requests.exceptions.RequestException as error:
        print("\nCould not connect to the API.")
        print("Error:", error)

        return []


def search_jobs(jobs, keyword):
    keyword = keyword.lower().strip()

    if not keyword:
        return jobs

    filtered_jobs = []

    for job in jobs:
        title = job.get("title", "").lower()
        company = job.get("companyName", "").lower()
        description = job.get("description", "").lower()

        if (
            keyword in title
            or keyword in company
            or keyword in description
        ):
            filtered_jobs.append(job)

    return filtered_jobs


def filter_by_location(jobs, location):
    location = location.lower().strip()

    if not location:
        return jobs

    filtered_jobs = []

    for job in jobs:
        job_location = job.get("location", "").lower()

        if location in job_location:
            filtered_jobs.append(job)

    return filtered_jobs


def display_jobs(jobs):
    if not jobs:
        print("\nNo matching jobs found.")
        return

    print("\n" + "=" * 65)
    print("              JOB / INTERNSHIP API TRACKER")
    print("=" * 65)

    print("\nMatching jobs:", len(jobs))

    for number, job in enumerate(jobs, start=1):
        title = job.get("title", "Unknown")
        company = job.get("companyName", "Unknown")
        location = job.get("location", "Remote")
        application_link = job.get(
            "applicationLink",
            "Not available"
        )

        print("\n" + "-" * 65)
        print("Job #", number)
        print("Role:     ", title)
        print("Company:  ", company)
        print("Location: ", location)
        print("Apply:    ", application_link)

    print("-" * 65)


def load_saved_jobs():
    if not os.path.exists(SAVED_FILE):
        return []

    try:
        with open(SAVED_FILE, "r", encoding="utf-8") as file:
            return json.load(file)

    except (json.JSONDecodeError, OSError):
        return []


def save_jobs(saved_jobs):
    with open(SAVED_FILE, "w", encoding="utf-8") as file:
        json.dump(saved_jobs, file, indent=4)


def bookmark_job(job):
    saved_jobs = load_saved_jobs()

    job_title = job.get("title", "Unknown")
    company = job.get("companyName", "Unknown")

    for saved_job in saved_jobs:
        if (
            saved_job.get("title") == job_title
            and saved_job.get("companyName") == company
        ):
            print("\nThis job is already saved.")
            return

    saved_jobs.append(job)
    save_jobs(saved_jobs)

    print("\n🔖 Job saved successfully!")


def display_saved_jobs():
    saved_jobs = load_saved_jobs()

    if not saved_jobs:
        print("\nNo saved jobs yet.")
        return

    print("\n" + "=" * 65)
    print("                    SAVED JOBS")
    print("=" * 65)

    print("\nSaved jobs:", len(saved_jobs))

    for number, job in enumerate(saved_jobs, start=1):
        print("\n" + "-" * 65)
        print("Saved Job #", number)
        print("Role:     ", job.get("title", "Unknown"))
        print("Company:  ", job.get("companyName", "Unknown"))
        print("Location: ", job.get("location", "Remote"))
        print(
            "Apply:    ",
            job.get("applicationLink", "Not available")
        )

    print("-" * 65)


def main():
    print("=" * 65)
    print("              JOB / INTERNSHIP API TRACKER")
    print("=" * 65)

    jobs = get_jobs()

    if not jobs:
        print("\nNo jobs available.")
        return

    print("\nTotal jobs fetched:", len(jobs))

    keyword = input(
        "\nEnter job keyword (press Enter for all): "
    )

    jobs = search_jobs(jobs, keyword)

    location = input(
        "Enter location (press Enter for all): "
    )

    jobs = filter_by_location(jobs, location)

    display_jobs(jobs)

    if jobs:
        choice = input(
            "\nEnter job number to save "
            "(press Enter to skip): "
        )

        if choice.strip():
            try:
                job_number = int(choice)

                if 1 <= job_number <= len(jobs):
                    bookmark_job(jobs[job_number - 1])
                else:
                    print("\nInvalid job number.")

            except ValueError:
                print("\nPlease enter a valid number.")

    view_saved = input(
        "\nView saved jobs? (y/n): "
    ).lower().strip()

    if view_saved == "y":
        display_saved_jobs()


if __name__ == "__main__":
    main()