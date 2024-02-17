from cmath import log
from os import environ, walk, path

from .logger import logger
from .config import COMMENT_TEMPLATE
from .list_activity import ListActivity


def find_readme():
    """
    Find the readme file in the given current directory.
    """
    logger.info("Searching for the readme file...")
    readme_path = None    

    for root, _, files in walk(".", topdown=True):
        for file in files:
            if file.lower() == "readme.md":
                local_readme_path = path.join(root, file)

                if validate_readme(local_readme_path):
                    readme_path = local_readme_path
                    logger.info(f"Found matching readme file at '{local_readme_path}'")

    if readme_path:
        return readme_path
    else:
        raise FileNotFoundError("Unable to find readme file.")


def open_readme(readme: str) -> "list[str]":
    """
    Open the readme file and return the contents as a string.
    """
    logger.info(f"Opening readme in '{readme}'")

    with open(readme, "r", encoding="utf-8") as file:
        opened = file.read()
        return opened.splitlines()


def update_readme(
    readme_content: "list[str]", readme_path: str, activity_list: "list[ListActivity]"
) -> None:
    """
    Update the readme file with the given contents.
    """
    logger.info("Updating the readme contents...")

    if environ.get("DEV") == "true":
        # if we are in dev mode, write to a new file
        readme_path += ".dev"

    start_index, end_index = readme_comment_indexes(readme_content)
    top_part = "\n".join(readme_content[: start_index + 1])
    bottom_part = "\n".join(readme_content[end_index:])

    with open(readme_path, "w", encoding="utf-8") as file:
        new_content = (
            top_part
            + "\n\n"
            + "\n".join(map(lambda activity: str(activity), activity_list))
            + "\n\n"
            + bottom_part
            + "\n"
        )
        file.write(new_content)


def validate_readme(readme: "str") -> bool:
    """
    Validate the readme file.
    """
    logger.info("Validating the readme file...")

    try:
        readme_comment_indexes(open_readme(readme))

    except ValueError:
        logger.error(f"Failed to validate readme at: '{readme}'")
        return False

    return True


def readme_comment_indexes(readme: "list[str]") -> "tuple[int, int]":
    """
    Get index of comments generated from the COMMENT_TEMPLATE in the readme.
    """
    trimmed = [line.strip() for line in readme]

    start_index = trimmed.index(COMMENT_TEMPLATE.format("start"))
    end_index = trimmed.index(COMMENT_TEMPLATE.format("end"))

    if start_index != -1 and end_index != -1:
        return start_index, end_index

    raise ValueError("Unable to find start and end comments in readme file.")
