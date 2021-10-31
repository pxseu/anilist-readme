from datetime import datetime
from enum import auto, Enum

from .config import EMOJI_DICT


class Language(Enum):
    romanji = auto()
    english = auto()
    native = auto()


def validate_language(lang: str) -> Language:
    """
    Check if the language is valid.
    """
    languages = [x.name for x in Language]
    if lang in languages:
        return Language[lang]
    raise ValueError(f"'{lang}'' is not a valid language. Must be: '{', '.join(languages)}'")


class ListActivity:
    def __init__(self, activity_data: dict, preferred_lang: Language = None) -> None:
        self.type: str = activity_data["type"]
        self.created_at = datetime.utcfromtimestamp(activity_data["createdAt"]).strftime("%H:%M, %d %B %Y")
        self.progress: str = activity_data["progress"]
        self.status: str = activity_data["status"]
        self.title: str = (
                activity_data["media"]["title"][preferred_lang.name or "english"] or
                activity_data["media"]["title"]["romaji"]
        )
        self.url: str = activity_data["media"]["siteUrl"]

    def __str__(self) -> str:
        return f"-   {EMOJI_DICT[self.type]} {self.status.capitalize()} {f'{self.progress} of ' if self.progress else ''}[{self.title}]({self.url}) ({self.created_at})"
