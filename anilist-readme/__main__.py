from graphql import grapql
from config import ANILIST_QUERY
from actions_utils import getActionsInput, info, add_secret
from list_activity import ListActivity
from readme_actions import open_readme, update_readme
from git import git_add_commit_push


def main(
    user_id: str,
    preferred_language: str,
    max_post_count: str,
    readme_path: str,
    commit_message: str,
    gh_token: str,
    commit_email: str,
    commit_username: str,
):
    info(f"Fetching Anilist data for user {user_id}")
    info(f"with preffered langauge '{preferred_language}'")
    response = grapql(ANILIST_QUERY, {"id": int(user_id), "post_count": int(max_post_count)})

    info(f"Parsing the response")
    parsed = [ListActivity(activity, preferred_language) for activity in response["data"]["Page"]["activities"]]

    info(f"Opening readme in '{readme_path}'")
    readme = open_readme(readme_path)

    info(f"Updating the readme")
    update_readme(readme, readme_path, parsed)

    info(f"Commiting the changes")
    add_secret(gh_token)
    git_add_commit_push(readme_path, commit_message, gh_token, commit_email, commit_username)


if __name__ == "__main__":
    user_id: str = getActionsInput("USER_ID", False)
    preferred_language = getActionsInput("PREFERRED_LANGUAGE") or "english"
    max_post_count = int(getActionsInput("MAX_POST_COUNT") or "5")
    readme_path = getActionsInput("README_PATH") or "./README.md"
    commit_message = getActionsInput("COMMIT_MESSAGE") or "Update readme"
    gh_token = getActionsInput("GH_TOKEN", False)
    commit_email = getActionsInput("COMMIT_EMAIL", False)
    commit_username = getActionsInput("COMMIT_USERNAME", False)

    main(
        user_id,
        preferred_language,
        max_post_count,
        readme_path,
        commit_message,
        gh_token,
        commit_email,
        commit_username,
    )
