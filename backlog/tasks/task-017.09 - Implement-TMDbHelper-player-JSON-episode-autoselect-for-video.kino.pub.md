---
id: task-017.09
title: 'Implement: TMDbHelper player JSON episode autoselect for video.kino.pub'
status: Done
assignee: []
created_date: '2025-12-14 15:05'
updated_date: '2025-12-14 15:06'
labels:
  - kodi
  - tmdbhelper
  - player
dependencies:
  - task-017.04
parent_task_id: task-017
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Update the user player JSON (external to TMDbHelper) so play_episode automatically selects show → season → episode and starts playback via video.kino.pub routes.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 Player JSON updated with URL-encoded show titles and explicit season/episode navigation steps (regex fallback)
- [x] #2 Fallback keeps search listing if matching fails; movies remain unaffected
- [x] #3 Install path documented for TMDbHelper userdata
- [x] #4 Change recorded in repo under integrations/tmdbhelper/players/kino_pub.json
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Updated user player JSON at integrations/tmdbhelper/players/kino_pub.json: URL-encoded titles, explicit show->season->episode navigation with regex fallback, search fallbacks unchanged. Install path documented in docs/tmdbhelper-integration-testing.md (place into special://profile/addon_data/plugin.video.themoviedb.helper/players/). Movies untouched.
<!-- SECTION:NOTES:END -->
