from anilist_readme.actions_utils import actions_input, add_secret
from anilist_readme.config import ANILIST_QUERY
from anilist_readme.git import git_add_commit_push
from anilist_readme.graphql import grapql
from anilist_readme.list_activity import ListActivity, validate_language
from anilist_readme.readme_actions import find_readme, open_readme, update_readme


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
    language = validate_language(preferred_language)

    response = grapql(ANILIST_QUERY, {"id": int(user_id), "post_count": int(max_post_count)})
    parsed = [ListActivity(activity, language) for activity in response["data"]["Page"]["activities"]]
    readme = open_readme(readme_path)
    update_readme(readme, readme_path, parsed)
    add_secret(gh_token)
    git_add_commit_push(readme_path, commit_message, gh_token, commit_email, commit_username)


if __name__ == "__main__":
    user_id = actions_input("USER_ID", optional=False)
    preferred_language = actions_input("PREFERRED_LANGUAGE", optional=False)
    max_post_count = actions_input("MAX_POST_COUNT", optional=False)
    readme_path = actions_input("README_PATH", optional=True) or find_readme()
    commit_message = actions_input("COMMIT_MESSAGE", optional=False)
    gh_token = actions_input("GH_TOKEN", optional=False)
    commit_email = actions_input("COMMIT_EMAIL", optional=False)
    commit_username = actions_input("COMMIT_USERNAME", optional=False)

    main(
        user_id=user_id,
        preferred_language=preferred_language,
        max_post_count=max_post_count,
        readme_path=readme_path,
        commit_message=commit_message,
        gh_token=gh_token,
        commit_email=commit_email,
        commit_username=commit_username,
    )
