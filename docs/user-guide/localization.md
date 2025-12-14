# Localization

Localization files live under `src/resources/language/` with per-locale folders and strings (`strings.po`). UI strings referenced in code use 320xx IDs.

## Structure
- `resource.language.en_gb`, `resource.language.ru_ru`, `resource.language.uk_ua`.
- Each folder contains `strings.po` with msgctxt IDs like `#32001` etc.

## Key string usage examples
- 32001/32002/32003: authentication dialogs and errors (`auth.py`).
- 32019/32020/32021/32022: menu labels for search/fresh/hot/popular (`plugin.py`, `main.py`).
- 32025/32026: search UI prompts and clear-history confirmation (`main.py`).
- 32028-32034: bookmarks UI and context menus (`main.py`, `listitem.py`).
- 32040: comments dialog title (`main.py`).

## Adding/updating translations
1. Edit the relevant `strings.po` in the locale folder; keep msgctxt IDs unchanged.
2. Use the same 320xx IDs referenced in code; add msgstr for the target language.
3. Test in Kodi by selecting the locale and verifying UI labels/dialogs render correctly.

## Sources
- src/resources/language/*
- src/resources/lib/main.py, auth.py, listitem.py (string references)
