from .logger import logger
import json
from os import environ
from typing import Optional

from .config import CMD_STR

SECRET_VALUES = ["GH_TOKEN", "COMMIT_EMAIL", "COMMIT_USERNAME"]

def add_secret(secret: str) -> None:
    print(f"{CMD_STR}add-mask{CMD_STR}{escape_data(secret)}")

def actions_input(value: str, optional: bool) -> Optional[str]:
    # remove all spaces to underscores
    value = value.replace(" ", "_")

    # get the value in uppercase from env prefixed with INPUT_
    output = environ.get(f"INPUT_{value.upper()}", default=None)

    # mask even in debug logs
    if value.upper() in SECRET_VALUES and output:
        add_secret(output)

    logger.debug(f"actions_input: {value}={output}")

    if output or optional:
        return output

    raise ValueError(f"{value} is required")


def escape_data(data: str) -> str:
    data = json.dumps(data)
    data = data.replace("%", "%25")
    data = data.replace("\n", "%0A")
    data = data.replace("\r", "%0D")
    return data
