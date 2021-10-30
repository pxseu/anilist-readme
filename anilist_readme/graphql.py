import httpx
from time import sleep

from .actions_utils import error, info
from .config import ANILIST_ENDPOINT


def grapql(query: str, variables: "dict[str]" = None, retry: int = 5, delay: float = 0.2) -> dict:
    """
    Makes a graphql request to the ANILIST_ENDPOINT, and returns the response.
    Uses query and variables in body
    """
    info("Making a POST request to ANILIST_ENDPOINT")

    # make the requests
    res = httpx.post(ANILIST_ENDPOINT, json={"query": query, "variables": variables})

    if res.is_error:
        # if the request is not ok, retry
        if retry > 0:
            # wait for a while
            sleep(delay)
            error(f"Error making graphql request: {res.status_code}, tries left: {retry}")

            # retry
            return grapql(
                query,
                variables,
                retry - 1,
                delay * 2,
            )
        # if the request is not ok, and retry is 0, return the error
        else:
            raise Exception(f"Error making graphql request: {res.status_code}")

    return res.json()
