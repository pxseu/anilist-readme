import os
from shlex import quote


def git_add_commit_push(readme_path: str, message: str, gh_token: str, email: str, username: str) -> None:
    # commit the change and push to your repo
    os.system(f"git config --global user.email {quote(email)}")
    os.system(f"git config --global user.name {quote(username)}")
    os.system(f"git remote set-url origin https://{gh_token}@github.com/{os.environ['GITHUB_REPOSITORY']}.git")
    os.system(f"git add {readme_path}")
    os.system(f"git commit -m  {quote(message)}")
    os.system(f"git push")
