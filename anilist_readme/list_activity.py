from datetime import datetime, tzinfo
from enum import auto, Enum
from typing import Optional

import pytz

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
    raise ValueError(
        f"'{lang}'' is not a valid language. Must be: '{', '.join(languages)}'"
    )


class ListActivity:
    def __init__(
        self,
        activity_data: dict,
        tz: str,
        preferred_lang: Language,
        format_date: str,
    ) -> None:
        self.type: str = activity_data["type"]
        self.created_at = custom_datetime_format(
            dt=datetime.fromtimestamp(activity_data["createdAt"], pytz.timezone(tz)),
            format_date=format_date,
        )
        self.progress: str = activity_data["progress"]
        self.status: str = activity_data["status"]
        self.title: str = (
            activity_data["media"]["title"][
                preferred_lang.name if preferred_lang else "english"
            ]
            or activity_data["media"]["title"]["romaji"]
        )
        self.url: str = activity_data["media"]["siteUrl"]

    def __str__(self) -> str:
        return f"-   {EMOJI_DICT[self.type]} {self.status.capitalize()} {f'{self.progress} of ' if self.progress else ''}[{self.title}]({self.url}) ({self.created_at})"


def custom_datetime_format(dt: datetime, format_date: str) -> str:
    new_format = (
        format_date.replace("{h}", "%H")
        .replace("{m}", "%M")
        .replace("{D}", "%d")
        .replace("{M}", "%m")
        .replace("{MW}", "%B")
        .replace("{Y}", "%Y")
    )

    return dt.strftime(new_format)
