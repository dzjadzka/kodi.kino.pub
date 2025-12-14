# Playback Flow Documentation

Complete playback mechanism specification for the kodi.kino.pub addon.

## Overview

The addon supports playback of:
- **Movies** - Single video files
- **Multi-episode items** - Multiple videos without seasons
- **TV shows** - Multi-season series with episodes
- **Live TV** - Streaming channels

**Stream Types Supported:**
- HLS (HTTP Live Streaming)
- HLS variants (hls, hls2, hls4)
- InputStream Adaptive integration for HLS

---

## Playback Initiation Flow

### User Triggers Playback

```
User selects item → Play
    ↓
Route: /play/<item_id>
    ↓
Handler: play(item_id) in main.py:290
    ↓
Parse query params: season_index, index
    ↓
Instantiate item from ID
    ├─→ Check window property cache first
    └─→ If not found: API GET /items/{id}
    ↓
Get playable item
    ├─→ Movie: item itself
    ├─→ Multi: item.videos[index]
    ├─→ TVShow: item.seasons[season_index].episodes[index]
    └─→ Create PlayableItem instance
    ↓
Build playable_list_item
    ├─→ Resolve media_url
    ├─→ Set InputStream properties (if HLS enabled)
    ├─→ Add subtitles
    ├─→ Set video info
    └─→ Set resume time
    ↓
Create Player(list_item)
    ↓
xbmcplugin.setResolvedUrl()
    ↓
Kodi starts playback
    ↓
Player.onPlayBackStarted()
    ├─→ Clear window property
    ├─→ Refresh token if needed
    └─→ Set Trakt.tv properties
    ↓
[Playback monitoring every 1 second]
    ↓
Player.onPlayBackStopped() / onPlayBackEnded()
    ├─→ Calculate resume point or watched status
    └─→ API: watching/marktime or watching/toggle
```

---

## Video URL Resolution

### Quality Selection

**Code:** `modeling.py:269-282`

**Process:**

```python
desired_quality = plugin.settings.video_quality  # "1080p"
desired_stream_type = plugin.settings.stream_type  # "hls4"
ask_quality = plugin.settings.ask_quality  # "true"/"false"

if ask_quality == "true":
    # Show dialog with available qualities
    return _get_media_url_from_dialog()

# Auto-select based on settings
files = {file["quality"]: file["url"] for file in video_data["files"]}

try:
    # Try preferred quality + stream type
    return files[desired_quality][desired_stream_type]
except KeyError:
    # Fallback to highest available quality
    return files[natural_sort(list(files.keys()))[-1]][desired_stream_type]
```

**Quality Levels:**
- `2160p` - 4K UHD
- `1080p` - Full HD (default)
- `720p` - HD
- `480p` - SD

**Stream Types:**
- `hls` - Basic HLS
- `hls2` - HLS variant 2
- `hls4` - HLS variant 4 / MPEG-DASH (default)

**Fallback Strategy:**
1. Try user's preferred quality + stream type
2. If not available: Highest quality + preferred stream type
3. Natural sort ensures proper quality ordering

---

### CDN Location

**Code:** `modeling.py:239-250`

Adds location parameter to URL:

```python
def _choose_cdn_loc(self, url: str) -> str:
    parsed = urllib.parse.urlparse(url)
    return urllib.parse.urlunparse((
        parsed.scheme,
        parsed.netloc,
        parsed.path,
        parsed.params,
        f"loc={self.plugin.settings.loc}",  # "ru" or "nl"
        parsed.fragment,
    ))
```

**Locations:**
- `ru` - Russia (default)
- `nl` - Netherlands

**Result:** `https://cdn.example.com/video.m3u8?loc=ru`

---

### Quality Selection Dialog

**Code:** `modeling.py:284-303`

When `ask_quality=true`:

```python
def _get_media_url_from_dialog(self) -> str:
    files = {file_["quality"]: file_["url"] for file_ in self.video_data["files"]}
    
    # Sort qualities in descending order
    qualities = natural_sort(list(files.keys()), reverse=True)
    
    # Show selection dialog
    idx = xbmcgui.Dialog().select(
        localize(32043),  # "Choose video quality"
        qualities
    )
    
    if idx >= 0:
        selected_quality = qualities[idx]
        return self._choose_cdn_loc(
            files[selected_quality][self.plugin.settings.stream_type]
        )
    
    # User cancelled - return highest quality
    return self._choose_cdn_loc(
        files[qualities[0]][self.plugin.settings.stream_type]
    )
```

**UI:** Simple list selection dialog with qualities in descending order

---

## InputStream Adaptive Integration

### Conditions for HLS Playback

