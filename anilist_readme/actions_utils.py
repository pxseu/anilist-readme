from .logger import logger
import json
from os import environ
from typing import Optional

from .config import CMD_STR


def actions_input(value: str, optional: bool) -> Optional[str]:
    # remove all spaces to underscores
    value = value.replace(" ", "_")

    # get the value in uppercase from env prefixed with INPUT_
    output = environ.get(f"INPUT_{value.upper()}", default=None)

    logger.debug(f"actions_input: {value}={output}")

    if output or optional:
        return output

    raise ValueError(f"{value} is required")


def add_secret(secret: str) -> None:
    print(f"{CMD_STR}add-mask{CMD_STR}{escape_data(secret)}")


def escape_data(data: str) -> str:
    data = json.dumps(data)
    data = data.replace("%", "%25")
    data = data.replace("\n", "%0A")
    data = data.replace("\r", "%0D")
    return data
