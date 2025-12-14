## Next Aired Calendar

TMDbHelper provides lists to retrieve episodes airing on a certain day or within a certain range. These lists can be based off the library or the user's trakt account.

| Additional Supported Parameters | [Filter](https://github.com/jurialmunkey/plugin.video.themoviedb.helper/wiki/Lists-Additional-Params#optional-exclusion-and-filter-parameters) | [Widget](https://github.com/jurialmunkey/plugin.video.themoviedb.helper/wiki/Lists-Additional-Params#additional-widget-parameters) |
| :--- | :--- | :--- |

| Examples |  |
| :--- | :--- |
| Library | `plugin://plugin.video.themoviedb.helper?info=library_nextaired&amp;startdate=0&amp;days=1` |
| Trakt | `plugin://plugin.video.themoviedb.helper?info=trakt_calendar&amp;startdate=0&amp;days=1` |

These lists are particularly useful if you want to create a Custom Skin Window as a replacement for the Next Aired script addon. Because TMDbHelper provides theses lists as plugin paths, there is greater flexibility in how you display these lists (unlike a scripted window which requires specific IDs and controls).

## Available parameters

| Param | Description |
| :--- | :--- |
| `&amp;startdate=` | The number of days from today to start the range from. e.g. `startdate=0` is Today, `startdate=1` is Tomorrow. Accepts negative values e.g. `startdate=-1` is from Yesterday and `startdate=-7` is from one week ago. |
| `&amp;days=` | The number of days to include in the range starting from the startdate. Any combination can be used to capture a specific range e.g. `startdate=0&amp;days=1` contains episodes airing today; `startdate=1&amp;days=1` contains episodes airing tomorrow; `startdate=0&amp;days=7`contains episodes airing this week; `startdate=-1&amp;days=8`contains episodes airing this week and also includes yesterday; `startdate=-7&amp;days=14`contains episodes airing from last week AND this week; etc. |
| `&amp;user=false` | Use with `info=trakt_calendar` to get ALL airing episodes not just the user's |
| `&amp;endpoint=premieres` | Use with `info=trakt_calendar` to get ONLY season premieres |
| `&amp;endpoint=new` | Use with `info=trakt_calendar` to get ONLY new tvshows |

## Special ListItem.Infolabels for Calendar episodes

| Infolabel | Description |
| :--- | :--- |
| `ListItem.Property(air_date)` | Formatted air date using "Long date format" setting in Kodi Settings > Interface > Region > |
| `ListItem.Property(air_time)` | Formatted air time using "Time format" setting in Kodi Settings > Interface > Region > |
| `ListItem.Property(air_day)` | Formatted air day using "%A" e.g. "Monday" "Tuesday" etc. |
| `ListItem.Property(air_day_short)` | Formatted air day using "%a" e.g. "Mon" "Tues" etc. |
| `ListItem.Property(air_date_short)` | Formatted air date using "%d %b" e.g. "25-Oct" "05-Sep" etc. |
| `ListItem.Year` | Formatted air date using "%Y" e.g. "2021" |
| `ListItem.Premiered` | Formatted air date using "Short date format" setting in Kodi Settings > Interface > Region >  |
| `ListItem.Property(widget)` | Contains information about the calendar list startdate and days setting. See below table for possible values |

NOTE: By default a tvshow with multiple episodes airing on the same day will be "stacked" into a single item in the calendar. The following `stacked_` properties are only available if the item has been stacked.

| Infolabel | Description |
| :--- |  :--- |
| ListItem.Property(stacked_count) | Number of episodes in the stack |
| ListItem.Property(stacked_labels) | Comma separated list of episode labels e.g. `5x01 - Ep1Title, 5x02 - Ep2Title, 5x03 - Ep3Title` |
| ListItem.Property(stacked_titles) |  Comma separated list of episode titles e.g. `Ep1Title, Ep2Title, Ep3Title` |
| ListItem.Property(stacked_episodes) | Comma separated lists of episode numbers e.g. `5x01, 5x02, 5x03` |
| ListItem.Property(stacked_first) | First episode number in the stack e.g. `5x01` |
| ListItem.Property(stacked_last) | Last episode number in the stack e.g. `5x03` |
| ListItem.Property(stacked_first_episode) | First episode number in the stack without formatting e.g. `1` |
| ListItem.Property(stacked_last_episode) | Last episode number in the stack without formatting e.g. `3` |
| ListItem.Property(stacked_first_season) | First season number in the stack without formatting e.g. `5` |
| ListItem.Property(stacked_last_season) | Last season number in the stack without formatting e.g. `5` |


## ListItem.Property(widget)

This property contains a formatted label based upon the settings of the particular list. It is useful if you want to show a "heading" label for the list.

| Plugin Path Params | Output in Property(widget) |
| :--- | :--- |
| `&amp;days=1&amp;startdate=-1` | "Yesterday" |
| `&amp;days=1&amp;startdate=0` | "Today" |
| `&amp;days=1&amp;startdate=1` | "Tomorrow" |
| `&amp;days=1&amp;startdate=[<-1 OR >1]` | "Monday" "Tuesday" etc. |
| `&amp;days=7&amp;startdate=0` | "This Week" |
| `&amp;days=7&amp;startdate=-7` | "Last Week" |
| `&amp;days=14&amp;startdate=0` | "This Fortnight" |
| `&amp;days=14&amp;startdate=-14` | "Last Fortnight" |
| `&amp;days=30&amp;startdate=0` | "This Month" |
| `&amp;days=30&amp;startdate=-30` | "Last Month" |