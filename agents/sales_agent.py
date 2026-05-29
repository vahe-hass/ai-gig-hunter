import time
import random
import requests

from memory.db import (
    get_sales_ready_leads,
    mark_contacted
)

from config.settings import (
    N8N_WEBHOOK
)


class SalesAgent:

    def run(self):

        leads = get_sales_ready_leads()

        if not leads:

            print(
                "No sales-ready leads found."
            )

            return

        print(
            f"Found {len(leads)} "
            f"sales-ready leads."
        )

        for lead in leads:

            try:

                lead_id = lead["id"]

                print(
                    f"\nProcessing lead "
                    f"#{lead_id}"
                )

                message = self.generate_message(
                    lead
                )

                payload = {

                    "lead_id":
                        lead["id"],

                    "client_name":
                        lead["client_name"],

                    "client_email":
                        lead["client_email"],

                    "title":
                        lead["title"],

                    "message":
                        message,

                    "website":
                        lead.get(
                            "client_website"
                        ),

                    "audit_score":
                        lead.get(
                            "audit_score"
                        ),

                    "audit_notes":
                        lead.get(
                            "audit_notes"
                        )
                }

                response = requests.post(

                    N8N_WEBHOOK,

                    json=payload,

                    timeout=15
                )

                if response.status_code == 200:

                    print(
                        f"Successfully sent "
                        f"lead #{lead_id}"
                    )

                    mark_contacted(
                        lead_id
                    )

                else:

                    print(
                        f"Failed sending "
                        f"lead #{lead_id}"
                    )

                    print(
                        response.text
                    )

                # anti-spam delay
                sleep_time = random.uniform(
                    3,
                    8
                )

                print(
                    f"Sleeping "
                    f"{sleep_time:.2f}s"
                )

                time.sleep(
                    sleep_time
                )

            except Exception as e:

                print(
                    f"SalesAgent failed "
                    f"for lead #{lead_id}"
                )

                print(str(e))

    def generate_message(

        self,

        lead

    ):

        client_name = (
            lead.get(
                "client_name"
            )
            or "there"
        )

        title = (
            lead.get(
                "title"
            )
            or ""
        )

        audit_notes = (
            lead.get(
                "audit_notes"
            )
            or ""
        )

        website = (
            lead.get(
                "client_website"
            )
            or ""
        )

        # ========================
        # WEBSITE AUDIT OUTREACH
        # ========================

        if audit_notes:

            return f"""
Hi {client_name},

I was checking your website:

{website}

and noticed a few areas that could be improved:

{audit_notes}

I specialize in modern web development and website optimization, and I believe I could help improve the user experience and overall performance of the site.

Would you be open to a quick conversation this week?

Best regards,
Vahe
"""

        # ========================
        # PROJECT OUTREACH
        # ========================

        return f"""
Hi {client_name},

I came across your project:

{title}

and it looks like something I can help with.

I specialize in fast, modern, responsive web development and have experience building professional websites and web applications.

I'd be happy to discuss the project further if you're interested.

Best regards,
Vahe
"""