## Trakt Management Functions

TMDbHelper provides a menu to add/remove items from Trakt history, collection and lists. It can be activate via script command:

```
RunScript(plugin.video.themoviedb.helper,sync_trakt,type=movie,tmdb_id=ID)
RunScript(plugin.video.themoviedb.helper,sync_trakt,type=tv,tmdb_id=ID)
RunScript(plugin.video.themoviedb.helper,sync_trakt,type=tv,tmdb_id=ID,season=SEASON,episode=EPISODE)
```
Replace ID|SEASON|EPISODE with the appropriate $INFO[]  
Note that ID for episodes should be the TVSHOW's ID (not the episode's).

If you do not have TMDb IDs for the items, you can do a lookup using a combination of query|imdb_id|tvdb_id|year instead


```
RunScript(plugin.video.themoviedb.helper,sync_trakt,type=movie,imdb_id=$INFO[ListItem.IMDbNumber],query=$INFO[ListItem.Title],year=$INFO[ListsItem.Year])
RunScript(plugin.video.themoviedb.helper,sync_trakt,type=tv,query=$INFO[ListItem.Title],tvdb_id=$INFO[ListItem.Property(tvdb_id)],year=$INFO[ListItem.Year])
RunScript(plugin.video.themoviedb.helper,sync_trakt,type=tv,query=$INFO[ListItem.TVShowTitle],tvdb_id=$INFO[ListItem.Property(tvshow.tvdb_id)],year=$INFO[ListItem.Year],season=$INFO[ListItem.Season],episode=$INFO[ListItem.Episode])
```