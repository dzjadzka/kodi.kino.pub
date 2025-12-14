---
id: task-008
title: Write backlog/docs/user-guide/settings.md
status: Done
assignee: []
created_date: '2025-12-14 12:06'
updated_date: '2025-12-14 12:17'
labels:
  - docs
dependencies: []
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Enumerate user-facing settings using src/resources/settings.xml and Settings helper in resources/lib/settings.py (video quality/stream type, ask_quality, mark_advert, exclude_anime, inputstream adaptive toggle/install helper, loc, history_max_qty, sorting, etc.).
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 backlog/docs/user-guide/settings.md lists all user-facing settings from src/resources/settings.xml with brief explanations
- [x] #2 Notes how Settings helper in resources/lib/settings.py interprets key options (quality/stream type, ask_quality, mark_advert, exclude_anime, inputstream adaptive toggle/install helper, loc, history_max_qty, sorting)
- [x] #3 Mentions defaults and any dependencies between settings where applicable
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
docs/user-guide/settings.md lists user settings from settings.xml, explains dependencies (ask_quality/HLS, inputstream toggles), sorting, search history, menu visibility, advanced defaults. Sources: settings.xml, settings.py.
<!-- SECTION:NOTES:END -->
