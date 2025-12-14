---
id: task-013
title: Write backlog/docs/developer-guide/testing.md
status: Done
assignee: []
created_date: '2025-12-14 12:07'
updated_date: '2025-12-14 12:17'
labels:
  - docs
dependencies: []
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Document testing approach covering pytest harness, podman-based Kodi + mockserver setup, expected_results fixtures, and proxy coverage based on tests/conftest.py, tests/helpers.py, tests/test_proxy.py.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 backlog/docs/developer-guide/testing.md explains how to run tests with pytest and required env/deps
- [ ] #2 Describes podman-based Kodi + mockserver setup from tests/conftest.py/helpers.py and how fixtures/expected_results are used
- [ ] #3 Includes notes on proxy coverage in tests/test_proxy.py and how to extend tests safely
<!-- AC:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
docs/developer-guide/testing.md documents pytest targets, podman-based Kodi+mockserver setup, fixtures/helpers, and proxy coverage in tests/test_proxy.py with references.
<!-- SECTION:NOTES:END -->
