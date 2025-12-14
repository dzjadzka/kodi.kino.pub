---
id: task-017.10
title: Verify listitem season/episode metadata for TMDbHelper matching
status: Done
assignee: []
created_date: '2025-12-14 15:05'
updated_date: '2025-12-14 15:06'
labels:
  - kodi
  - player
  - qa
dependencies:
  - task-017.02
  - task-017.05
parent_task_id: task-017
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Confirm video.kino.pub emits season/episode info in listitems (seasons and episodes) so TMDbHelper player steps can match and auto-select. Add minimal fixes if any fields missing.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 Listitem metadata for seasons and episodes verified from code/logs (season, episode, tvshowtitle) and noted with file references
- [x] #2 If gaps exist, minimal backward-compatible fix implemented in video.kino.pub to set season/episode infolabels
- [x] #3 Result documented in task notes and referenced in doc-001
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Verified from code that Season/SeasonEpisode listitems set season/episode infolabels via video_info in src/resources/lib/modeling.py: Season.video_info includes "season"; SeasonEpisode.video_info includes "season" and "episode", tvshowtitle, duration, playcount. ExtendedListItem calls setInfo("video", video_info), so TMDbHelper matching can use season/episode. No code changes needed; decision recorded in doc-001.
<!-- SECTION:NOTES:END -->
