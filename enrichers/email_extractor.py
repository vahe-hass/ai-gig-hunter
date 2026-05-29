import re
import requests
from bs4 import BeautifulSoup
from config.logger import logger


EMAIL_REGEX = (
    r"[a-zA-Z0-9._%+-]+"
    r"@[a-zA-Z0-9.-]+"
    r"\.[a-zA-Z]+"
)


HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 "
        "(Windows NT 10.0; Win64; x64)"
    )
}


COMMON_PATHS = [
    "",
    "/contact",
    "/about",
    "/contact-us",
    "/about-us"
]


BAD_EMAIL_KEYWORDS = [
    ".png",
    ".jpg",
    ".jpeg",
    ".webp",
    "example.com"
]


def is_valid_email(email):

    email = email.lower()

    return not any(
        bad in email
        for bad in BAD_EMAIL_KEYWORDS
    )


def extract_emails_from_url(url):

    found_emails = set()

    try:

        for path in COMMON_PATHS:

            try:

                full_url = (
                    url.rstrip("/")
                    + path
                )

                logger.info(f"Scanning: {full_url}")

                response = requests.get(
                    full_url,
                    headers=HEADERS,
                    timeout=10
                )

                if response.status_code != 200:
                    continue

                soup = BeautifulSoup(
                    response.text,
                    "html.parser"
                )

                text = soup.get_text()

                emails = re.findall(
                    EMAIL_REGEX,
                    text
                )

                for email in emails:

                    email = email.strip()

                    if is_valid_email(email):

                        found_emails.add(
                            email
                        )

            except Exception as inner_error:

                logger.warning("Path scan failed")
                logger.exception(inner_error)


        return list(found_emails)

    except Exception as e:

        logger.warning("Email extraction failed")
        logger.exception(e)


        return []