**Code:** `plugin.py:252-258`

```python
@property
def is_hls_enabled(self) -> bool:
    return (
        "hls" in self.settings.stream_type
        and self.settings.use_inputstream_adaptive == "true"
        and inputstreamhelper is not None
    )
```

**Requirements:**
1. Stream type contains "hls"
2. Setting `use_inputstream_adaptive` = true
3. inputstreamhelper module available (optional dependency)

---

### InputStream Properties

**Code:** `modeling.py:305-332`

```python
@property
def hls_properties(self) -> Dict[str, str]:
    if not self.plugin.is_hls_enabled:
        popup_warning(localize(32044))  # "HLS stream is not supported"
        return {}
    
    try:
        from inputstreamhelper import Helper
        
        is_helper = Helper("hls")
        if not is_helper.check_inputstream():
            # InputStream Adaptive not installed/configured
            return {}
    except Exception:
        return {}
    
    return {
        "inputstream": "inputstream.adaptive",
        "inputstream.adaptive.manifest_type": "hls",
    }
```

**Properties Set:**
- `inputstream` - Addon to use (`inputstream.adaptive`)
- `inputstream.adaptive.manifest_type` - Stream type (`hls`)

**Helper Check:**
- Validates InputStream Adaptive installation
- If not installed: Returns empty dict (fallback to direct play)

---

### ListItem Configuration

**Code:** `modeling.py:252-268`

```python
@property
def playable_list_item(self) -> ExtendedListItem:
    li = self.list_item
    li.setPath(self.media_url)
    li.setSubtitles([st["url"] for st in self.video_data.get("subtitles", [])])
    
    # Add InputStream properties if HLS enabled
    for prop, value in self.hls_properties.items():
        li.setProperty(prop, value)
    
    li.setProperty("play_duration", str(self.video_data["duration"]))
    li.setProperty("imdbnumber", str(self.item_id))
    
    return li
```

**Properties:**
- `path` - Resolved video URL
- `subtitles` - Subtitle file URLs
- `play_duration` - Video duration (for token refresh check)
- `imdbnumber` - Item ID
- Plus InputStream properties if HLS enabled

---

## Playback State Management

### Player Class

**Code:** `player.py:31-108`

```python
class Player(xbmc.Player):
    def __init__(self, list_item: ExtendedListItem) -> None:
        super().__init__()
        self.list_item = list_item
        self.plugin = list_item.plugin
        self.play(list_item.getPath(), list_item)
```

**Lifecycle Events:**
- `onPlayBackStarted()` - Playback begins
- `onPlayBackStopped()` - User stops playback
- `onPlayBackEnded()` - Playback completes
- `onPlayBackError()` - Playback error

---

### Playback Start

**Code:** `player.py:61-76`

```python
def onPlayBackStarted(self) -> None:
    self.plugin.logger.debug("Playback started")
    
    # Clear cached items from window
    self.plugin.clear_window_property()
    
    # Refresh token if expires during playback
    if self.should_refresh_token:
        self.plugin.logger.debug("Access token should be refreshed")
        self.plugin.auth.get_token()
    
    # Set Trakt.tv scrobble properties
    imdb_id = f"tt{int(self.list_item.getProperty('imdbnumber')):07d}"
    ids = json.dumps({"imdb": imdb_id})
    xbmcgui.Window(10000).setProperty("script.trakt.ids", ids)
```

**Actions:**
1. Clear window property (item cache)
2. Refresh token if playback longer than token lifetime
3. Set Trakt.tv scrobble data

---

### Token Refresh Check

**Code:** `player.py:45-48`

```python
@property
def should_refresh_token(self) -> bool:
    current_time = int(time.time())
    play_duration = int(self.list_item.getProperty("play_duration"))
    token_expire = int(self.plugin.settings.access_token_expire)
    
    return current_time + play_duration >= token_expire
```

**Logic:** If `now + video_duration >= token_expiry`, refresh proactively

**Purpose:** Prevent token expiry mid-playback (would interrupt marktime updates)

---

### Marktime Updates

**Code:** `player.py:50-58`

```python
def set_marktime(self) -> None:
    if self.isPlaying():
        current_time = int(self.getTime())
        item_id = int(self.list_item.getProperty("id"))
        season = self.list_item.getProperty("season")
        video = self.list_item.getProperty("video")
        
        data = {"id": item_id, "time": current_time}
        if season:
            data["season"] = int(season)
        if video:
            data["video"] = int(video)
        
        self.plugin.client("watching/marktime").get(data=data)
```

**Frequency:** Every 1 second while playing

