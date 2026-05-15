def is_good_lead(job):
    keywords = ["wordpress", "website", "landing page"]

    return any(k in job["title"].lower() for k in keywords)