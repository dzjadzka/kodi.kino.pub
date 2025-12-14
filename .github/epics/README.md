# Epics Directory

This directory contains epic-level planning documents for major initiatives in the kodi.kino.pub project.

## Purpose

Epics are large bodies of work that can be broken down into smaller, manageable tasks. Each epic represents a significant feature, refactoring, or project phase that requires coordination across multiple tasks and potentially multiple sprints.

## Naming Convention

Epic files follow the naming pattern:
```
{number}-{short-descriptive-name}.md
```

Examples:
- `001-full-reverse-engineering.md`
- `002-clean-rewrite-implementation.md`
- `003-migration-strategy.md`

## Epic Structure

Each epic document should include:

### Required Sections
- **Epic ID**: Unique identifier (e.g., EPIC-001)
- **Epic Description**: Clear summary of what the epic aims to achieve
- **Epic Goal**: Specific, measurable outcome
- **Business Value**: Why this work matters
- **Epic Priority**: P0 (Critical), P1 (High), P2 (Medium), P3 (Low)
- **Tasks**: Breakdown of work into tasks with:
  - Priority
  - Estimated Effort
  - Dependencies
  - Goal
  - Steps
  - Acceptance Criteria
  - Output/Deliverables
- **Definition of Done (DoD)**: Clear criteria for epic completion
- **Risks and Blockers**: Known issues and mitigation strategies

### Optional Sections
- **Need Decision**: Items requiring stakeholder input
- **Dependencies**: External and internal dependencies
- **Notes**: Additional context, out of scope items, success metrics
- **Epic Owner**: Person responsible for the epic
- **Created/Updated**: Timestamps
- **Status**: Current epic status

## Task Formatting

Tasks within epics should follow this format:

```markdown
#### Task X.Y: Task Name
**Priority:** P0-P3  
**Estimated Effort:** X-Y hours  
**Dependencies:** Task references

**Goal:**  
Clear statement of what this task achieves.

**Steps:**
1. Step 1
2. Step 2
...

**Acceptance Criteria:**
- [ ] Criterion 1
- [ ] Criterion 2
...

**Output:** Deliverable description
```

## Priority Levels

- **P0 (Critical)**: Blocking work, must be completed first
- **P1 (High)**: Important work, should be completed soon
- **P2 (Medium)**: Useful work, can be scheduled flexibly
- **P3 (Low)**: Nice-to-have, can be deferred

## Status Values

- **DRAFT**: Epic is being written
- **READY FOR REVIEW**: Epic is complete and awaiting review
- **IN PROGRESS**: Epic work has started
- **BLOCKED**: Epic cannot proceed due to dependencies
- **COMPLETED**: All tasks and DoD criteria met
- **CANCELLED**: Epic work abandoned

## Creating a New Epic

1. Create a new file in this directory following the naming convention
2. Copy the structure from an existing epic as a template
3. Fill in all required sections
4. Set status to DRAFT
5. Request review when ready
6. Update status to READY FOR REVIEW
7. Begin work only after review and approval

## Related Documentation

- Task-level issues can be created in GitHub Issues referencing the epic
- Implementation documentation should go in `.github/docs/`
- Architecture Decision Records (ADRs) should reference relevant epics

## Questions?

For questions about epic planning or structure, please open a discussion in GitHub Discussions or contact the project maintainers.
