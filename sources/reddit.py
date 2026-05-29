import requests
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
    "[hiring]",
    "[hire me]"
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
    "my rates",
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

    headers = {
        "User-Agent": (
            "Mozilla/5.0 "
            "AILeadBot/1.0"
        )
    }

    jobs = []

    try:

        for subreddit in SUBREDDITS:

            url = (
                f"https://www.reddit.com/"
                f"r/{subreddit}/new.json?limit=25"
            )

            response = requests.get(
                url,
                headers=headers,
                timeout=10
            )

            if response.status_code != 200:


                logger.info(f"Reddit bad status for r/{subreddit}: {response.status_code}")


                continue

            data = response.json()

            posts = (
                data.get("data", {})
                .get("children", [])
            )

            logger.info(f"r/{subreddit}: {len(posts)} posts fetched")

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
                        f"{title} {description}"
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
                        "permalink"
                    )

                    job_url = (
                        "https://reddit.com"
                        + permalink
                    )

                    job = {
                        "title": title,
                        "description": description,
                        "client_name": author,
                        "client_email": None,
                        "client_website": None,
                        "url": job_url
                    }

                    jobs.append(job)

                except Exception as inner_error:


                    logger.warning("Failed parsing Reddit post")
                    logger.exception(inner_error)


        logger.info(f"Reddit: fetched {len(jobs)} relevant posts"
)

        return jobs

    except Exception as e:

        logger.warning("Reddit scraper failed")
        logger.exception(e)

        return []