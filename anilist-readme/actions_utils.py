from typing import Union
import os


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


def escape_data(data: str) -> str:
    data = data.replace('%', '%25')
    data = data.replace('\n', '%0A')
    data = data.replace('\r', '%0D')
    data = data.replace(':', '%3A')
    data = data.replace(',', '%2C')
    return data
