import requests
import time
import random
from pathlib import Path
from dotenv import load_dotenv
import os
from config.logger import logger


script_dir = Path(__file__).parent
env_path = script_dir.parent / '.env'

load_dotenv(dotenv_path=env_path)

GMAP_API_KEY = os.getenv('GMAP_API_KEY')


SEARCH_QUERIES = [
    "restaurants in Lyon",
    "dentists in Lyon",
    "gyms in Lyon",
    "beauty salons in Lyon",
    "real estate agencies in Lyon"
]





TEXT_SEARCH_URL = (
    "https://maps.googleapis.com/maps/api/place/textsearch/json"
)

PLACE_DETAILS_URL = (
    "https://maps.googleapis.com/maps/api/place/details/json"
)


def fetch_place_details(place_id):


    try:
        
        params = {

            "place_id": place_id,

            "fields": (
                "name,"
                "formatted_address,"
                "website,"
                "formatted_phone_number,"
                "url"
            ),

            "key": GMAP_API_KEY
        }

        response = requests.get(
            PLACE_DETAILS_URL,
            params=params,
            timeout=10
        )

        if response.status_code != 200:

            logger.info(f"Place Details bad status: {response.status_code}")

            return None

        data = response.json()

        result = data.get("result")

        if not result:
            return None

        return result

    except Exception as e:

        logger.warning("Failed fetching place details")
        logger.exception(e)


        return None


def fetch_google_maps_leads():

    jobs = []

    seen_place_ids = set()

    try:

        if not os.getenv('GMAP_API_KEY'):

            logger.info("Your Google maps API key is missing")

            return []

        for query in SEARCH_QUERIES:

            logger.info(f"Searching Google Maps: {query}")

            params = {

                "query": query,

                "key": GMAP_API_KEY
            }

            response = requests.get(
                TEXT_SEARCH_URL,
                params=params,
                timeout=10
            )

            if response.status_code != 200:

                logger.info(f"Google Maps bad status: {response.status_code}")

                continue

            data = response.json()

            results = data.get(
                "results",
                []
            )

            logger.info(f"{query}: {len(results)} places found")

            for place in results:

                try:

                    place_id = place.get(
                        "place_id"
                    )

                    if not place_id:
                        continue

                    if place_id in seen_place_ids:
                        continue

                    seen_place_ids.add(place_id)

                    # polite delay
                    time.sleep(
                        random.uniform(2, 3)
                    )

                    details = fetch_place_details(
                        place_id
                    )

                    if not details:
                        continue

                    name = details.get("name")

                    address = details.get(
                        "formatted_address"
                    )

                    website = details.get(
                        "website"
                    )

                    phone = details.get(
                        "formatted_phone_number"
                    )

                    maps_url = details.get(
                        "url"
                    )


                    job = {

                        "title": name,

                        "description": (
                            f"Address: {address} "
                            f"Phone: {phone}"
                        ),

                        "client_name": name,
                        "client_email": None,
                        "client_website": website,
                        "url": maps_url,

                    }

                    jobs.append(job)

                except Exception as inner_error:

 
                    logger.warning("Failed parsing place")
                    logger.exception(inner_error)



        logger.info(f"Google Maps: fetched {len(jobs)} leads")

        return jobs

    except Exception as e:

        logger.warning("Google Maps scraper failed")
        logger.exception(e)

        return []