**API Call:** `GET /watching/marktime?id={id}&time={seconds}&season={s}&video={v}`

---

### Playback Stop

**Code:** `player.py:78-90`

```python
def onPlayBackStopped(self) -> None:
    if self.should_make_resume_point:
        # Save resume point
        self.set_marktime()
    elif self.should_reset_resume_point:
        # Clear resume point
        data = {"id": item_id, "time": 0}
        # Add season/video if present
        self.plugin.client("watching/marktime").get(data=data)
```

**Logic:**

```python
@property
def should_make_resume_point(self) -> bool:
    current_time = self.getTime()
    total_time = self.getTotalTime()
    percentage = (current_time / total_time) * 100
    
    # Between start threshold and completion threshold
    return (
        current_time > ignoresecondsatstart
        and percentage < playcountminimumpercent
    )

@property
def should_reset_resume_point(self) -> bool:
    # Watched to completion, clear resume
    return self.should_mark_as_watched
```

**Thresholds:**
- `ignoresecondsatstart` - Kodi setting (default: 180s)
- `playcountminimumpercent` - Kodi setting (default: 90%)

---

### Playback Complete

**Code:** `player.py:92-104`

```python
def onPlayBackEnded(self) -> None:
    if self.should_mark_as_watched:
        item_id = int(self.list_item.getProperty("id"))
        season = self.list_item.getProperty("season")
        video = self.list_item.getProperty("video")
        
        data = {"id": item_id, "status": 1}  # 1 = watched
        if season:
            data["season"] = int(season)
        if video:
            data["video"] = int(video)
        
        self.plugin.client("watching/toggle").get(data=data)
```

**Logic:**

```python
@property
def should_mark_as_watched(self) -> bool:
    percentage = (self.getTime() / self.getTotalTime()) * 100
    return percentage >= playcountminimumpercent  # >= 90%
```

**API Call:** `GET /watching/toggle?id={id}&status=1&season={s}&video={v}`

---

## Multi-Episode Handling

### Multi Class

**Code:** `modeling.py:438-456`

For items with `subtype: "multi"`:

```python
class Multi(ItemEntity):
    isdir: ClassVar[bool] = True
    
    @property
    def videos(self) -> List[Episode]:
        return [
            Episode(parent=self, item_data=self.item, video_data=v, index=i)
            for i, v in enumerate(self.item["videos"])
        ]
```

**Structure:** Flat list of episodes (no seasons)

**Navigation:**
```
Multi Item
└── /episodes/<item_id>/
    ├── Episode 1 (index=0)
    ├── Episode 2 (index=1)
    └── ...
```

**Playback:** `/play/<item_id>?index=0`

---

### Episode Class

**Code:** `modeling.py:458-488`

```python
class Episode(PlayableItem):
    def __init__(self, *, parent, item_data, video_data, index):
        super().__init__(parent=parent, item_data=item_data)
        self._video_data = video_data
        self._index = index
    
    @property
    def video_data(self):
        return self._video_data
    
    @property
    def video_info(self) -> Dict[str, Any]:
        info = super().video_info
        info.update({
            "mediatype": "episode",
            "episode": self._video_data["number"],
            "tvshowtitle": self.parent.title,
        })
        return info
```

**Video Info:**
- `mediatype`: "episode"
- `episode`: Episode number
- `tvshowtitle`: Parent item title

---

## TV Show Handling

### TVShow Class

**Code:** `modeling.py:334-366`

```python
class TVShow(ItemEntity):
    isdir: ClassVar[bool] = True
    
    @cached_property
    def seasons(self) -> List[Season]:
        return [
            Season(parent=self, season_data=s, tvshow_title=self.title)
            for s in self.item["seasons"]
        ]
```

**Navigation:**
```
TV Show
└── /seasons/<item_id>/
    ├── Season 1
    │   └── /season_episodes/<item_id>/1/
    │       ├── S01E01
    │       ├── S01E02
    │       └── ...
    ├── Season 2
    └── ...
```

---

### Season Class

**Code:** `modeling.py:368-397`

```python
class Season(ItemEntity):
    isdir: ClassVar[bool] = True
    
    def __init__(self, *, parent, season_data, tvshow_title):
        self.parent = parent
        self.season_data = season_data
        self.season_number = season_data["number"]
        self.tvshow_title = tvshow_title
    
    @property
    def episodes(self) -> List[SeasonEpisode]:
        return [
            SeasonEpisode(
                parent=self,
                item_data=self.parent.item,
                video_data=ep,
                index=i,
                tvshow_title=self.tvshow_title,
            )
            for i, ep in enumerate(self.season_data["episodes"])
        ]
```

