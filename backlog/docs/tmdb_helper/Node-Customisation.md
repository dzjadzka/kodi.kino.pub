## Custom User Nodes  
As of v5.1.21 TMDbHelper allows users to create custom TMDbHelper folder and shortcut nodes.

Nodes are text files using JSON formatting. Save your node in:   
`.kodi/userdata/addon_data/plugin.video.themoviedb.helper/nodes/FILENAME.json`

Nodes added to the above folder will appear under `TMDbHelper > Nodes`

## Example Node

```json
{
    "name": "Genre Randomiser",
    "icon": "special://home/addons/plugin.video.themoviedb.helper/resources/icons/themoviedb/genre.png",
    "list": [
        {
            "name": "Random Movie Genre",
            "icon": "special://home/addons/plugin.video.themoviedb.helper/resources/icons/themoviedb/genre.png",
            "path": "plugin://plugin.video.themoviedb.helper/?info=random_genres&tmdb_type=movie"
        },
        {
            "name": "Random TV Genre",
            "icon": "special://home/addons/plugin.video.themoviedb.helper/resources/icons/themoviedb/genre.png",
            "path": "plugin://plugin.video.themoviedb.helper/?info=random_genres&tmdb_type=tv"
        }
    ]
}
```

This node will create a "Genre Randomiser" folder under "Nodes". The "Genre Randomiser" folder will contain two shortcuts: "Random Movie Genre" and "Random TV Genre".


## Skin Support

Skinners can include their own custom nodes in their skins to use as plugin:// paths in containers. Save the node somewhere in your extras folder and access like so (replace FILENAME and FOLDER with the filename and folder of JSON file).

```
plugin://plugin.video.themoviedb.helper/?info=dir_custom_node&amp;filename=FILENAME.json&amp;basedir=special://skin/extras/FOLDER
```