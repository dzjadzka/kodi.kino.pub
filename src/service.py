"""Run once at login to install the TMDbHelper player JSON if it is missing."""

from resources.lib.tmdbhelper_installer import ensure_tmdbhelper_player_installed


def run() -> None:
    ensure_tmdbhelper_player_installed()


if __name__ == "__main__":
    run()
