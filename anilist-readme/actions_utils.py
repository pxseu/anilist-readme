import os
import json
from typing import Union
from config import CMD_STR


def getActionsInput(value: str, optional: bool = True) -> Union[str, None]:
    # remove all spaces to undersocres
    value = value.replace(' ', '_')

    # get the value in uppercase from env prefixed with INPUT_
    try:
        return os.environ[f'INPUT_{value.upper()}']
    except:
        if optional:
            return None
        else:
            raise ValueError(f'{value} is required')


def info(msg: str) -> None:
    print(f'[INFO] {msg}')


def add_secret(secret: str) -> None:
    print(f'{CMD_STR}add-mask{CMD_STR}{escapeData(secret)}')


def escapeData(data: str) -> str:
    data = json.dumps(data)
    data = data.replace('%', '%25')
    data = data.replace("\n", "%0A")
    data = data.replace("\r", "%0D")
    return data
