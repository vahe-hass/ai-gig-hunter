import requests
from bs4 import BeautifulSoup


KEYWORDS = [
    "web",
    "wordpress",
    "react",
    "frontend",
    "backend",
    "developer",
    "shopify",
    "javascript",
    "php",
]


def is_relevant_job(text):

    text = text.lower()

    return any(
        keyword in text
        for keyword in KEYWORDS
    )


def clean_html(html):

    if not html:
        return ""

    soup = BeautifulSoup(
        html,
        "html.parser"
    )

    return soup.get_text(
        separator=" ",
        strip=True
    )


def fetch_remoteok_jobs():

    url = "https://remoteok.com/api"

    headers = {
        "User-Agent": (
            "Mozilla/5.0 "
            "(Windows NT 10.0; Win64; x64)"
        )
    }

    jobs = []

    try:

        response = requests.get(
            url,
            headers=headers,
            timeout=10
        )

        if response.status_code != 200:

            print(
                f"RemoteOK bad status: "
                f"{response.status_code}"
            )

            return []

        data = response.json()

        print(
            f"Found {len(data)} "
            f"potential job links"
        )

        # first item is metadata
        for item in data[1:]:

            try:

                title = item.get("position")

                description = clean_html(
                    item.get("description")
                )

                company = item.get("company")

                job_url = item.get("url")

                if not title:
                    continue

                searchable_text = (
                    f"{title} {description}"
                )

                # filter irrelevant jobs
                if not is_relevant_job(
                    searchable_text
                ):
                    continue

                # trim massive descriptions
                if len(description) > 3000:
                    description = (
                        description[:3000]
                    )

                job = {
                    "title": title,
                    "description": description,
                    "client_name": company,
                    "client_email": None,
                    "client_website": None,
                    "url": job_url
                }

                jobs.append(job)

            except Exception as inner_error:

                print(
                    "Failed parsing one "
                    "RemoteOK job"
                )

                print(str(inner_error))

        print(
            f"RemoteOK: fetched "
            f"{len(jobs)} relevant jobs"
        )

        return jobs

    except Exception as e:

        print("RemoteOK scraper failed")

        print(str(e))

        return []