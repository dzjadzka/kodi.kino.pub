---
id: task-017.05
title: 'Plan: video.kino.pub resolver/search support for TMDbHelper'
status: To Do
assignee: []
created_date: '2025-12-14 12:45'
updated_date: '2025-12-14 15:21'
labels:
  - kodi
  - player
  - design
dependencies:
  - task-017.02
  - task-017.03
parent_task_id: task-017
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Plan concrete changes in video.kino.pub to support TMDbHelper playback without TMDbHelper edits: ensure search route reliably accepts `title` param (non-interactive) and matching for movies/episodes works; add helper route only if needed for robustness. Must remain backward compatible.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Identify minimal code changes (if any) in video.kino.pub to guarantee `/search/<type>/results/?title=` works with TMDbHelper (e.g., parameter handling or matching tweaks) with file references
- [ ] #2 Define matching heuristic (title/year for movies; showname+season+episode for episodes) and confirm 1-based indices; document no external-id support
- [ ] #3 Outline behavior when multiple matches/none found and what user sees (fallback to search listing)
- [ ] #4 Produce short implementation notes (files to touch, caution on backward compatibility)
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Added installer route /install_tmdbhelper_player/ in video.kino.pub to copy player JSON into TMDbHelper userdata without touching TMDbHelper code. Updated testing docs with RunPlugin instructions.
<!-- SECTION:NOTES:END -->
