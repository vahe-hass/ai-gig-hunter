import requests
import time
import random
from bs4 import BeautifulSoup
from config.logger import logger


KEYWORDS = [
    "web",
    "developer",
    "frontend",
    "backend",
    "full stack",
    "wordpress",
    "react",
    "shopify",
    "javascript",
    "php",
    "laravel"
]


MAX_PAGES = 4


def is_relevant(text):

    text = text.lower()

    return any(
        keyword in text
        for keyword in KEYWORDS
    )


def fetch_hackernews_jobs():

    base_url = (
        "https://news.ycombinator.com"
    )

    current_url = (
        f"{base_url}/jobs"
    )

    session = requests.Session()

    session.headers.update({
        "User-Agent": (
            "Mozilla/5.0 "
            "(Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 "
            "(KHTML, like Gecko) "
            "Chrome/124.0.0.0 "
            "Safari/537.36"
        )
    })

    jobs = []

    seen_urls = set()

    try:

        for page in range(MAX_PAGES):

            sleep_time = random.uniform(5, 6)

            time.sleep(sleep_time)


            logger.info(f"Scraping HackerNews: {current_url}")

            response = session.get(
                current_url,
                timeout=10
            )

            if response.status_code == 429:


                logger.warning("HackerNews rate limited (429) Stopping scraper.")

                break

            if response.status_code != 200:

                logger.warning(f"HackerNews bad status: {response.status_code}")

                break

            soup = BeautifulSoup(
                response.text,
                "html.parser"
            )

            rows = soup.select("tr.athing")


            logger.info(f"Found {len(rows)} posts")

            for row in rows:

                try:

                    title_tag = row.select_one(
                        "span.titleline a"
                    )

                    if not title_tag:
                        continue

                    title = title_tag.get_text(
                        strip=True
                    )

                    if not is_relevant(title):
                        continue

                    job_url = title_tag.get("href")

                    if not job_url:
                        continue

                    # convert relative links
                    if job_url.startswith("item?"):

                        job_url = (
                            base_url + "/"
                            + job_url
                        )

                    # prevent duplicates
                    if job_url in seen_urls:
                        continue

                    seen_urls.add(job_url)

                    job = {
                        "title": title,
                        "description": None,
                        "client_name": "Hacker News",
                        "client_email": None,
                        "client_website": None,
                        "url": job_url
                    }

                    jobs.append(job)

                except Exception as inner_error:


                    logger.warning("Failed parsing HackerNews post")
                    logger.exception(inner_error)


            # find next page link
            more_link = soup.select_one(
                "a.morelink"
            )

            if not more_link:

                logger.info("No more pages found")

                break

            next_href = more_link.get("href")

            if not next_href:

                break

            current_url = (
                base_url + "/"
                + next_href
            )

        logger.info(f"HackerNews: fetched {len(jobs)} relevant jobs")

        return jobs

    except Exception as e:


        logger.warning("HackerNews scraper failed")
        logger.exception(e)


        return []