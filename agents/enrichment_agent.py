from enrichers.email_extractor import (
    extract_emails_from_url
)

from memory.db import (
    get_leads_missing_email,
    update_lead_email
)


class EnrichmentAgent:

    def run(self):

        leads = get_leads_missing_email()

        print(
            f"Found {len(leads)} "
            f"leads missing emails"
        )

        for lead in leads:

            try:

                lead_id = lead["id"]

                website = lead["client_website"]

                if not website:
                    continue

                print(
                    f"Extracting emails from "
                    f"{website}"
                )

                emails = extract_emails_from_url(
                    website
                )

                if not emails:

                    print(
                        "No emails found"
                    )

                    continue

                primary_email = emails[0]

                update_lead_email(

                    lead_id,

                    primary_email

                )

                print(
                    f"Email saved: "
                    f"{primary_email}"
                )

            except Exception as e:

                print(
                    "EnrichmentAgent failed"
                )

                print(str(e))


if __name__ == "__main__":

    EnrichmentAgent().run()