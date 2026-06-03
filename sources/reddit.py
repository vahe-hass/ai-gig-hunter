import requests
import random
import time

from config.logger import logger

SUBREDDITS = [
"forhire",
"freelance_forhire",
"webdevjobs",
"smallbusiness",
"startups"
]

KEYWORDS = [
"web developer",
"wordpress",
"website",
"landing page",
"shopify",
"frontend",
"backend",
"react",
"developer needed",
"looking for developer"
]

BUYER_KEYWORDS = [
"looking for",
"hiring",
"need a",
"need help",
"seeking",
"developer needed",
"who can build",
"need website",
"budget",
"paid",
"[hiring]"
]

SELLER_KEYWORDS = [
"for hire",
"hire me",
"my portfolio",
"[portfolio]",
"i am a developer",
"freelancer here",
"offering services",
"web developer available",
"my rates"
]

def is_relevant(text):


    text = text.lower()

    return any(
        keyword in text
        for keyword in KEYWORDS
    )


def is_buyer_post(text):


    text = text.lower()

    buyer_match = any(
        keyword in text
        for keyword in BUYER_KEYWORDS
    )

    seller_match = any(
        keyword in text
        for keyword in SELLER_KEYWORDS
    )

    return buyer_match and not seller_match


def fetch_reddit_jobs():


    session = requests.Session()

    session.headers.update({

        "User-Agent": (
            "Mozilla/5.0 "
            "(Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 "
            "(KHTML, like Gecko) "
            "Chrome/137.0.0.0 "
            "Safari/537.36"
        ),

        "Accept": "application/json",

        "Accept-Language":
            "en-US,en;q=0.9",

        "Referer":
            "https://old.reddit.com/"
    })

    jobs = []

    try:

        for subreddit in SUBREDDITS:

            time.sleep(
                random.uniform(2, 5)
            )

            url = (
                f"https://old.reddit.com/"
                f"r/{subreddit}/new.json"
                f"?limit=50"
            )

            response = None

            for attempt in range(3):

                try:

                    response = session.get(
                        url,
                        timeout=15
                    )

                    if response.status_code == 200:

                        break

                    logger.warning(
                        f"Reddit status "
                        f"{response.status_code} "
                        f"for r/{subreddit} "
                        f"(attempt {attempt+1}/3)"
                    )

                    time.sleep(
                        random.uniform(5, 10)
                    )

                except Exception as retry_error:

                    logger.warning(
                        f"Retry failed for "
                        f"r/{subreddit}"
                    )

                    logger.exception(
                        retry_error
                    )

            if not response:

                continue

            if response.status_code != 200:

                logger.warning(
                    f"Skipping r/{subreddit} "
                    f"after retries. "
                    f"Status: "
                    f"{response.status_code}"
                )

                continue

            data = response.json()

            posts = (
                data.get("data", {})
                .get("children", [])
            )

            logger.info(
                f"r/{subreddit}: "
                f"{len(posts)} posts fetched"
            )

            for post in posts:

                try:

                    post_data = post.get(
                        "data",
                        {}
                    )

                    title = post_data.get(
                        "title",
                        ""
                    )

                    description = post_data.get(
                        "selftext",
                        ""
                    )

                    searchable_text = (
                        f"{title} "
                        f"{description}"
                    )

                    if not is_relevant(
                        searchable_text
                    ):
                        continue

                    if not is_buyer_post(
                        searchable_text
                    ):
                        continue

                    author = post_data.get(
                        "author"
                    )

                    permalink = post_data.get(
                        "permalink",
                        ""
                    )

                    job_url = (
                        "https://reddit.com"
                        + permalink
                    )

                    job = {

                        "title":
                            title,

                        "description":
                            description,

                        "client_name":
                            author,

                        "client_email":
                            None,

                        "client_website":
                            None,

                        "url":
                            job_url
                    }

                    jobs.append(job)

                except Exception as inner_error:

                    logger.warning(
                        "Failed parsing "
                        "Reddit post"
                    )

                    logger.exception(
                        inner_error
                    )

        logger.info(
            f"Reddit: fetched "
            f"{len(jobs)} "
            f"relevant posts"
        )

        return jobs

    except Exception as e:

        logger.warning(
            "Reddit scraper failed"
        )

        logger.exception(e)

        return []