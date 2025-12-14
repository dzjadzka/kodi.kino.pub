## Optional Exclusion and Filter Parameters

Several lists support filtering and excluding items based upon item properties.

| Param | Description |
| :--- | :--- |
| `filter_key=KEY&amp;filter_value=VALUE` | Only include items where the specified key matches the specified value. |
| `exclude_key=KEY&amp;exclude_value=VALUE` | Exclude all items that have the specified key that matches the specified value. |

#### Advanced Usage Examples

| Examples | Description |
| :--- | :--- |
| `filter_key=genre&amp;filter_value=Action / Adventure` | Checking for multiple values is possible by using a `/`. For instance, this filter will include items that have Action or Adventure as a genre |
| `exclude_key=providers&amp;exclude_value=is_empty` | The `is_empty` value can be used to check for empty keys. For instance, this exclusion will exclude items that without a provider. |
| `exclude_key=year&amp;exclude_value=2000&amp;exclude_operator=lt` | By default the standard comparison uses the IN operator to check if the specified VALUE is IN the KEY. The operator can be changed to any [standard python operator](https://docs.python.org/3/library/operator.html). For instance, this exclusion will exclude items where the year is LESS THAN (lt) 2000.  |
| `filter_key=premiered&amp;filter_value=$DAYS[-120]&amp;filter_operator=lt` | As of 5.1.37 the `$DAYS[X]` can be used to generate a date X days from today - e.g. `$DAYS[-120]` will generate the date which was 120 days ago. The example filter here will only include items which premiered at least 120 days ago.  |


## Lookup Parameters 

| Params | Required | Possible Values | Details |
| :--- | :--- | :--- | :--- |
| `tmdb_type=` | Required | `movie` `tv` `person` | Type of item | 
| `imdb_id=` | Optional | `ListItem.IMDbNumber` `ListItem.Property(imdb_id)` | IMDb ID of item |
| `tmdb_id=` | Optional | `ListItem.Property(tmdb_id)` | TMDb ID of item |
| `query=` | Optional | `ListItem.Title` `ListItem.TvShowTitle` | Title of item |
| `year=` | Optional | `ListItem.Year` |  Used in conjunction with query= to match item to exact year |
| `episode_year=` | Optional | `ListItem.Year` |  Used in conjunction with query= to match fuzzily to year because the episode year doesn't match tvshow year. Will find the most recent show in the search with a first aired date on or before the year specified |


## Additional Widget Parameters
| Param | Description |
| :--- | :--- |
| `nextpage=true` | Displays the "Next Page" item at the end of lists with a next page. Set to `false` to override any user settings and force the nextpage item to be hidden. |
| `fanarttv=true` | ~Gets additional artwork from FanartTV. Used if you required additional artwork for a widget in video info dialog. Set to `false` to override user's settings and prevent unneeded additional artwork lookups~ Depreciated. This param no longer has any effect. |
| `cacheonly=true` | Skips detailed item lookups for items and only applies previously cached details. Only the basic details retrieved from lists will be used (note that Trakt and MDbList lists require cacheonly=false). As of v6.7.0+ use `cacheonly=false` to force extra details to be looked up as user level setting has been removed. Further control for skinners is provided via `Skin.SetBool(TMDbHelper.DisableDefaultCacheOnly)` to flip the default value for basic lists to be `cacheonly=false` if no value is specified (v6.7.5+)  |
| `widget=true` | This param is automatically appended if the widget was added via skinshortcuts dialog in skin settings. Applies any "widget" based TMDbHelper user settings |
| `detailed=true` | For performance purposes, default indexed properties (e.g. Cast.X.Name) are not set on lists even if details are available. If you are using a widget which requires these properties set the detailed param to true (v4.10.30+) |
