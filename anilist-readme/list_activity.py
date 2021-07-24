from typing import Literal
from config import EMOJI_DICT
from datetime import datetime

prefferd_lang_type = Literal["romaji", "english", "native"]
prefferd_lang_tuple = ("romaji", "english", "native")


class ListActivity:
    def __init__(self, activity_data: dict, preffered_lang: prefferd_lang_type = None) -> None:
        if preffered_lang not in prefferd_lang_tuple:
            raise Exception(f"{preffered_lang} is not a valid language")

        self.type: str = activity_data["type"]
        self.created_at = datetime.utcfromtimestamp(activity_data["createdAt"]).strftime("%H:%M, %d %B %Y")
        self.progress: str = activity_data["progress"]
        self.status: str = activity_data["status"]
        self.title: str = (
            activity_data["media"]["title"][preffered_lang or "english"] or activity_data["media"]["title"]["romaji"]
        )
        self.url: str = activity_data["media"]["siteUrl"]

    def __str__(self) -> str:
        return f"-   {EMOJI_DICT[self.type]} {self.status.capitalize()} {f'{self.progress} of ' if self.progress else ''}[{self.title}]({self.url}) ({self.created_at})"
