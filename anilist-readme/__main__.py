from graphql import grapql
from config import ANILIST_QUERY
from actions_utils import getActionsInput, info
from ListActivity import ListActivity
from readme import open_readme, update_readme
from git import git_add_commit_push

if __name__ == "__main__":
    user_id: str = getActionsInput("USER_ID", False)
    preferred_language = getActionsInput("PREFERRED_LANGUAGE") or "english"
    max_post_count = int(getActionsInput("MAX_POST_COUNT") or "5")
    readme_path = getActionsInput("README_PATH") or "./README.md"
    commit_message = getActionsInput("COMMIT_MESSAGE") or "Update readme"
    gh_token = getActionsInput("GH_TOKEN", False)
    commit_email = getActionsInput("COMMIT_EMAIL", False)
    commit_username = getActionsInput("COMMIT_USERNAME", False)

    info(f"""Fetching Anilist data for user {user_id}
        with preffered langauge '{preferred_language}'""")

    response = grapql(ANILIST_QUERY, {"id": int(
        user_id), "post_count": int(max_post_count)})

    parsed = [ListActivity(activity, preferred_language)
              for activity in response["data"]["Page"]["activities"]]

    readme = open_readme(readme_path)
    update_readme(readme, readme_path, parsed)
    git_add_commit_push(readme_path, commit_message, gh_token, commit_email, commit_username)
