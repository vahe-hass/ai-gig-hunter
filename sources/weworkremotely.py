import requests

from bs4 import BeautifulSoup


def fetch_weworkremotely_jobs():

    url = (
        "https://weworkremotely.com/"
        "remote-jobs/search?term=developer"
    )

    headers = {
        "User-Agent": (
            "Mozilla/5.0 "
            "(Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 "
            "(KHTML, like Gecko) "
            "Chrome/124.0.0.0 "
            "Safari/537.36"
        )
    }

    jobs = []

    try:

        response = requests.get(
            url,
            headers=headers,
            timeout=10
        )

        print(
            f"WeWorkRemotely status: "
            f"{response.status_code}"
        )

        if response.status_code != 200:
            return []

        print(
            f"Response length: "
            f"{len(response.text)}"
        )

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        # all job links
        links = soup.select('a[href*="/remote-jobs/"]')

        print(
            f"Found {len(links)} "
            f"potential job links"
        )

        seen_urls = set()

        for link in links:

            try:

                href = link.get("href")

                if not href:
                    continue

                if href in seen_urls:
                    continue

                seen_urls.add(href)

                # title
                title_tag = (
                    link.select_one("span.title")
                )

                # company
                company_tag = (
                    link.select_one("span.company")
                )

                title = None

                if title_tag:
                    title = title_tag.get_text(
                        strip=True
                    )

                # fallback title
                if not title:
                    title = link.get_text(
                        strip=True
                    )

                if not title:
                    continue

                company = (
                    company_tag.get_text(strip=True)
                    if company_tag else None
                )

                job_url = (
                    "https://weworkremotely.com"
                    + href
                )

                job = {
                    "title": title,
                    "description": None,
                    "client_name": company,
                    "client_email": None,
                    "budget": None,
                    "url": job_url
                }

                jobs.append(job)

            except Exception as inner_error:

                print(
                    "Failed parsing one "
                    "WeWorkRemotely job"
                )

                print(str(inner_error))

        print(
            f"WeWorkRemotely: fetched "
            f"{len(jobs)} jobs"
        )

        return jobs

    except Exception as e:

        print(
            "WeWorkRemotely scraper failed"
        )

        print(str(e))

        return []