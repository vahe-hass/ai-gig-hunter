from tools.scraper import get_jobs
from tools.lead_filter import is_good_lead
from memory.db import save_lead

class MarketingAgent:

    def run(self):
        jobs = get_jobs()

        for job in jobs:
            if is_good_lead(job):
                save_lead(job)