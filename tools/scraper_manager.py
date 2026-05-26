from sources.remoteok import (
    fetch_remoteok_jobs
)
from sources.weworkremotely import (
    fetch_weworkremotely_jobs
)
from sources.reddit import (
    fetch_reddit_jobs
)
from sources.hackernews import (
    fetch_hackernews_jobs
)
from sources.google_maps import (
    fetch_google_maps_leads
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

    jobs.extend(
        fetch_hackernews_jobs() or []
    )

    jobs.extend(
        fetch_google_maps_leads() or []
    )

    


    print(f"Total jobs collected: {len(jobs)}")
    print("-------------------------------------------------------")

    return jobs

