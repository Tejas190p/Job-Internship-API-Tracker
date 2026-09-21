

import requests

API_URL = "https://himalayas.app/jobs/api"


def get_jobs():
    print("\nConnecting to Jobs API...")

    try:
        response = requests.get(
            API_URL,
            params={"limit": 20},
            timeout=15
        )

        response.raise_for_status()

        data = response.json()

        return data.get("jobs", [])

    except requests.exceptions.RequestException as error:
        print("\nCould not connect to the API.")
        print("Error:", error)

        return []


def display_jobs(jobs):
    if not jobs:
        print("\nNo jobs found.")
        return

    print("\n" + "=" * 60)
    print("           JOB / INTERNSHIP API TRACKER")
    print("=" * 60)

    print("\nJobs found:", len(jobs))

    for number, job in enumerate(jobs, start=1):

        title = job.get("title", "Unknown")
        company = job.get("companyName", "Unknown")
        location = job.get("location", "Remote")
        application_link = job.get(
            "applicationLink",
            "Not available"
        )

        print("\n" + "-" * 60)
        print("Job #", number)
        print("Role:     ", title)
        print("Company:  ", company)
        print("Location: ", location)
        print("Apply:    ", application_link)

    print("-" * 60)


def main():
    print("=" * 60)
    print("           JOB / INTERNSHIP API TRACKER")
    print("=" * 60)

    print("\nFetching latest job opportunities...")

    jobs = get_jobs()

    display_jobs(jobs)



if __name__ == "__main__":
    main()