## Understanding Players

TMDbHelper has a player function which allows you to select from a variety of "players" to play an item using a number of video on demand streaming plugins. The player json file is a set of rules which defines how TMDbHelper should interact with the end streaming plugin to find the correct item to play.

Below we will break down the components of the [Netflix Player](https://github.com/jurialmunkey/plugin.video.themoviedb.helper/blob/matrix/resources/players/netflix.json) file as an example.

**Player Name and Plugin ID**
```json
"name": "Netflix",
"plugin": "plugin.video.netflix",
```

Simple enough. These two lines define the name of the player and the plugin ID of the end plugin that will be used. The name displays when selecting a play method to indicate which player is being used e.g. "Play with Netflix", "Search with Netflix".


**Player Priority and Provider Link**
```json
"priority": 100,
"provider": "Netflix",
```

The priority determines the "rank" of the player in the selection dialog. Small numbers have high priority and will appear closer to the top of the dialog. The provider links the player to a streaming service and automatically gives it a higher priority if the item is provided by that streaming service.

**Playback Method**
```json
 "is_resolvable": "true",
```

The is_resolvable flag tells TMDbHelper that the Netflix plugin does not use player hacks and that it can play files using the proper setResolvedURL method that Kodi expects plugins to use. This flag should be set to false if the end plugin uses xbmc.Player() hacks (usually banned add-ons do this).

**Assert Keys**
```json
"assert": {
    "play_movie":       ["title", "year"],
    "play_episode":     ["showname", "season", "episode"],
    "search_movie":     ["title"],
    "search_episode":   ["showname"]
},
```

The assert key tells TMDbHelper what values it must have in order to play the item using the plugin. In this case, to play a movie using this plugin a title and year is needed. If TMDbHelper does not have a year for the movie it will not display this player as a choice.

**Play Movie Steps**
```json
"play_movie": [
    "plugin://plugin.video.netflix/directory/search/search/add/",
    {"keyboard": "Select"},
    {"keyboard": "{title}"},
    {"title": "(?i).*{title}.*", "year": "{year}"}
],
```

This block defines what actions TMDbHelper must take to play using the "Play Movie with Netflix" function. 
1. It opens the search directory plugin url `plugin://plugin.video.netflix/directory/search/search/add/`. 
2. Then it stimulates pressing "Select" on the keyboard because the Netflix plugin displays a confirmation dialog that must be dismissed before the search input dialog displays.
3. Then it inputs the title of the movie into the pop-up keyboard and presses enter.
4. Finally, it then looks through the search results for an item that matches the title/year and if it finds one it plays it. The additional `(?i).*` is a regex matching pattern. The `(?i)` is to ignore case so that capital letters don't matter. The `.*` is a wildcard so that if there is some additional text at the start/end of the title it will still match -- e.g. if we're looking for the movie "Alien" but on Netflix it is "[Classic Sci-Fi Movies] Alien" it will still match.


**Play Episode Steps**
```json
"play_episode"      : [
    "plugin://plugin.video.netflix/directory/search/search/add/",
    {"keyboard": "Select"},
    {"keyboard": "{showname}"},
    {"title": "(?i)^(\\[.*\\])?{showname}(\\[.*\\])?$"},
    {"return": "true", "season": "{season}", "episode": "{episode}"},
    {"season": "{season}"},
    {"season": "{season}", "episode": "{episode}"}
],
```

Similar to the Play Movie steps, this block defines the steps to play episodes.

1. As above, it calls the search path
2. As above, it then presses "Select" to dismiss a confirmation dialog
3. As above, it inputs the search term into the keyboard except this time it puts in the showname
4. As above, it looks to match an item based on the title. However, this time it tries to match using the showname. It has some additional regex to filter out [COLOR=blue] type tags that the Netflix plugin sometimes adds to the title. If it finds a match it opens the tvshow.
5. The `return` flag is an early exit step. This step looks for an item where the season and episode numbers match. This is because tvshows with one season are flattened on the Netflix plugin. If it finds a match it plays the episode, otherwise it tries the next step instead.
6. The season step looks for a season match and opens the season if it finds it.
7. The final step then looks through the episodes in the season folder for an item where the season and episode numbers match. If a match is found it plays the episode.


## Player Files
Put user created player files in `userdata/addon_data/plugin.video.themoviedb.helper/players/`

| Key | Description |
| :--- | :--- |
| name | label in the pop-up select dialog |
| plugin | plugin ID which is used to check if addon is installed.  |
| priority | integer determining position of player in dialog, the lower the number the closer to the top |
| provider | for matching with justwatch providers to override priority based on justwatch provider index for item - see [player provider names list](https://github.com/jurialmunkey/plugin.video.themoviedb.helper/blob/matrix/resources/player_provider_names.txt) for possible options |
| play_movie | list of steps taken to get the plugin url to play the movie |
| play_episode | list of steps taken to get the plugin url to play the episode |
| search_movie | list of steps taken to get the plugin url to open a search folder for the movie |
| search_episode | list of steps taken to get the plugin url to open a search folder for the episode |
| assert | only show player if these item keys are available |
| fallback | specify a fallback if player fails or is unavailable |
| make_playlist | set to 'true' to have TMDbHelper generate a playlist of episodes when playing an episode. TMDbHelper will queue all episodes following the one played - e.g. if you play S2E3 it will queue S2E4 onwards. The default player for the playlist will be set to the same player so that the user doesn't need to reselect the player when skipping to next item. NOTE: Only works with plugins that work with is_resolvable flag below. |
| is_resolvable | set to 'true' if the player plugin uses the correct `setResolvedUrl()` method for playback. This option should be set to 'false' for any player plugin where items are passed to Player() instead e.g. many plugins that scrape multiple sources often use Player() hacks and will need to be set to 'false' to avoid unexpected behaviour. |

Use play_movie/episode if the end url will directly play the item (will display as "Play with NAME").
Use search_movie/episode if the end url will open a search folder of items (will display as "Search NAME").

## Available Keys
Curly brace {keys} are used to format the url with the appropriate info. The {key} is replaced by the info about the item as specified in the below table. Where there are two info values in the table below, the first is used for movies and the second for tvshows.

For plugin:// URLs you will need to make sure that you are using the correct encoding that the plugin expects. See the [Special Suffixes](https://github.com/jurialmunkey/plugin.video.themoviedb.helper/wiki/Player-Function#special-suffixes) section for more details.

| Key | Info |
| :--- | :--- |
| {id} | `tmdb id` `tvdb id` |
| {tmdb} | `tmdb id` |
| {imdb} | `imdb id` |
| {tvdb} | `tvdb id` |
| {trakt} | `trakt number id` |
| {slug} | `trakt slug id` |
| {name} | `movie title (year)` `tvshow title S01E01` |
| {year} | `year` |
| {season} | `season number` |
| {episode} | `episode number` |
| {premiered} | `premiered date in YYYY-MM-DD format` |
| {released} | `release date in YYYY-MM-DD format` |
| {showname} | `tvshow title` |
| {showyear} | `tvshow year of pilot episode` |
| {showpremiered} | `tvshow premiered date of pilot episode` |
| {clearname} | `movie title` `tvshow title` |
| {thumbnail} | `thumb image` |
| {poster} | `poster image` |
| {fanart} | `fanart image` |
| {title} | `movie title` `episode title` |
| {originaltitle} | `movie title in original language` `show name in original language` |
| {epid} | `tvdb episode id` |
| {epimdb} | `imdb episode id` |
| {eptmdb} | `tmdb episode id` |
| {eptrakt} | `trakt episode id` |
| {now} | `current timestamp` |



## Special Suffixes for Plugin:// URI
Many plugins expect the plugin:// URI to have a specific encoding. You can apply different encoding types by appending an encoding suffix to the key name as listed in the table below. Most plugins will expect `KEY_url` in plugin:// path.

| Key | Description |
| :--- | :--- |
| {KEY_+} | replaces spaces with `+` |
| {KEY_-} | replaces spaces with `-` |
| {KEY_url} | url percent encode keys - spaces as `%20` |
| {KEY_url+} | url percent encode keys - spaces as `%2B` i.e. `+` |
| {KEY_escaped} | double url percent encode keys - spaces as `%2520` |
| {KEY_escaped+} | double url percent encode keys - spaces as `%252B` i.e. `+` |

The following keys can have encoding applied: `{name}` `{showname}` `{clearname}` `{tvshowtitle}` `{title}` `{thumbnail}` `{poster}` `{fanart}` `{originaltitle}` `{plot}` `{cast}` `{actors}`

For instance `{plot}` can be substituted for `{plot_+}` `{plot_-}` `{plot_url}` `{plot_url+}` `{plot_escaped}` or `{plot_escape+}`


## API Language and Country
By default, TMDbHelper will grab information in the language specified in TMDbHelper settings. However, some plugins might require information from a specific region and language.

As of v6.10.4 the translation method works for all languages including English. The old api_language override method is depreciated.

### Title Key Translation (Faster)
You can get the player to lookup foreign language translations for the Movie/TvShow/Episode title. Unlike the above forced override, this method instead adds the translated title as a separate key.

You can specify the translation lookup using the "language" option to specify the two letter iso language code:
```json
{
    "name"              : "YouTube",
    "language"          : "de",
    "plugin"            : "plugin.video.youtube",
```

For this player TMDbHelper will add a translation lookup to retrieve the German translation of the title and plot in _addition_ to the language and country specified in the settings. The translated values are placed into the corresponding keys with the language code at the front - e.g. `{de_title}` `{de_plot}`. 



This option has the added advantage of allowing you to mix the translated title with your default language, something which can be particularly useful for regex matching using an OR operator (e.g. you could check `"{title}|{de_title}"`)

Translations are retrieved for the following keys: 
`title` `showname` `clearname` `tvshowtitle` `name` `plot`

URL encoded versions of the keys are also generated and accepted in the player file - e.g. 
`{de_title_-}` `{de_title_escaped}` `{de_title_meta_url+}` etc.

If no translation is available for that particular key, the value falls back to the default value e.g. `{de_title}` will return `{originaltitle}` if there is no German translation available for the title.

~NOTE: Because the default language of the TMDb API is English, English translations are not provided in the get translations API call. If your TMDbH language is set to a language other than English and you have a player which requires English titles, you will need to use the slower api_language override option above instead.~

NOTE: As of v6.10.4, English tags such as `en_title` now work correctly. API language override is no longer required and is depreciated.


### Force API Language and Country Override (Slower) 

NOTE: As of v6.10.4, this method is depreciated. Translation keys work for all languages now. Use the translation method above.
```
"api_language"      : "en-US"
```
~You can use this method to force the player to look up ALL the item details again using the specified language and country code. The original values will be overwritten with the new values.~

~If your player only requires the movie/tvshow/episode title to be translated to a language other than English, you should use the faster title key translation method listed below instead.~


## Assert Keys
Occasionally some IDs might not be available for some items. To prevent a player from displaying if it requires a specific key, you can assert the key values for the player.

For instance, to only display the play_movie player if IMDb ID and Year are available:
```
"assert": {"play_movie": ["imdb", "year"]}
```

You may also wish to show a different player if some info is not available. To do so add `!` to the key name. For instance, to also only show the `search_movie` player if IMDB ID is *not* available:

```
"assert": {"play_movie": ["imdb", "year"],
           "search_movie": ["!imdb"]}
```



## Fallback Player
You can specify a fallback player if the player fails to retrieve a url to open (or if the default player is not available due to an empty asserted key value).

For instance, to have the Netflix play_movie player fallback to Youtube search_movie player, add to the Netflix player file:
```
"fallback": {"play_movie": "youtube.json search_movie"}
```

NOTE: Fallback is only used if TMDbHelper fails to retrieve a URL from the plugin being called. It does NOT check if the plugin being called was able to successfully play a file if that URL first runs a script. For instance, suppose a plugin that needs to scrape sources before playing. Because TMDbHelper received a URL and was able to run it successfully then it will NOT use the fallback even if ultimately no playable sources were found in the plugin.


## Additional Steps
Some plugins do not expose a playable plugin path directly. Instead it is necessary to "step" through the plugin to reach a playable path. Steps are defined by placing actions within a list using square brackets `[]`. Actions are separated by a comma. Actions are defined by curly brace key/value dictionary pairs. See the Netflix example used above for more details.

| Action | Description |
| :--- | :--- |
| "title": "{key}" | Match ListItem.Title to {key} |
| "year": "{key}" | Match ListItem.Year to {key} |
| "originaltitle": "{key}" | Match ListItem.OriginalTitle to {key} |
| "imdbnumber": "{key}" | Match ListItem.IMDbNumber to {key} |
| "premiered": "{key}" | Match ListItem.Premiered to {key} |
| "firstaired": "{key}" | Match first aired date to {key} |
| "season": "{key}" | Match ListItem.Season to {key} |
| "episode": "{key}" | Match ListItem.Episode to {key} |
| "label": "{key}" | Match ListItem.Label to {key} |
| "file": "{key}" | Match ListItem.FileNameAndPath to {key} |
| "showtitle": "{key}" | Match ListItem.TvShowTitle to {key} |

| Special Action | Description |
| :--- | :--- |
| "position": "{key}" | Matches based upon index position of item list. Value in {key} is index position to use. Useful to match season or episode in plugins that don't give season or episode numbers to match. |
| "dialog": "True" | Open a dialog to select item. Useful for plugins that open into a folder of selectable sources. Also useful for plugins where matching in one of the steps is difficult and user input is preferred to select item. Optionally can use "Auto" instead of "True" for automatic selection of single items when only one result returned. |
| "strict": "True" | Force the step to check that only one item matches the step rules. The step fails if multiple items match. Optionally can combine with a dialog action to pop-up a dialog to select from the matching items. For instance `{"dialog": "auto", "strict": "true", "label": "{title}"}` will auto play if only one item with title is found otherwise it provides a dialog to select from items with matching titles. |
| "keyboard": "{key}" | Input {key} into a pop-up keyboard dialog. Useful for plugins that only allow searching via keyboard input and don't expose a search end point that allows passing the query directly to the plugin url.  |
| "direction": "rtl" | Use in tandem with keyboard input step to mirror text for rtl language keys, e.g. `{"keyboard": "{he_key}", "direction": "rtl"}` |
| "return": "true" | Specifies an early return step where if a match is found the player will exit and play the file. However, if a match is NOT found then the player continues onto the next step as if the return step did not occur. Useful for addons where single season shows and miniseries skip the seasons step and open directly into episodes. For instance see the [Netflix player](https://github.com/jurialmunkey/plugin.video.themoviedb.helper/blob/ebb265e2a2bbdcae39907a9215655bd2dd8e6b4e/resources/players/netflix.json#L18-L25) where the `{"return": "true", "season": "{season}", "episode": "{episode}"}` will allow for checking for a matching episode before continuing onto a standard `{"season": "{season}"}` step |


## Regex Matching in Actions
Info keys in actions will also now accept regular expressions (regex) to perform matching. Matching is done using the python module re.match which matches from the start of the string by default (you can use `.*` wild card at the start if you need match within the string).

See the YouTube player for an example of regex matching
```
{
    "name"              : "YouTube",
    "plugin"            : "plugin.video.youtube",
    "play_movie"        : [
                            "plugin://plugin.video.youtube/search/?q={name}&search_type=notvalid",
                            {"title": "(?i){title}"}
                          ],
    "play_episode"      : [
                            "plugin://plugin.video.youtube/search/?q={name}&search_type=notvalid",
                            {"title": "(?i).*{showname}.*S.*{season}E.*{episode}|(?i).*S.*{season}E.*{episode}.*{showname}|(?i).*{showname}.*{title}"}
                          ],
    "search_movie"      : "plugin://plugin.video.youtube/search/?q={name}&search_type=notvalid",
    "search_episode"    : "plugin://plugin.video.youtube/search/?q={name}&search_type=notvalid"
```

In the YouTube player, the play_movie actions search youtube for `{name}` and then look for any item with ListItem.Title that begins with the `{title}` key. The `(?i)` regex tells the re.match module to ignore case so that, for example, `YoUTuBe tiTLe NaME` will match `YouTube Title`.

In the play_episode actions, the pipe `|` means OR. So for S01E01 of a show the regex will match any of the combinations:
```
ShowName - S01E01
...SHOWName S1E1
S1E1 - -- ShownaME (best evA scene!!!1111!)
--Showname --- Episode titLE
```

See here for an easy starter regex guide:
https://dl.icewarp.com/online_help/203030104.htm


## Calling Players via RunScript
| Type | Path |
| :--- | :--- |
| Movie | `Runscript(plugin.video.themoviedb.helper,play=movie,tmdb_id=$INFO[ListItem.UniqueID(tmdb)]),imdb_id=$INFO[ListItem.UniqueID(imdb)])` |
| Episode | `Runscript(plugin.video.themoviedb.helper,play=tv,query=$INFO[ListItem.TVShowTitle],ep_year=$INFO[ListItem.Year],season=$INFO[ListItem.Season],episode=$INFO[ListItem.Episode])` |

Optional params to help identify the item to play
`query=`, `year=`, `ep_year=`, `imdb_id=`, `tmdb_id=`, `tvdb_id=`

By default the play function will attempt to play using the default player settings. You can override the default player and force the player dialog by adding `ignore_default=true` param.

Alternatively, you can play using a specific player with `play_using=` instead of play:
| Type | Path |
| :--- | :--- |
| Movie | `Runscript(plugin.video.themoviedb.helper,play_using=youtube.json,tmdb_type=movie,tmdb_id=$INFO[ListItem.UniqueID(tmdb)]),imdb_id=$INFO[ListItem.UniqueID(imdb)])` |
| Episode | `Runscript(plugin.video.themoviedb.helper,play_using=youtube.json,tmdb_type=tv,query=$INFO[ListItem.TVShowTitle],ep_year=$INFO[ListItem.Year],season=$INFO[ListItem.Season],episode=$INFO[ListItem.Episode])` |

The `play_using` function will use the `play_episode|movie` method of the player. You can use the `search_episode|movie` methods by adding `mode=search` param.

## Executing a Kodi built-in function
As of v5.1.19+ it is possible for players to execute [Kodi built-in functions](https://kodi.wiki/view/List_of_built-in_functions) by using the path prefix `executebuiltin://` 

This ability might be useful if you wish to run a script or other Kodi command using information about the movie/episode.

Example player file which runs the `Notification()` built-in to show the title and year of the item in a notification dialog:

```json
{
    "name"          : "Notification",
    "plugin"        : "xbmc.core",
    "icon"          : "{}/resources/icons/other/kodi.png",
    "priority"      : 10000,
    "is_resolvable" : "false",
    "play_movie"    : "executebuiltin://Notification({title},{year})"
}
```
