# AniList readme workflow

> Simple workflow that will add your latest activity into your readme!

[![forthebadge](https://forthebadge.com/images/badges/made-with-python.svg)](https://forthebadge.com)
[![forthebadge](https://forthebadge.com/images/badges/0-percent-optimized.svg)](https://forthebadge.com)
[![forthebadge](https://forthebadge.com/images/badges/it-works-why.svg)](https://forthebadge.com)

## Note

This was made by a person who primarily uses TypeScript and doesn't know how to use Python.

## How to

Simply add this to your README.md

```html
# 🌸 My recent AniList activity

<!-- ANILIST_ACTIVITY:start -->

<!-- ANILIST_ACTIVITY:end -->
```

and setup the workflow file at `.github/workflows/anilist.yml` like this:

```yml
name: AniList readme workflow
on:
  schedule:
    # Runs every hour
    - cron: "0 * * * *"
  workflow_dispatch: # for manual debuging

jobs:
  update-readme-with-anilist:
    name: Update this repo's README with latest AniList activites
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: AniList readme workflow
        uses: pxseu/anilist-readme@senpai # latest version
        with:
          user_id: YOUR_USER_ID # or
          user_name: YOUR_USER_NAME
```

## Settings

| Option               | Description                                                      | Default                                | Required |
| -------------------- | ---------------------------------------------------------------- | -------------------------------------- | -------- |
| `user_id`            | Your AniList user id                                             | ""                                     | `True`   |
| `user_name`          | Your AniList username                                            | ""                                     | `True`   |
| `max_post_count`     | A number from 1 to 50 limiting the ammount of posts              | "5"                                    | `False`  |
| `preferred_language` | The language of the list content (e.g. Romaji, English, Native)  | "english"                              | `False`  |
| `timezone`           | Timezone of the list content (e.g. Europe/Berlin)                | "UTC"                                  | `False`  |
| `date_format`        | Date format of the list content (e.g. {D}/{M or MW}/{Y} {h}:{m}) | "{h}:{m} {D} {MW} {Y}"                 | `False`  |
| `readme_path`        | Path to the readme file to edit                                  | "./README.md"                          | `False`  |
| `gh_token`           | Authorized github token                                          | ${{ github.token }}                    | `False`  |
| `commit_message`     | A message to use when commiting                                  | "Update AniList activity in README.md" | `False`  |
| `commit_username`    | The username for the commiter                                    | "GitHub Action"                        | `False`  |
| `commit_email`       | The email for the commiter                                       | "action@github.com"                    | `False`  |

> Note: Eiter `user_id` or `user_name` is required! \
> I recommend you leave the default `commit_username` and `commit_email` \
> For `date_format` months: {M} will result in a number (e.g '3') & {MW} will result in a string (e.g 'March') \
> If you're unsure what's your User ID on AniList follow the quide below

## How to get my user ID

If you change your username frequently or you're unsure what your user id is, you can use the AniList API to get it.
Head on over to https://anilist.co/graphiql and input the query below and replace `YOUR_USERNAME` with your username.

```gql
query {
  User(name: "YOUR_USERNAME") {
    id
    name
  }
}
```

The query above will return your username and your id which you can use for this action.

## Example

You can find it on my [profile](https://github.com/pxseu/pxseu/blob/a2980f3165f0ed86d5469ee35b8ff38e12116794/README.md)!
