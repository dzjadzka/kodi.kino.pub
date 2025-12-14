---
id: task-017
title: 'EPIC: TMDbHelper Player integration for video.kino.pub'
status: Done
assignee: []
created_date: '2025-12-14 12:45'
updated_date: '2025-12-14 16:57'
labels:
  - kodi
  - tmdbhelper
  - player
  - epic
dependencies: []
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Enable TMDbHelper to use video.kino.pub as a Player for movie/episode playback. Scope: define contract between TMDbHelper player JSON and video.kino.pub routes, add resolver/search capabilities in video.kino.pub if needed, and supply a player JSON for TMDbHelper. Out of scope: broader TMDbHelper features unrelated to player integration. Phases: Discovery → Contract → Implementation → QA → Docs.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Contract documented for TMDbHelper -> video.kino.pub Player covering movies and episodes
- [ ] #2 Approved player JSON specification exists for TMDbHelper including assert/steps/is_resolvable
- [ ] #3 Resolver/search approach for video.kino.pub defined (including external-id mapping strategy)
- [ ] #4 Risks/limitations and fallbacks captured with mitigation plan
- [ ] #5 Implementation/test/docs tasks identified and linked
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
17:34 log confirms kino_pub player now auto-resolves episodes without opening folders after adding explicit return step in TMDbHelper player JSON.
<!-- SECTION:NOTES:END -->
