import requests
from config import ANILIST_ENDPOINT


def grapql(query: str, variables: "dict[str]" = None) -> dict:
    """
    Makes a graphql request to the ANILIST_ENDPOINT, and returns the response.
    Uses query and variables in body
    """
    req = requests.post(ANILIST_ENDPOINT, json={
        "query": query,
        "variables": variables
    })

    if not req.ok:
        raise Exception(f"Error making graphql request: {req.status_code}")

    return req.json()
