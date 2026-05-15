import requests
from memory.db import get_uncontacted, mark_contacted

N8N_WEBHOOK = "http://localhost:5678/webhook/send-outreach"

class SalesAgent:

    def run(self):
        leads = get_uncontacted()

        for lead in leads:
            message = self.generate_message(lead)

            requests.post(N8N_WEBHOOK, json={
                "lead_id": lead[0],
                "message": message,
                "title": lead[1]
            })

            mark_contacted(lead[0])

    def generate_message(self, lead):
        # Replace later with Claude/OpenAI
        return f"""
Hi,

I saw your job: {lead[1]}

I can build this quickly and professionally.

Let’s discuss.

Best,
Vahe
"""