from os import environ, system
from shlex import quote

from .logger import logger


def git_add_commit_push(readme_path: str, message: str, gh_token: str, email: str, username: str) -> None:
    # commit the change and push to your repo
    logger.info("Committing the changes")

    if environ.get("DEV") == "true":
        logger.debug("Skipping git commit and push due to DEV=true")
        # if we are in dev mode, we don't commit
        return

    system(f"git config --global user.email {quote(email)}")
    system(f"git config --global user.name {quote(username)}")
    system(f"git remote set-url origin https://{gh_token}@github.com/{environ['GITHUB_REPOSITORY']}.git")
    system(f"git add {readme_path}")
    system(f"git commit -m  {quote(message)}")
    system("git push")
