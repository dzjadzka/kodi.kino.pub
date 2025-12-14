---
id: task-011
title: Write backlog/docs/developer-guide/architecture.md
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
Outline addon entrypoint, routing system, plugin orchestration, models/entities, and helpers using src/addon.py, resources/lib/routing.py, resources/lib/plugin.py, resources/lib/modeling.py, and helper modules.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 backlog/docs/developer-guide/architecture.md describes entrypoint flow from src/addon.py into routing/plugin stack
- [x] #2 Explains routing system (resources/lib/routing.py) and how Plugin orchestrates routes/actions (resources/lib/plugin.py)
- [x] #3 Summarizes key models/entities (resources/lib/modeling.py) and helper modules (utils, listitem, logger) with relationships
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
docs/developer-guide/architecture.md outlines entrypoint (addon.py), routing, plugin orchestration, models/listitems, and helper modules (auth, client, search_history, settings, player, logger, xbmc_settings).
<!-- SECTION:NOTES:END -->
