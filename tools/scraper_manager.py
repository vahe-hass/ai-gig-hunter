from sources.remoteok import fetch_remoteok_jobs
from sources.weworkremotely import (
    fetch_weworkremotely_jobs
)
from sources.reddit import (
    fetch_reddit_jobs
)

def get_jobs():

    jobs = []

    jobs.extend(
        fetch_remoteok_jobs() or []
    )

    jobs.extend(
        fetch_weworkremotely_jobs() or []
    )

    jobs.extend(
        fetch_reddit_jobs() or []
    )


    print(f"Total jobs collected: {len(jobs)}")

    return jobs

