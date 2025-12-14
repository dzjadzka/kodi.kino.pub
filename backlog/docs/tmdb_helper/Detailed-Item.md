## Detailed Item  
| Example Command | `plugin://plugin.video.themoviedb.helper/?info=details&amp;tmdb_type=movie&amp;query=$INFO[ListItem.Title]` |
| :--- | :--- |

Supports: [Lookup Parameters](https://github.com/jurialmunkey/plugin.video.themoviedb.helper/wiki/Lists-Additional-Params#lookup-parameters)


### General

| InfoLabel | Description |
| :--- | :--- |
| ListItem.Label | Label |
| ListItem.Icon | Icon |
| ListItem.Thumb | Thumb | 
| ListItem.Title | Title |
| ListItem.OriginalTitle | Original Language Title |
| ListItem.Plot | Plot |
| ListItem.Rating | TMDb Average Rating |
| ListItem.Votes | TMDb Number of Votes |
| ListItem.Premiered | Premiered |
| ListItem.Year | Year |
| ListItem.IMDbNumber | IMDb Number |
| ListItem.Status | Status Airing Cancelled etc. |
| ListItem.Genre | List of Genres |
| ListItem.Duration | Duration |
| ListItem.Studio | List of Studios |
| ListItem.Country | List of Countries |
| ListItem.MPAA | Certification |
| ListItem.Trailer | Youtube Trailer |
| ListItem.Cast | List of Cast Members |
| ListItem.Director | List of Directors |
| ListItem.Writer | List of Writers |
| ListItem.PlayCount | Playcount (Trakt) |
| ListItem.Overlay | Watched Indicator (Trakt) |
| ListItem.LastPlayed | Last Played Date (Trakt) |
| ListItem.Property(Param.Info) | The value of the `info=` param key in Container.FolderPath. Works with other params. Replace `Info` with desired param |
| ListItem.Property(TMDb_ID) | TMDb ID |
| ListItem.Property(IMDb_ID) | IMDb ID |
| ListItem.Property(TVDb_ID) | TVDb ID |
| ListItem.Property(Genre.X.Name) | Name of Genre at X position |
| ListItem.Property(Genre.X.TMDb_ID) | TMDb_ID of Genre at X position |
| ListItem.Property(Studio.X.Name) | Name of Studio at X position. Note for TV Shows `ListItem.Studio` combines Release Network + Production Studios. `Studio.X` properties only list Production Studios. Use `Network.X` properties to retrieve TV Networks |
| ListItem.Property(Studio.X.Icon) | Icon of Studio at X position |
| ListItem.Property(Studio.X.TMDb_ID) | TMDb_ID of Studio at X position |
| ListItem.Property(Country.X.Name) | Name of Country at X position |
| ListItem.Property(Country.X.TMDb_ID) | TMDb_ID of Country at X position |
| ListItem.Property(Language.X.Name) | Name of Language at X position |
| ListItem.Property(Language.X.ISO) | ISO of Language at X position |
| ListItem.Property(Cast.X.Name) | Name of Cast at X position |
| ListItem.Property(Cast.X.Role) | Role of Cast at X position |
| ListItem.Property(Cast.X.Character) | Character of Cast at X position |
| ListItem.Property(Cast.X.Thumb) | Thumb of Cast at X position |
| ListItem.Property(Crew.X.Name) | Name of Crew at X position |
| ListItem.Property(Crew.X.Role) | Role of Crew at X position |
| ListItem.Property(Crew.X.Job) | Job of Crew at X position |
| ListItem.Property(Crew.X.Department) | Department of Crew at X position |
| ListItem.Property(Crew.X.Thumb) | Thumb of Crew at X position |
| ListItem.Property(Screenplay.X.Name) | Name of Screenplay at X position |
| ListItem.Property(Screenplay.X.Role) | Role of Screenplay at X position |
| ListItem.Property(Screenplay.X.Job) | Job of Screenplay at X position |
| ListItem.Property(Screenplay.X.Department) | Department of Screenplay at X position |
| ListItem.Property(Screenplay.X.Thumb) | Thumb of Screenplay at X position |
| ListItem.Property(Director.X.Name) | Name of Director at X position |
| ListItem.Property(Director.X.Role) | Role of Director at X position |
| ListItem.Property(Director.X.Job) | Job of Director at X position |
| ListItem.Property(Director.X.Department) | Department of Director at X position |
| ListItem.Property(Director.X.Thumb) | Thumb of Director at X position |
| ListItem.Property(Writer.X.Name) | Name of Writer at X position |
| ListItem.Property(Writer.X.Role) | Role of Writer at X position |
| ListItem.Property(Writer.X.Job) | Job of Writer at X position |
| ListItem.Property(Writer.X.Department) | Department of Writer at X position |
| ListItem.Property(Writer.X.Thumb) | Thumb of Writer at X position |
| ListItem.Property(Producer.X.Name) | Name of Producer at X position |
| ListItem.Property(Producer.X.Role) | Role of Producer at X position |
| ListItem.Property(Producer.X.Job) | Job of Producer at X position |
| ListItem.Property(Producer.X.Department) | Department of Producer at X position |
| ListItem.Property(Producer.X.Thumb) | Thumb of Producer at X position |
| ListItem.Property(Sound_Department.X.Name) | Name of Sound_Department at X position |
| ListItem.Property(Sound_Department.X.Role) | Role of Sound_Department at X position |
| ListItem.Property(Sound_Department.X.Job) | Job of Sound_Department at X position |
| ListItem.Property(Sound_Department.X.Department) | Department of Sound_Department at X position |
| ListItem.Property(Sound_Department.X.Thumb) | Thumb of Sound_Department at X position |
| ListItem.Property(Art_Department.X.Name) | Name of Art_Department at X position |
| ListItem.Property(Art_Department.X.Role) | Role of Art_Department at X position |
| ListItem.Property(Art_Department.X.Job) | Job of Art_Department at X position |
| ListItem.Property(Art_Department.X.Department) | Department of Art_Department at X position |
| ListItem.Property(Art_Department.X.Thumb) | Thumb of Art_Department at X position |
| ListItem.Property(Photography.X.Name) | Name of Photography at X position |
| ListItem.Property(Photography.X.Role) | Role of Photography at X position |
| ListItem.Property(Photography.X.Job) | Job of Photography at X position |
| ListItem.Property(Photography.X.Department) | Department of Photography at X position |
| ListItem.Property(Photography.X.Thumb) | Thumb of Photography at X position |
| ListItem.Property(Editor.X.Name) | Name of Editor at X position |
| ListItem.Property(Editor.X.Role) | Role of Editor at X position |
| ListItem.Property(Editor.X.Job) | Job of Editor at X position |
| ListItem.Property(Editor.X.Department) | Department of Editor at X position |
| ListItem.Property(Editor.X.Thumb) | Thumb of Editor at X position |
| ListItem.Property(original_language) | Original language of the production |

### Movie Specific
| InfoLabel | Description |
| :--- | :--- |
| ListItem.Set | Name of Set Movie Belongs To|
| ListItem.Tagline | Tagline |
| ListItem.Property(Budget) | Budget |
| ListItem.Property(Revenue) | Revenue |
| ListItem.Property(Set.TMDb_ID) | TMDb_ID of Set Movie Belongs To |
| ListItem.Property(Set.Name) | Name of Set Movie Belongs To |
| ListItem.Property(Set.Poster) | Poster of Set Movie Belongs To |
| ListItem.Property(Set.Fanart) | Fanart of Set Movie Belongs To |

### TvShow Specific
| InfoLabel | Description |
| :--- | :--- |
| ListItem.Episode | Episode Number |
| ListItem.Season | Season Number |
| ListItem.Property(Last_Aired) | Last Aired Date in Kodi System Short Format |
| ListItem.Property(Last_Aired.Day) | Last Aired Day |
| ListItem.Property(Last_Aired.Long) | Last Aired Date in Kodi System Long Format |
| ListItem.Property(Last_Aired.Short) | Last Aired in `%d %b` format e.g. `6 May` |
| ListItem.Property(Last_Aired.Episode) | Last Aired Episode |
| ListItem.Property(Last_Aired.Name) | Last Aired Name |
| ListItem.Property(Last_Aired.TMDb_ID) | Last Aired TMDb_ID |
| ListItem.Property(Last_Aired.Plot) | Last Aired Plot |
| ListItem.Property(Last_Aired.Season) | Last Aired Season |
| ListItem.Property(Last_Aired.Rating) | Last Aired Rating |
| ListItem.Property(Last_Aired.Votes) | Last Aired Votes |
| ListItem.Property(Last_Aired.Thumb) | Last Aired Thumb |
| ListItem.Property(Next_Aired) | Next Aired Date in Kodi System Short Format |
| ListItem.Property(Next_Aired.Day) | Next Aired Day |
| ListItem.Property(Next_Aired.Long) | Next Aired Date in Kodi System Long Format |
| ListItem.Property(Next_Aired.Short) | Next Aired Date in `%d %b` format e.g. `6 May` |
| ListItem.Property(Next_Aired.Episode) | Next Aired Episode |
| ListItem.Property(Next_Aired.Name) | Next Aired Name |
| ListItem.Property(Next_Aired.TMDb_ID) | Next Aired TMDb_ID |
| ListItem.Property(Next_Aired.Plot) | Next Aired Plot |
| ListItem.Property(Next_Aired.Season) | Next Aired Season |
| ListItem.Property(Next_Aired.Thumb) | Next Aired Thumb |
| ListItem.Property(Creator) | List of TvShow Creators |
| ListItem.Property(Creator.X.Name) | Name of Creator at X Position |
| ListItem.Property(Creator.X.TMDb_ID) | TMDb ID of Creator at X Position |
| ListItem.Property(Creator.X.Thumb) | Thumb of Creator at X Position |
| ListItem.Property(Network) | List of Networks. Note for TV Shows `ListItem.Studio` combines Release Network + Production Studios. Use `Network` property to retrieve only TV Networks. |
| ListItem.Property(Network.X.Name) | Name of Network at X position. Note for TV Shows `Studio.X` properties contain only Production Studios. Use `Network.X` properties to retrieve TV Networks. |
| ListItem.Property(Network.X.Icon) | Icon of Network at X position |
| ListItem.Property(Network.X.TMDb_ID) | TMDb_ID of Network at X position |
| ListItem.Property(UnWatchedEpisodes) | Number of Episodes Remaining (Trakt) |

### Person Specific
| InfoLabel | Description |
| :--- | :--- |
| ListItem.Property(Biography) | Biography |
| ListItem.Property(Age) | Age |
| ListItem.Property(Birthday) | Date of Birth |
| ListItem.Property(Deathday) | Date of Death |
| ListItem.Property(Character) | Character Person is Known For |
| ListItem.Property(Department) | Department Most Commonly Associated With Person |
| ListItem.Property(Job) | Job Most Commonly Associated With Person |
| ListItem.Property(Known_For) | List of Title Person is Known For |
| ListItem.Property(Role) | Role Person is Known For |
| ListItem.Property(Born) | Place Person Was Born |
| ListItem.Property(Gender) | Gender |
| ListItem.Property(Aliases) | Other Names Person is Known By |
| ListItem.Property(Known_For.X.Title) | Title of Known For Item at X Position. Also accepts TMDb_ID, Rating, TMDb_Type in place of Title. |
| ListItem.Property(Movie.Cast.X.Title) | Title of Movie person starred in at X position. Also accepts TMDb_ID, Rating, Votes, Plot, Premiered, Poster, Fanart, Character in place of Title. |
| ListItem.Property(Movie.Crew.X.Title) | Title of Movie person crewed in at X position. Also accepts TMDb_ID, Rating, Votes, Plot, Premiered, Poster, Fanart, Department, Job in place of Title. |
| ListItem.Property(TVShow.Cast.X.Title) | Title of TVShow person starred in at X position. Also accepts TMDb_ID, Rating, Votes, Plot, Premiered, Poster, Fanart, Character, Episodes in place of Title. |
| ListItem.Property(TVShow.Crew.X.Title) | Title of TVShow person crewed in at X position. Also accepts TMDb_ID, Rating, Votes, Plot, Premiered, Poster, Fanart, Department, Job, Episodes in place of Title. |
| ListItem.Property(numitems.tmdb.movies.cast) | Number of credited movies as a cast member |
| ListItem.Property(numitems.tmdb.movies.crew) | Number of credited movies as a crew member |
| ListItem.Property(numitems.tmdb.movies.total) | Number of credited movies in total |
| ListItem.Property(numitems.tmdb.tvshows.cast) | Number of credited tvshows as a cast member |
| ListItem.Property(numitems.tmdb.tvshows.crew) | Number of credited tvshows as a crew member |
| ListItem.Property(numitems.tmdb.tvshows.total) | Number of credited tvshows in total |

### Movie Set Specific
| InfoLabel | Description |
| :--- | :--- |
| ListItem.Property(Set.X.Title) | Title of Movie at X Position in Set |
| ListItem.Property(Set.X.TMDb_ID) | TMDb_ID of Movie at X Position in Set |
| ListItem.Property(Set.X.OriginalTitle) | OriginalTitle of Movie at X Position in Set |
| ListItem.Property(Set.X.Plot) | Plot of Movie at X Position in Set |
| ListItem.Property(Set.X.Premiered) | Premiered of Movie at X Position in Set |
| ListItem.Property(Set.X.Year) | Year of Movie at X Position in Set |
| ListItem.Property(Set.X.Rating) | Rating of Movie at X Position in Set |
| ListItem.Property(Set.X.Votes) | Votes of Movie at X Position in Set |
| ListItem.Property(Set.X.Poster) | Poster of Movie at X Position in Set |
| ListItem.Property(Set.X.Fanart) | Fanart of Movie at X Position in Set |
| ListItem.Property(Set.X.Genre) | Genres of Movie at X Position in Set |
| ListItem.Property(Set.Year.First) | Year of First Movie in Set |
| ListItem.Property(Set.Year.Last) | Year of Last Movie in Set |
| ListItem.Property(Set.Years) | Earliest and Latest Years |
| ListItem.Property(Set.Rating) | Average of Ratings for All Movies in Set |
| ListItem.Property(Set.Votes) | Total Votes for All Movies in Set |
| ListItem.Property(Set.NumItems) | Number of Items in Set |
| ListItem.Property(Set.Genres) | All Genres of Movies in Set |

### Ratings Specific

| InfoLabel | Description |
| :--- | :--- |
| ListItem.Property(Awards) | Oscars and Other Awards/Nominations (OMDb) |
| ListItem.Property(Oscar_Wins) | Number of Oscar wins (OMDb) |
| ListItem.Property(Oscar_Nominations) | Number of Oscar nominations (OMDb) |
| ListItem.Property(Award_Wins) | Number of other award wins (OMDb) |
| ListItem.Property(Award_Nominations) | Number of other award nominations (OMDb) |
| ListItem.Property(TMDb_Rating) | TMDb Rating |
| ListItem.Property(TMDb_Votes) | TMDb Votes |
| ListItem.Property(Trakt_Rating) | Trakt Rating (Trakt) |
| ListItem.Property(Trakt_Votes) | Trakt Votes (Trakt) |
| ListItem.Property(Metacritic_Rating) | Metacritic Rating (OMDb) |
| ListItem.Property(IMDb_Rating) | IMDb_Rating (OMDb) |
| ListItem.Property(IMDb_Votes) | IMDb_Votes (OMDb) |
| ListItem.Property(RottenTomatoes_Rating) | RottenTomatoes_Rating (OMDb) |
| ListItem.Property(RottenTomatoes_Image) | RottenTomatoes_Image (OMDb) |
| ListItem.Property(RottenTomatoes_ReviewsTotal) | RottenTomatoes_ReviewsTotal (OMDb) |
| ListItem.Property(RottenTomatoes_ReviewsFresh) | RottenTomatoes_ReviewsFresh (OMDb) |
| ListItem.Property(RottenTomatoes_ReviewsRotten) | RottenTomatoes_ReviewsRotten (OMDb) |
| ListItem.Property(RottenTomatoes_Consensus) | RottenTomatoes_Consensus (OMDb) |
| ListItem.Property(RottenTomatoes_UserMeter) | RottenTomatoes_UserMeter (OMDb) |
| ListItem.Property(RottenTomatoes_UserReviews) | RottenTomatoes_UserReviews (OMDb) |
| ListItem.Property(emmy_wins) | Emmy Wins (OMDb) |
| ListItem.Property(emmy_nominations) | Emmy Nominations (OMDb) |
| ListItem.Property(top250) | IMDb Top250 Position (IMDb via Trakt list) |
| ListItem.Property(total_awards_won) | Total Awards Won (TVDb) |
| ListItem.Property(awards_won) | Separated `/` list of Awards Won (TVDb) |
| ListItem.Property(awards_won_cr) | Separated '[CR]' list of Awards Won (TVDb) |
| ListItem.Property(academy_awards_won) | Total Academy Awards Won (TVDb) |
| ListItem.Property(goldenglobe_awards_won) | Total Golden Globes Won (TVDb) |
| ListItem.Property(mtv_awards_won) | Total MTV Awards Won (TVDb) |
| ListItem.Property(criticschoice_awards_won) | Total Critics Choice Awards Won (TVDb) |
| ListItem.Property(emmy_awards_won) | Total Primetime Emmys Won (TVDb) |
| ListItem.Property(sag_awards_won) | Total SAG Awards Won (TVDb) |
| ListItem.Property(bafta_awards_won) | Total BAFTA Awards Won (TVDb) |
| ListItem.Property(total_awards_nominated) | Total Awards Nominated (TVDb) |
| ListItem.Property(awards_nominated) | Separated `/` list of Awards Nominated (TVDb) |
| ListItem.Property(awards_nominated_cr) | Separated '[CR]' list of Awards Nominated (TVDb) |
| ListItem.Property(academy_awards_nominated) | Total Academy Awards Nominated (TVDb) |
| ListItem.Property(goldenglobe_awards_nominated) | Total Golden Globes Nominated (TVDb) |
| ListItem.Property(mtv_awards_nominated) | Total MTV Awards Nominated (TVDb) |
| ListItem.Property(criticschoice_awards_nominated) | Total Critics Choice Awards Nominated (TVDb) |
| ListItem.Property(emmy_awards_nominated) | Total Primetime Emmys Nominated (TVDb) |
| ListItem.Property(sag_awards_nominated) | Total SAG Awards Nominated (TVDb) |
| ListItem.Property(bafta_awards_nominated) | Total BAFTA Awards Nominated (TVDb) |


### Artwork Specific
| InfoLabel | Description |
| :--- | :--- |
| ListItem.Art(Poster) | Poster |
| ListItem.Art(Fanart) | Fanart |
| ListItem.Art(ClearArt) | ClearArt (Fanart.tv) |
| ListItem.Art(ClearLogo) | Clearlogo (Fanart.tv) |
| ListItem.Art(Landscape) | Landscape (Fanart.tv) |
| ListItem.Art(Banner) | Banner (Fanart.tv) |


