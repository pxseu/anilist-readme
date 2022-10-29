from time import sleep
from typing import Any, Dict, Optional, AnyStr

import httpx

from .logger import logger
from .config import ANILIST_ENDPOINT


def grapql(
    query: str,
    variables: Optional[Dict[str, Any]] = None,
    retry: int = 5,
    delay: float = 0.2,
) -> dict:
    """
    Makes a graphql request to the ANILIST_ENDPOINT, and returns the response.
    Uses query and variables in body
    """
    logger.info("Making a POST request to ANILIST_ENDPOINT")

    # make the requests
    res = httpx.post(ANILIST_ENDPOINT, json={"query": query, "variables": variables})

    logger.debug(f"Response status: {res.status_code}")

    if not res.is_error:
        return res.json()

    # if the request is not ok, and retry is 0, return the error
    if retry <= 0:
        res.raise_for_status()

    # if the request is not ok, retry
    # wait for a while
    sleep(delay)
    logger.error(
        f"Error making graphql request: {res.status_code}, tries left: {retry}"
    )

    # retry
    return grapql(
        query=query,
        variables=variables,
        retry=retry - 1,
        delay=delay * 2,
    )
