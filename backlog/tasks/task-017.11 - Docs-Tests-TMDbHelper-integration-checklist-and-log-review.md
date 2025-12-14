---
id: task-017.11
title: 'Docs/Tests: TMDbHelper integration checklist and log review'
status: Done
assignee: []
created_date: '2025-12-14 15:05'
updated_date: '2025-12-14 15:06'
labels:
  - kodi
  - tmdbhelper
  - player
  - testing
  - docs
dependencies:
  - task-017.07
parent_task_id: task-017
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Add testing checklist and log review guidance for TMDbHelper ↔ video.kino.pub player integration (movies and episodes) including ambiguous titles and localization cases.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 Checklist document added/updated covering movies and episodes, localized titles, ambiguous matches, season/episode >1
- [x] #2 Instructions include player JSON installation path and what to look for in kodi.log (routes, setResolvedUrl, match steps)
- [x] #3 Linked from doc-001 notes and tasks for future validation
- [x] #4 No open questions; ready for manual verification runs
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Added docs/tmdbhelper-integration-testing.md with install instructions for player JSON, manual checklist (movies/episodes, localized/ambiguous titles, season/episode >1), and log review guidance. Referenced in doc-001 Next steps.
<!-- SECTION:NOTES:END -->
