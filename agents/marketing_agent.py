from tools.scraper_manager import get_jobs
from memory.db import save_lead


class MarketingAgent:

    MINIMUM_SCORE = 35

    def run(self):

        jobs = get_jobs()
        print(f"Found {len(jobs)} job(s)")

        for job in jobs:
            score = self.score_lead(job)
            job["score"] = score
            if score >= self.MINIMUM_SCORE:
                save_lead(job)
                print(
                    f"Saved lead: {job.get('title')} "
                    f"(score: {score})"
                )

            else:

                print(
                    f"Skipped low-score lead: "
                    f"{job.get('title')} "
                    f"(score: {score})"
                )

    def score_lead(self, job):
        score = 0
        title = job.get("title", "").lower()
        description = (job.get("description") or "").lower()
        text = f"{title} {description}"

        # keyword scoring
        if "wordpress" in text:
            score += 35

        if "website" in text:
            score += 20

        if "landing page" in text:
            score += 20

        if "web developer" in text:
            score += 20

        if "developer" in text:
            score += 20

        if "shopify" in text:
            score += 15

        if "react" in text:
            score += 15

        if "urgent" in text:
            score += 10

        if "$" in text:
            score += 10

        # bonus for client email
        if job.get("client_email"):
            score += 10

        # keep score between 0 and 100
        score = max(0, min(score, 100))

        return score