---
id: task-004
title: Write backlog/docs/user-guide/navigation.md
status: Done
assignee: []
created_date: '2025-12-14 12:06'
updated_date: '2025-12-14 12:16'
labels:
  - docs
dependencies: []
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Describe main menu entries and user flows using Plugin._main_menu_items in resources/lib/plugin.py and routes in resources/lib/main.py (search, fresh/hot/popular, collections, TV, bookmarks, watching, items/<type>).
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 backlog/docs/user-guide/navigation.md lists main menu items sourced from Plugin._main_menu_items
- [x] #2 Each menu entry notes the downstream routes/flows in resources/lib/main.py (search, fresh/hot/popular, collections, TV, bookmarks, watching, items/<type>)
- [x] #3 Doc includes brief usage examples or expected UI outcomes for key routes
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
docs/user-guide/navigation.md lists main menu items from Plugin._main_menu_items with routes and example flows (search, collections, bookmarks). Sources: plugin.py, main.py.
<!-- SECTION:NOTES:END -->
