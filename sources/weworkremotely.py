import requests
from bs4 import BeautifulSoup
from config.logger import logger



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


def fetch_weworkremotely_jobs():

    url = (
        "https://weworkremotely.com/"
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

        if response.status_code != 200:
            return []

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        # all job links
        links = soup.select('a[href*="/remote-jobs/"]')


        logger.info(f"Found {len(links)} potential job links")

        seen_urls = set()

        for link in links[3:]:

            try:

                href = link.get("href")

                if not href:
                    continue

                if href in seen_urls:
                    continue

                seen_urls.add(href)

                # title
                title_tag = (
                    link.select_one("div.new-listing__header__title__text")
                )

                # company
                company_tag = (
                    link.select_one("p.new-listing__company-name")
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

                searchable_text = (
                    f"{title}"
                )

                # filter irrelevant jobs
                if not is_relevant_job(
                    searchable_text
                ):
                    continue

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
                    "client_website": None,
                    "url": job_url
                }

                jobs.append(job)

            except Exception as inner_error:

                logger.warning("Failed parsing one WeWorkRemotely job")
                logger.exception(inner_error)


        logger.info(f"WeWorkRemotely: fetched {len(jobs)} relevant jobs")

        return jobs

    except Exception as e:

        logger.warning("WeWorkRemotely scraper failed")
        logger.exception(e)

        return []