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
        jobs = data.get("jobs", [])

        return jobs

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
        title = str(job.get("title", "")).lower()
        company = str(job.get("companyName", "")).lower()
        description = str(job.get("description", "")).lower()

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
        job_location = str(
            job.get("location", "")
        ).lower()

        if location in job_location:
            filtered_jobs.append(job)

    return filtered_jobs


def display_jobs(jobs):
    if not jobs:
        print("\nNo matching jobs found.")
        return

    print("\n" + "=" * 70)
    print("                    JOB RESULTS")
    print("=" * 70)

    print(f"\nJobs found: {len(jobs)}")

    for number, job in enumerate(jobs, start=1):

        title = job.get("title", "Unknown")
        company = job.get("companyName", "Unknown")
        location = job.get("location", "Unknown")

        application_link = job.get(
            "applicationLink",
            "Not available"
        )

        print("\n" + "-" * 70)

        print(f"Job #{number}")
        print("Role:     ", title)
        print("Company:  ", company)
        print("Location: ", location)
        print("Apply:    ", application_link)

    print("-" * 70)


def load_saved_jobs():
    if not os.path.exists(SAVED_FILE):
        return []

    try:
        with open(
            SAVED_FILE,
            "r",
            encoding="utf-8"
        ) as file:
            data = json.load(file)

        if isinstance(data, list):
            return data

        return []

    except (json.JSONDecodeError, OSError):
        return []


def save_jobs(saved_jobs):
    try:
        with open(
            SAVED_FILE,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                saved_jobs,
                file,
                indent=4
            )

    except OSError as error:
        print("\nCould not save jobs.")
        print("Error:", error)


def bookmark_job(job):
    saved_jobs = load_saved_jobs()

    title = job.get(
        "title",
        "Unknown"
    )

    company = job.get(
        "companyName",
        "Unknown"
    )

    for saved_job in saved_jobs:

        if (
            saved_job.get("title") == title
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

    print("\n" + "=" * 70)
    print("                    SAVED JOBS")
    print("=" * 70)

    print(
        f"\nSaved jobs: {len(saved_jobs)}"
    )

    for number, job in enumerate(
        saved_jobs,
        start=1
    ):

        print("\n" + "-" * 70)

        print(
            f"Saved Job #{number}"
        )

        print(
            "Role:     ",
            job.get(
                "title",
                "Unknown"
            )
        )

        print(
            "Company:  ",
            job.get(
                "companyName",
                "Unknown"
            )
        )

        print(
            "Location: ",
            job.get(
                "location",
                "Unknown"
            )
        )

        print(
            "Apply:    ",
            job.get(
                "applicationLink",
                "Not available"
            )
        )

    print("-" * 70)


def search_and_filter(jobs):

    keyword = input(
        "\nEnter job keyword "
        "(press Enter for all): "
    )

    filtered_jobs = search_jobs(
        jobs,
        keyword
    )

    location = input(
        "Enter location "
        "(press Enter for all): "
    )

    filtered_jobs = filter_by_location(
        filtered_jobs,
        location
    )

    return filtered_jobs


def search_and_save(jobs):

    filtered_jobs = search_and_filter(
        jobs
    )

    display_jobs(
        filtered_jobs
    )

    if not filtered_jobs:
        return

    choice = input(
        "\nEnter job number to save "
        "(press Enter to skip): "
    )

    if not choice.strip():
        return

    try:

        job_number = int(choice)

        if (
            1 <= job_number
            <= len(filtered_jobs)
        ):

            selected_job = filtered_jobs[
                job_number - 1
            ]

            bookmark_job(
                selected_job
            )

        else:

            print(
                "\nInvalid job number."
            )

    except ValueError:

        print(
            "\nPlease enter a valid number."
        )


def show_menu():

    print("\n" + "=" * 70)
    print(
        "              JOB / INTERNSHIP API TRACKER"
    )
    print("=" * 70)

    print("\n1. Search and filter jobs")
    print("2. View all fetched jobs")
    print("3. View saved jobs")
    print("4. Exit")


def main():

    jobs = get_jobs()

    if not jobs:

        print(
            "\nNo jobs available."
        )

        return

    print(
        f"\nSuccessfully fetched {len(jobs)} jobs."
    )

    while True:

        show_menu()

        choice = input(
            "\nChoose an option: "
        ).strip()

        if choice == "1":

            search_and_save(
                jobs
            )

        elif choice == "2":

            display_jobs(
                jobs
            )

        elif choice == "3":

            display_saved_jobs()

        elif choice == "4":

            print(
                "\nThanks for using "
                "Job Internship API Tracker!"
            )

            break

        else:

            print(
                "\nInvalid option."
            )

            print(
                "Please choose 1, 2, 3, or 4."
            )


if __name__ == "__main__":
    main()