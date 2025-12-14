## Discover

| Example | `plugin://plugin.video.themoviedb.helper?info=discover&amp;tmdb_type=movie&amp;with_cast=$INFO[ListItem.Label]` |
| :--- | :--- |

| Additional Supported Parameters | [Filter](https://github.com/jurialmunkey/plugin.video.themoviedb.helper/wiki/Lists-Additional-Params#optional-exclusion-and-filter-parameters) | [Widget](https://github.com/jurialmunkey/plugin.video.themoviedb.helper/wiki/Lists-Additional-Params#additional-widget-parameters) |
| :--- | :--- | :--- |

## Available Parameters
Discover allows for complex searches using the following parameters

| Param | Description |
| :--- | :--- |
| `&amp;tmdb_type=` | Type of item. Required! Must be `movie` or `tv` |
| `&amp;with_cast=` | Includes items that have one of the specified people as a cast member |
| `&amp;with_crew=` | Includes items that have one of the specified people as a crew member |
| `&amp;with_people=` | Includes items that have one of the specified people as a cast or crew member |
| `&amp;with_companies=` | Includes items from a matching movie studio  |
| `&amp;with_genres=` | Includes items with a matching genre |
| `&amp;without_genres=` | Excludes items with a matching genre |
| `&amp;with_id=True` | By default discover will translate names into TMDb IDs for you. However, if the TMDb ID is already available, you can pass IDs instead by setting the with_id param to True |
| `&amp;with_separator=OR`  | By default, if multiple values separated by a slash " / " are passed as params, discover will only return items matching ALL those values. To instead return items matching ANY of those values, change with_separator to OR. NOTE: The slash separator has spaces either side. |
| `&amp;with_separator=AND`  | Default behaviour |
| `&amp;with_separator=NONE`  | Only match with the first value in list of separated values |
