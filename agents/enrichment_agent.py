from enrichers.email_extractor import (
    extract_emails_from_url
)

from memory.db import (
    get_leads_missing_email,
    update_lead_email
)

from config.logger import logger


class EnrichmentAgent:

    def run(self):

        leads = get_leads_missing_email()


        logger.info(f"Found {len(leads)} leads missing emails")

        for lead in leads:

            try:

                lead_id = lead["id"]

                website = lead["client_website"]

                if not website:
                    continue

                logger.info(f"Extracting emails from {website}")

                emails = extract_emails_from_url(
                    website
                )

                if not emails:

                    logger.info("No emails found")

                    continue

                primary_email = emails[0]

                update_lead_email(

                    lead_id,

                    primary_email

                )

                logger.info(f"Email saved: {primary_email}")

            except Exception as e:

                logger.warning("EnrichmentAgent failed")
                logger.exception(e)


if __name__ == "__main__":

    EnrichmentAgent().run()