import requests
from bs4 import BeautifulSoup
from memory.db import get_unaudited_websites, update_website_audit


HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 "
        "(Windows NT 10.0; Win64; x64)"
    )
}


def analyze_website(url):

    audit_notes = []

    score = 100

    try:

        response = requests.get(
            url,
            headers=HEADERS,
            timeout=10
        )

        if response.status_code != 200:

            return {
                "score": 10,
                "notes": (
                    f"Website returned status "
                    f"{response.status_code}"
                )
            }

        html = response.text

        soup = BeautifulSoup(
            html,
            "html.parser"
        )

        # ========================
        # TITLE CHECK
        # ========================

        title = soup.title

        if not title or not title.text.strip():

            audit_notes.append(
                "Missing page title"
            )

            score -= 15

        # ========================
        # MOBILE CHECK
        # ========================

        viewport = soup.find(
            "meta",
            attrs={"name": "viewport"}
        )

        if not viewport:

            audit_notes.append(
                "Website may not be mobile optimized"
            )

            score -= 20

        # ========================
        # HTTPS CHECK
        # ========================

        if not url.startswith("https"):

            audit_notes.append(
                "Website is not using HTTPS"
            )

            score -= 20

        # ========================
        # CONTACT CHECK
        # ========================

        page_text = soup.get_text().lower()

        if (
            "contact" not in page_text
            and "email" not in page_text
            and "phone" not in page_text
        ):

            audit_notes.append(
                "No visible contact information"
            )

            score -= 15

        # ========================
        # IMAGE ALT CHECK
        # ========================

        images = soup.find_all("img")

        missing_alt = 0

        for image in images:

            if not image.get("alt"):

                missing_alt += 1

        if missing_alt >= 5:

            audit_notes.append(
                "Many images missing alt tags"
            )

            score -= 10

        # ========================
        # WORDPRESS DETECTION
        # ========================

        if "wp-content" in html:

            audit_notes.append(
                "WordPress website detected"
            )

        # ========================
        # SLOW PAGE HEURISTIC
        # ========================

        html_size = len(html)

        if html_size > 2_000_000:

            audit_notes.append(
                "Very large page size"
            )

            score -= 10

        # ========================
        # FINAL SCORE FLOOR
        # ========================

        if score < 0:

            score = 0

        # ========================
        # DEFAULT NOTE
        # ========================

        if not audit_notes:

            audit_notes.append(
                "Website looks technically healthy"
            )

        return {
            "score": score,
            "notes": "\n".join(audit_notes)
        }

    except Exception as e:

        return {
            "score": 5,
            "notes": (
                f"Audit failed: {str(e)}"
            )
        }


class AuditAgent:

    def run(self):

        leads = get_unaudited_websites()

        print(
            f"Found {len(leads)} "
            f"websites to audit"
        )

        for lead in leads:

            try:

                lead_id = lead["id"]

                website = lead["client_website"]

                if not website:

                    continue

                print(
                    f"Auditing: {website}"
                )

                audit = analyze_website(
                    website
                )

                update_website_audit(

                    lead_id=lead_id,

                    audit_score=audit["score"],

                    audit_notes=audit["notes"]

                )

                print(
                    f"Audit complete: "
                    f"{audit['score']}"
                )

            except Exception as e:

                print(
                    "AuditAgent failed"
                )

                print(str(e))


if __name__ == "__main__":

    AuditAgent().run()