## Lookup Queries
TMDb Helper provides a number of lists that are based upon another item. See lookup parameters link for alternative methods of retrieving TMDb ID when it is not available.

| Additional Supported Parameters | [Lookup](https://github.com/jurialmunkey/plugin.video.themoviedb.helper/wiki/Lists-Additional-Params#lookup-parameters) | [Filter](https://github.com/jurialmunkey/plugin.video.themoviedb.helper/wiki/Lists-Additional-Params#optional-exclusion-and-filter-parameters) | [Widget](https://github.com/jurialmunkey/plugin.video.themoviedb.helper/wiki/Lists-Additional-Params#additional-widget-parameters) |
| :--- | :--- | :--- | :--- |




## Recommend 
```
plugin://plugin.video.themoviedb.helper?info=recommendations&amp;tmdb_type=movie&amp;tmdb_id=348
```

| Param | Options |
| :--- | :--- |
| `tmdb_type=` | `movie` `tv` |

## Similar 
```
plugin://plugin.video.themoviedb.helper?info=similar&amp;tmdb_type=movie&amp;tmdb_id=348
```

| Param | Options |
| :--- | :--- |
| `tmdb_type=` | `movie` `tv` |



## Cast 
```
plugin://plugin.video.themoviedb.helper?info=cast&amp;tmdb_type=movie&amp;tmdb_id=348`
```

| Param | Options |
| :--- | :--- |
| `tmdb_type=` | `movie` `tv` |
| `aggregate=` | Optional. By default cast will return main cast of current season. Use `aggregate=true` param to retrieve the full aggregated cast from all seasons and episodes. |

## Crew 
```
plugin://plugin.video.themoviedb.helper?info=crew&amp;tmdb_type=movie&amp;tmdb_id=348
```


| Param | Options |
| :--- | :--- |
| `tmdb_type=` | `movie` `tv` |
| `aggregate=` | Optional. By default cast will return main crew of current season. Use `aggregate=true` param to retrieve the full aggregated crew from all seasons and episodes. |

## Keywords 
```
plugin://plugin.video.themoviedb.helper?info=movie_keywords&amp;tmdb_type=movie&amp;tmdb_id=348
```

| Param | Options |
| :--- | :--- |
| `tmdb_type=` | `movie` |

## Reviews 
```
plugin://plugin.video.themoviedb.helper?info=reviews&amp;tmdb_type=movie&amp;tmdb_id=348
```

| Param | Options |
| :--- | :--- |
| `tmdb_type=` | `movie` `tv` |

## Posters 
```
plugin://plugin.video.themoviedb.helper?info=posters&amp;tmdb_type=movie&amp;tmdb_id=348
```

| Param | Options |
| :--- | :--- |
| `tmdb_type=` | `movie` `tv` |

## Fanart 
```
plugin://plugin.video.themoviedb.helper?info=fanart&amp;tmdb_type=movie&amp;tmdb_id=348
```

| Param | Options |
| :--- | :--- |
| `tmdb_type=` | `movie` `tv` |

## Videos 
```
plugin://plugin.video.themoviedb.helper?info=videos&amp;tmdb_type=movie&amp;tmdb_id=348
```

| Param | Options |
| :--- | :--- |
| `tmdb_type=` | `movie` `tv` |

## Seasons 
```
plugin://plugin.video.themoviedb.helper?info=seasons&amp;tmdb_type=tv&amp;tmdb_id=48891
```

| Param | Options |
| :--- | :--- |
| `tmdb_type=` | `tv` |

## Episodes in Season 
```
plugin://plugin.video.themoviedb.helper?info=episodes&amp;tmdb_type=tv&amp;tmdb_id=48891&amp;season=2
```

| Param | Options |
| :--- | :--- |
| `tmdb_type=` | `tv` |

## All Episodes for TV Show (Flattened Seasons)
```
plugin://plugin.video.themoviedb.helper?info=flatseasons&amp;tmdb_type=tv&amp;tmdb_id=48891
```

| Param | Options |
| :--- | :--- |
| `tmdb_type=` | `tv` |


## Episode Cast 
```
plugin://plugin.video.themoviedb.helper?info=cast&amp;tmdb_type=tv&amp;tmdb_id=48891&amp;season=2&amp;episode=1
```

| Param | Options |
| :--- | :--- |
| `tmdb_type=` | `tv` |

## Episode Thumbs 
```
plugin://plugin.video.themoviedb.helper?info=episode_thumbs&amp;tmdb_type=tv&amp;tmdb_id=48891&amp;season=2&amp;episode=1
```

| Param | Options |
| :--- | :--- |
| `tmdb_type=` | `tv` |

## Movies as Cast 
```
plugin://plugin.video.themoviedb.helper?info=stars_in_movies&amp;type=person&amp;tmdb_id=1100
```

| Param | Options |
| :--- | :--- |
| `tmdb_type=` | `person` |


## TV as Cast 
```
plugin://plugin.video.themoviedb.helper?info=stars_in_tvshows&amp;type=person&amp;tmdb_id=1100
```


| Param | Options |
| :--- | :--- |
| `tmdb_type=` | `person` |

## Movies as Crew 
```
plugin://plugin.video.themoviedb.helper?info=crew_in_movies&amp;type=person&amp;tmdb_id=1100
```


| Param | Options |
| :--- | :--- |
| `tmdb_type=` | `person` |


## TV as Crew 
```
plugin://plugin.video.themoviedb.helper?info=crew_in_tvshows&amp;type=person&amp;tmdb_id=1100
```


| Param | Options |
| :--- | :--- |
| `tmdb_type=` | `person` |


## Person images 
```
plugin://plugin.video.themoviedb.helper?info=images&amp;type=person&amp;tmdb_id=1100
```


| Param | Options |
| :--- | :--- |
| `tmdb_type=` | `person` |


## Collection (aka Set) 
```
plugin://plugin.video.themoviedb.helper?info=collection&amp;type=collection&amp;tmdb_id=10
```

| Param | Options |
| :--- | :--- |
| `tmdb_type=` | `collection` |


## Recommended next item to watch. 
```
plugin://plugin.video.themoviedb.helper?info=next_recommendation&amp;type=tv&amp;tmdb_id=48891&amp;season=2&amp;episode=4
```


| Param | Options |
| :--- | :--- |
| `tmdb_type=` | `movie` `tv` |


Displays next episode for tvshow or next movie for collection. If there is no next item it displays the first item from info=recommendations.


## Search
```
plugin://plugin.video.themoviedb.helper?info=search&amp;type=movie&amp;query=Alien
```

| Param | Options |
| :--- | :--- |
| `query=` | The text you want to search for |
| `tmdb_type=` | `movie` `tv` `person` `both` `collection` `company` `keyword` |
| `year=` | Optional. Year movie or tvshow premiered in current region. |
| `first_air_date_year=` | Optional. Year tvshow first aired. |
| `primary_release_year=` | Optional. Year movie premiered in main market. |