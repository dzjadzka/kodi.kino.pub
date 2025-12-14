## Script Methods

TMDbHelper provides a number of functions via RunScript() commands

```
RunScript(plugin.video.themoviedb.helper,{command})
```

| Command | Additional Params | Description |
| :--- | :--- | :--- |
| authenticate_trakt | | (Re)Authenticate Trakt account via auth code |
| revoke_trakt | |  Logs the user out of their Trakt account |
| recache_kodidb | | Refreshes the Kodi DB in memory |
| split_value={value} | separator={separator} property={name} | Splits a value into separate properties. Specify separator= to change the default separator from ' / '. Outputs to $INFO[Window(Home).Property(TMDbHelper.Split.0)] where 0 is the index of the item. Specify property= to change 'TMDbHelper.Split' to another name |
| kodi_setting={setting} | property={name} | Outputs value of the Kodi setting to $INFO[Window(Home).Property(TMDbHelper.KodiSetting)] or property= if specified |

TBC



