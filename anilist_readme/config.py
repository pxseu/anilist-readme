ANILIST_ENDPOINT = "https://graphql.anilist.co"
LIST_QUERY = """query ($id: Int, $post_count: Int) {
    Page(page: 1, perPage: $post_count) {
        activities(userId: $id, sort: ID_DESC, type: MEDIA_LIST) {
            ... on ListActivity {
                type
                createdAt
                progress
                status
                media {
                    title {
                        romaji
                        english
                        native
                    }
                siteUrl
                }
            }
        }
    }
}"""
USERNAME_QUERY = """query ($name: String) {
    User(name: $name) {
        id
    }
}"""

EMOJI_DICT = {"MANGA_LIST": "📖", "ANIME_LIST": "📺"}

COMMENT_TEMPLATE = "<!-- ANILIST_ACTIVITY:{} -->"
CMD_STR = "::"
