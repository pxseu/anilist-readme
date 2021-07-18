import os
from shlex import quote


def git_add_commit_push(readme_path: str, message: str) -> None:
    # commit the change and push to your repo
    os.system(f"git add {readme_path}")
    # os.system(f'git commit -m  {quote(message)}')
    # os.system(f'git push')