**Title Format:**
```python
f"{'ended' if ended else 'on air'} Season {season_number}"
```

---

### SeasonEpisode Class

**Code:** `modeling.py:399-436`

```python
class SeasonEpisode(PlayableItem):
    def __init__(self, *, parent, item_data, video_data, index, tvshow_title):
        super().__init__(parent=parent, item_data=item_data)
        self._video_data = video_data
        self._index = index
        self.tvshow_title = tvshow_title
    
    @property
    def video_info(self) -> Dict[str, Any]:
        info = super().video_info
        info.update({
            "mediatype": "episode",
            "episode": self._video_data["number"],
            "season": self._video_data["snumber"],
            "tvshowtitle": self.tvshow_title,
        })
        return info
```

**Video Info:**
- `mediatype`: "episode"
- `episode`: Episode number within season
- `season`: Season number
- `tvshowtitle`: TV show title

**Playback:** `/play/<item_id>?season_index=0&index=2` (Season 1, Episode 3)

---

## Resume Points

### Resume Time Calculation

**Code:** `modeling.py:491-529` (Movie example)

```python
@property
def video_info(self) -> Dict[str, Any]:
    info = super().video_info
    info.update({
        "mediatype": "movie",
        "playcount": self.watching_info["status"],  # 0 or 1
        "duration": self.video_data["duration"],
    })
    
    # Add resume time if unwatched and has resume point
    if info["playcount"] == 0 and self.watching_info["time"]:
        info["time"] = self.watching_info["time"]
    
    return info
```

**Logic:**
- If `status=0` (unwatched) AND `time>0`: Set resume point
- If `status=1` (watched): No resume point
- Kodi uses `time` field to resume playback

---

## Subtitles

**Code:** `modeling.py:256`

```python
li.setSubtitles([st["url"] for st in self.video_data.get("subtitles", [])])
```

**Format:** Array of subtitle URLs (direct .srt file links)

**Example:**
```python
[
    "https://cdn.example.com/subtitles_en.srt",
    "https://cdn.example.com/subtitles_ru.srt"
]
```

**Kodi Behavior:** User can select subtitle track during playback

---

## Playback Flow Diagrams

### Movie Playback

```
User clicks Movie
    ↓
/play/<movie_id>
    ↓
Instantiate Movie(item_data)
    ↓
movie.playable_list_item
    ├─→ media_url: Resolve quality + stream type
    ├─→ hls_properties: Set InputStream if enabled
    ├─→ subtitles: Add subtitle URLs
    └─→ video_info: Set resume point if exists
    ↓
Player(list_item).play()
    ↓
Kodi plays video
```

---

### TV Show Episode Playback

```
User clicks TV Show
    ↓
/seasons/<show_id>/
    └─→ List seasons
        ↓
    User clicks Season 1
        ↓
    /season_episodes/<show_id>/1/
        └─→ List episodes
            ↓
        User clicks S01E03
            ↓
        /play/<show_id>?season_index=0&index=2
            ↓
        Instantiate TVShow(item_data)
            ↓
        Get season: tvshow.seasons[0]
            ↓
        Get episode: season.episodes[2]
            ↓
        episode.playable_list_item
            ├─→ media_url: Resolve from episode.video_data
            └─→ video_info: episode=3, season=1
            ↓
        Player(list_item).play()
```

---

## Summary

### Playback Characteristics

- **Supported Formats:** HLS (primary), direct HTTP
- **Quality Levels:** 480p, 720p, 1080p, 2160p
- **Quality Selection:** Auto (user preference) or manual (dialog)
- **InputStream Adaptive:** Optional HLS optimization
- **CDN:** Russia or Netherlands location
- **Subtitles:** Multi-language support
- **Resume Points:** Automatic save/restore
- **Watch Status:** Auto-mark at 90% completion
- **Token Management:** Proactive refresh before long videos

### State Tracking

- **Marktime:** Updated every 1 second during playback
- **Resume Points:** Saved between start threshold and 90%
- **Watched Status:** Marked at 90%+ completion
- **Clear Resume:** When marked as watched

### Integration

- **InputStream Adaptive:** HLS streaming optimization
- **Trakt.tv:** Scrobble support via window properties
- **Kodi Settings:** Respects playcount thresholds

---

## References

- Playback models: `src/resources/lib/modeling.py:232-529`
- Player implementation: `src/resources/lib/player.py`
- Quality selection: `src/resources/lib/modeling.py:269-303`
- InputStream integration: `src/resources/lib/modeling.py:305-332`
- State management: `src/resources/lib/player.py:45-104`
- Play route: `src/resources/lib/main.py:290-300`
