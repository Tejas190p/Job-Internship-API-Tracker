import requests


API_URL = "https://himalayas.app/jobs/api"


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


def main():
    print("=" * 65)
    print("              JOB / INTERNSHIP API TRACKER")
    print("=" * 65)

    print("\nFetching latest job opportunities...")

    jobs = get_jobs()

    if not jobs:
        print("\nNo jobs available.")
        return

    print("\nTotal jobs fetched:", len(jobs))

    # Search by keyword
    keyword = input(
        "\nEnter job keyword (press Enter for all): "
    )

    jobs = search_jobs(jobs, keyword)

    # Filter by location
    location = input(
        "Enter location (press Enter for all): "
    )

    jobs = filter_by_location(jobs, location)

    # Display final results
    display_jobs(jobs)


if __name__ == "__main__":
    main()