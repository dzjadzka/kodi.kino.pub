## Trakt Lists
Some lists require a user to authenticate their Trakt account

| Additional Supported Parameters | [Filter](https://github.com/jurialmunkey/plugin.video.themoviedb.helper/wiki/Lists-Additional-Params#optional-exclusion-and-filter-parameters) | [Widget](https://github.com/jurialmunkey/plugin.video.themoviedb.helper/wiki/Lists-Additional-Params#additional-widget-parameters) |
| :--- | :--- | :--- |

| Name | Path | Types |
| :--- | :--- | :--- |
| Watchlist  | `plugin://plugin.video.themoviedb.helper?info=trakt_watchlist&amp;type=movie` | `movie` `tv`  |
| In-Progress (Unfinished Shows / Movies) | `plugin://plugin.video.themoviedb.helper?info=trakt_inprogress&amp;type=tv` | `movie` `tv`  |
| On Deck (Unfinished Episodes)  | `plugin://plugin.video.themoviedb.helper?info=trakt_ondeck&amp;type=tv` | `tv`  |
| Still to Watch (Watchlist + In-Progress) | `plugin://plugin.video.themoviedb.helper?info=trakt_towatch&amp;type=movie` | `movie` `tv`  |
| Next Episodes | `plugin://plugin.video.themoviedb.helper?info=trakt_nextepisodes&amp;type=tv` | `tv`  |
| Recommended Because You Recently Watched | `plugin://plugin.video.themoviedb.helper?info=trakt_becauseyouwatched&amp;type=tv` | `movie` `tv`  |
| Recommended Because You Most Watched | `plugin://plugin.video.themoviedb.helper?info=trakt_becausemostwatched&amp;type=tv` | `movie` `tv`  |
| History | `plugin://plugin.video.themoviedb.helper?info=trakt_history&amp;type=movie` | `movie` `tv`  |
| Most Watched| `plugin://plugin.video.themoviedb.helper?info=trakt_mostwatched&amp;type=movie` | `movie` `tv`  |
| Recommend | `plugin://plugin.video.themoviedb.helper?info=trakt_recommendations&amp;type=movie` | `movie` `tv`  |
| Your Shows Airing This Week  | `plugin://plugin.video.themoviedb.helper?info=trakt_myairing&amp;type=tv` | `tv`  |
| Trending  | `plugin://plugin.video.themoviedb.helper?info=trakt_trending&amp;type=movie` | `movie` `tv`  |
| Popular (Across all Users)  | `plugin://plugin.video.themoviedb.helper?info=trakt_popular&amp;type=movie` | `movie` `tv`  |
| Most Played (Across all Users)  | `plugin://plugin.video.themoviedb.helper?info=trakt_watchlist&amp;type=movie` | `movie` `tv`  |
| Anticipated  | `plugin://plugin.video.themoviedb.helper?info=trakt_anticipated&amp;type=movie` | `movie` `tv`  |
| Top 10 Box Office This Week  | `plugin://plugin.video.themoviedb.helper?info=trakt_boxoffice&amp;type=movie` | `movie` `tv`  |
| Trending Lists  | `plugin://plugin.video.themoviedb.helper?info=trakt_trendinglists&amp;type=both` | `both`  |
| Popular Lists  | `plugin://plugin.video.themoviedb.helper?info=trakt_popularlists&amp;type=both` | `both`  |
| Liked Lists  | `plugin://plugin.video.themoviedb.helper?info=trakt_likedlists&amp;type=both` | `both`  |
| Your Lists  | `plugin://plugin.video.themoviedb.helper?info=trakt_mylists&amp;type=both` | `both`  |
| Specific List by a User  | `plugin://plugin.video.themoviedb.helper?info=trakt_userlist&amp;type=both&amp;list_slug=get-to-the-choppa&amp;user_slug=justin` | `both`  |