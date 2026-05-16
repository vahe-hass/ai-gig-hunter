import requests

from memory.db import get_uncontacted, mark_contacted
from config.settings import N8N_WEBHOOK


class SalesAgent:

    def run(self):
        leads = get_uncontacted()

        if not leads:
            print("No uncontacted leads found.")
            return

        print(f"Found {len(leads)} leads.")
        print(leads)

        for lead in leads:
            lead_id = lead[0]
            title = lead[1]
            description = lead[2]

            message = self.generate_message(title, description)

            payload = {
                "lead_id": lead_id,
                "title": title,
                "description": description,
                "message": message
            }

            try:
                response = requests.post(
                    N8N_WEBHOOK,
                    json=payload,
                    timeout=10
                )

                if response.status_code == 200:
                    print(f"Successfully sent lead #{lead_id} to n8n.")

                    mark_contacted(lead_id)

                else:
                    print(
                        f"Failed to send lead #{lead_id}. "
                        f"Status code: {response.status_code}"
                    )

                    print("Response:")
                    print(response.text)

            except requests.exceptions.ConnectionError:
                print(
                    "Connection error: Could not connect to n8n.\n"
                    "Make sure n8n is running and workflow is active."
                )

            except requests.exceptions.Timeout:
                print(
                    f"Timeout error while sending lead #{lead_id}."
                )

            except Exception as e:
                print(
                    f"Unexpected error while sending lead #{lead_id}:"
                )

                print(str(e))

    def generate_message(self, title, description):

        return f"""
Hi,

I saw your project:

{title}

It looks like something I can help with.

I specialize in modern web development and can build
clean, responsive, and fast websites professionally.

Let me know if you'd like to discuss the project further.

Best regards,
Vahe
"""