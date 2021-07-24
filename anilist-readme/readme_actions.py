from typing import List
from config import COMMENT_TEMPLATE


def open_readme(readme):
    """
    Open the readme file and return the contents as a string.
    """
    with open(readme, "r") as file:
        opened = file.read()
        readme_contents = opened.splitlines()

    return readme_contents


def update_readme(readme_content: List[str], readme_path: str, activity_list):
    """
    Update the readme file with the given contents.
    """
    indexes = readme_comment_indexes(readme_content)
    top_part = "\n".join(readme_content[: (indexes[0] + 1)])
    bottom_part = "\n".join(readme_content[indexes[1] :])

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


def readme_comment_indexes(readme: List[str]):
    """
    Get index of comments generated from the COMMENT_TEMPLATE in the readme.
    """

    start_index = readme.index(COMMENT_TEMPLATE.format("start"))
    end_index = readme.index(COMMENT_TEMPLATE.format("end"))

    if start_index != -1 and end_index != -1:
        return [start_index, end_index]
    else:
        raise ValueError("Unable to find start and end comments in readme file.")
