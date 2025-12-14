# Settings and environment

Environment flags adjust API targets and logging.

## KINO_PUB_TEST
- When set (truthy), `Settings.is_testing` returns True.
- API URLs switch to localhost mockserver endpoints: `api_url` -> `http://localhost:1080/v1`, `oauth_api_url` -> `http://localhost:1080/v1/oauth2/device`.
- Logger enables rotating file handler at `special://temp/video_kino_pub.log` with DEBUG level for detailed traces.

## Defaults and advanced settings
- Without the flag, API targets are production (`https://api.srvkp.com/v1` and `/oauth2/device`).
- Advanced video thresholds default to playcountminimumpercent=90, ignoresecondsatstart=180, ignorepercentatend=8 unless overridden in Kodi `advancedsettings.xml`.

## When to use
- Enable `KINO_PUB_TEST` during integration tests or local development with the mockserver to avoid hitting production APIs and to capture verbose logs.

## Sources
- src/resources/lib/settings.py
- src/resources/lib/logger.py
