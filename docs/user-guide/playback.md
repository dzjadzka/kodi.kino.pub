# Playback

Playback and resume logic are managed by `Player` (`src/resources/lib/player.py`) and list item metadata built from modeling utilities.

## Starting playback
- Route `/play/<item_id>` resolves a playable list item (season/index aware) and hands it to Kodi; tokens are refreshed if they would expire before the stream ends.
- Trailer playback uses `/trailer/<item_id>` and plays the first trailer URL from `items/trailer` API.

## Resume and watched logic
- While playing, the player tracks elapsed time.
- On stop: sends resume point (`watching/marktime`) if past the ignore-seconds threshold; or marks watched via `watching/toggle` once playcount threshold is met; or resets resume to 0 if stopped immediately.
- On end: marks watched if playcount is still zero.

## Quality and stream selection
- Stream type and quality come from settings (HLS variants and quality selection, including ask-when-possible behavior when `ask_quality` is enabled with HLS).
- InputStream Adaptive support is optional; menu actions allow installation and settings if enabled.

## Trakt scrobble properties
- At playback start, if an IMDb id is present, the add-on sets `script.trakt.ids` window property (formatted `tt#######`) for Trakt scrobbling.

## Sources
- src/resources/lib/main.py (`/play`, `/trailer`)
- src/resources/lib/player.py
