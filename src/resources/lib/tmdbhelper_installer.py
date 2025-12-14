import os

import xbmc
import xbmcvfs


_player_json_checked = False


KINOPUB_PLAYER_JSON = """{
  "name": "KinoPub",
  "plugin": "video.kino.pub",
  "provider": "kino.pub",
  "priority": 200,
  "is_resolvable": "true",
  "assert": {
    "play_movie": ["title", "year"],
    "play_episode": ["showname", "season", "episode"],
    "search_movie": ["title"],
    "search_episode": ["showname"]
  },
  "fallback": {
    "play_movie": "kino_pub.json search_movie",
    "play_episode": "kino_pub.json search_episode"
  },
  "play_movie": [
    "plugin://video.kino.pub/search/movies/results/?title={title_url}&year={year}",
    {"title": "(?i).*{title}.*", "year": "{year}"}
  ],
  "play_episode": [
    "plugin://video.kino.pub/search/serials/results/?title={showname_url}",
    {"title": "(?i).*{showname}.*"},
    {"season": "{season}"},
    {"season": "{season}", "episode": "{episode}"},
    {"title": "(?i).*s0*{season}e0*{episode}.*"}
  ],
  "search_movie": "plugin://video.kino.pub/search/movies/results/?title={title_url}",
  "search_episode": "plugin://video.kino.pub/search/serials/results/?title={showname_url}"
}
"""


def _write_embedded_player(dst_path: str) -> bool:
    try:
        file = xbmcvfs.File(dst_path, "w")
        file.write(KINOPUB_PLAYER_JSON)
        file.close()
        return True
    except Exception as exc:  # noqa: BLE001
        xbmc.log(f"[video.kino.pub] Failed to write TMDbHelper player json: {exc}", xbmc.LOGERROR)
        return False


def install_tmdbhelper_player(force: bool = False) -> bool:
    """
    Copy TMDbHelper player JSON into TMDbHelper userdata.

    If the source file is missing from the addon package, fall back to the embedded copy.
    """
    dst_dir = xbmcvfs.translatePath(
        "special://profile/addon_data/plugin.video.themoviedb.helper/players/"
    )
    dst = os.path.join(dst_dir, "kino_pub.json")
    if not force and xbmcvfs.exists(dst):
        return True

    xbmcvfs.mkdirs(dst_dir)
    src = xbmcvfs.translatePath(
        "special://home/addons/video.kino.pub/integrations/tmdbhelper/players/kino_pub.json"
    )
    if xbmcvfs.exists(src):
        ok = xbmcvfs.copy(src, dst)
    else:
        xbmc.log("[video.kino.pub] TMDbHelper player json source missing; writing embedded copy", xbmc.LOGWARNING)
        ok = _write_embedded_player(dst)

    if ok:
        xbmc.log("[video.kino.pub] Installed TMDbHelper player json into userdata", xbmc.LOGINFO)
    else:
        xbmc.log("[video.kino.pub] Failed to install TMDbHelper player json", xbmc.LOGERROR)
    return ok


def ensure_tmdbhelper_player_installed() -> None:
    global _player_json_checked
    if _player_json_checked:
        return
    _player_json_checked = True
    install_tmdbhelper_player(force=False)
