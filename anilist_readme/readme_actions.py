from os import environ, walk, path
from .list_activity import ListActivity
from .actions_utils import info
from .config import COMMENT_TEMPLATE


def find_readme():
    """
    Find the readme file in the given current directory.
    """
    info("Searching for the readme file...")
    readme_path = None

    for root, dirs, files in walk("."):
        for file in files:
            if file.lower() == "readme.md":
                readme_path = path.join(root, file)
                break

    if readme_path:
        info(f"Found readme file at: '{readme_path}'")
        return readme_path
    else:
        raise FileNotFoundError("Unable to find readme file.")


def open_readme(readme: str):
    """
    Open the readme file and return the contents as a string.
    """
    info(f"Opening readme in '{readme}'")

    with open(readme, "r") as file:
        opened = file.read()
        readme_contents = opened.splitlines()

    return readme_contents


def update_readme(readme_content: "list[str]", readme_path: str, activity_list: "list[ListActivity]"):
    """
    Update the readme file with the given contents.
    """
    info("Updating the readme contents")

    if environ.get("DEV") == "true":
        # if we are in dev mode, we don't commit
        return

    indexes = readme_comment_indexes(readme_content)
    top_part = "\n".join(readme_content[: (indexes[0] + 1)])
    bottom_part = "\n".join(readme_content[indexes[1]:])

    with open(readme_path, "w") as file:
        new_content = (
                top_part
                + "\n\n"
                + "\n".join(map(lambda activity: str(activity), activity_list))
                + "\n\n"
                + bottom_part
                + "\n"
        )
        file.write(new_content)


def readme_comment_indexes(readme: "list[str]"):
    """
    Get index of comments generated from the COMMENT_TEMPLATE in the readme.
    """
    trimmed = [line.strip() for line in readme]

    start_index = trimmed.index(COMMENT_TEMPLATE.format("start"))
    end_index = trimmed.index(COMMENT_TEMPLATE.format("end"))

    if start_index != -1 and end_index != -1:
        return [start_index, end_index]
    else:
        raise ValueError("Unable to find start and end comments in readme file.")
