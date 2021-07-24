# AniList readme workflow

> Simple workflow that will add your latest activity into your readme!

[![forthebadge](https://forthebadge.com/images/badges/made-with-python.svg)](https://forthebadge.com)
[![forthebadge](https://forthebadge.com/images/badges/0-percent-optimized.svg)](https://forthebadge.com)
[![forthebadge](https://forthebadge.com/images/badges/it-works-why.svg)](https://forthebadge.com)

## Note

This was made by a person who uses primarly TypeScript which does not know how to use Python.

## How to

Simply add this to your README.md

```html
# 🌸 My recent AniList activity

<!-- ANILIST_ACTIVITY:start -->

<!-- ANILIST_ACTIVITY:end -->
```

and setup the workflow like this:

```yml
name: AniList readme workflow
on:
    schedule:
        # Runs every hour
        - cron: "0 * * * *"
    workflow_dispatch:

jobs:
    update-readme-with-anilist:
        name: Update this repo's README with latest AniList activites
        runs-on: ubuntu-latest
        steps:
            - uses: actions/checkout@v2
            - name: AniList readme workflow
              uses: pxseu/anilist-readme@v1.2.1
              with:
                  user_id: YOUR_USER_ID
```

## Settings

| Option            | Description                                         | Default                                | Required |
| ----------------- | --------------------------------------------------- | -------------------------------------- | -------- |
| `user_id`         | Your AniList user id                                | ""                                     | `True`   |
| `gh_token`        | Auhtorized github token                             | ${{ github.token }}                    | `False`  |
| `readme_path`     | Path to the readme file to edit                     | "./README.md"                          | `False`  |
| `max_post_count`  | A number from 1 to 50 limiting the ammount of posts | "5"                                    | `False`  |
| `commit_message`  | A message to use when commiting                     | "Update AniList activity in README.md" | `False`  |
| `commit_username` | The username for the commiter                       | "GitHub Action"                        | `False`  |
| `commit_email`    | The email for the commiter                          | "action@github.com"                    | `False`  |

> Note: I recommend you leave the default `commit_username` and `commit_email` \
> If you're unsure what's your User ID on AniList follow the quide bellow

## How the get my user id

Head on over to https://anilist.co/graphiql and input the query bellow and replacing `YOUR_USERNAME` with your username.

```gql
query {
	User(name: "YOUR_USERNAME") {
		id
		name
	}
}
```

Above query will return you your username next to your id with which you can use this action.

## Example

You can find it on my [profile](https://github.com/pxseu/pxseu/blob/a2980f3165f0ed86d5469ee35b8ff38e12116794/README.md)!
