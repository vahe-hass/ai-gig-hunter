from sources.remoteok import fetch_remoteok_jobs
from sources.weworkremotely import (
    fetch_weworkremotely_jobs
)


def get_jobs():

    jobs = []

    remoteok_jobs = fetch_remoteok_jobs() or []

    wwr_jobs = fetch_weworkremotely_jobs() or []

    jobs.extend(remoteok_jobs)

    jobs.extend(wwr_jobs)

    print(f"Total jobs collected: {len(jobs)}")

    return jobs

