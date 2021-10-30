from os import environ
import json
from typing import Union
from .config import CMD_STR


def actions_input(value: str, optional: bool = True) -> Union[str, None]:
    # remove all spaces to underscores
    value = value.replace(" ", "_")

    # get the value in uppercase from env prefixed with INPUT_
    try:
        return environ[f"INPUT_{value.upper()}"]
    except:
        if optional:
            return None
        else:
            raise ValueError(f"{value} is required")


def info(msg: str) -> None:
    print(f"[INFO] {msg}")


def error(msg: str) -> None:
    print(f"[ERROR] {msg}")


def add_secret(secret: str) -> None:
    print(f"{CMD_STR}add-mask{CMD_STR}{escape_data(secret)}")


def escape_data(data: str) -> str:
    data = json.dumps(data)
    data = data.replace("%", "%25")
    data = data.replace("\n", "%0A")
    data = data.replace("\r", "%0D")
    return data
