from os import environ
from shlex import quote
from datetime import timedelta, datetime, timezone
from dateutil.parser import parse

from .logger import logger
from .system import syscmd

def git_config(email: str, username: str, gh_token: str) -> None:
    if environ.get("DEV") == "true":
        logger.debug("Skipping git config due to DEV=true")
        return
    
    syscmd(f"git config --global user.email {quote(email)}")
    syscmd(f"git config --global user.name {quote(username)}")
    syscmd(
        f"git remote set-url origin https://{gh_token}@github.com/{environ['GITHUB_REPOSITORY']}.git"
    )

def git_add_commit_push(
    readme_path: str, message: str, gh_token: str, email: str, username: str
) -> None:
    # commit the change and push to your repo
    logger.info("Committing the changes")

    if environ.get("DEV") == "true":
        logger.debug("Skipping git commit and push due to DEV=true")
        # if we are in dev mode, we don't commit
        return

    git_config(email, username, gh_token)
    syscmd(f"git add {readme_path}")
    syscmd(f"git commit -m  {quote(message)}")
    syscmd("git push")

# since github suspends actions that are in repos inactive for more than 60 days, we need to commit something to the repo to keep it active
def git_check_activity(gh_token: str, email: str, username: str) -> None:
    git_config(email, username, gh_token)
    git_log = syscmd(f"git --no-pager log -1 --pretty=format:'%cI'", capture_output=True, encoding='utf-8')
    last_commit_activity = parse(git_log)

    # safer to run a few days before the 60 days limit
    if last_commit_activity < datetime.now(timezone.utc) - timedelta(days=59):
        if environ.get("DEV") == "true":
            logger.debug("Skipping inactive commit due to DEV=true")
            return

        syscmd(f"git commit --allow-empty -m {quote('AniList readme workflow, dummy commit')}")
        syscmd("git push")