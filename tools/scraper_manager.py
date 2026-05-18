from sources.remoteok import fetch_remoteok_jobs


def get_jobs():

    jobs = []

    jobs.extend(fetch_remoteok_jobs())

    print(f"Total jobs collected: {len(jobs)}")

    return jobs


