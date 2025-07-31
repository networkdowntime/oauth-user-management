---
description: Convert System Requirements Documents (SRDs) into numbered implementation tasks as part of spec-driven development
applyTo: "**/tasks/**/*.md,**/**/[0-9][0-9][0-9][0-9]-*.md"
---

# Implementation Task Generation Workflow

## Overview

This workflow converts **System Requirements Documents (SRDs)** into actionable, numbered implementation tasks following the spec-driven development methodology. Tasks are the final step in the documentation chain before actual coding begins.

**Position in Spec-Driven Flow**: BRD → PRDs with User Stories → System Architecture (with ADRs) → SRDs → **Implementation Tasks**

## Prerequisites

Before generating implementation tasks, ensure you have:
- ✅ **System Requirements Document (SRD)** for the target system
- ✅ **Approved System Architecture** with relevant ADRs
- ✅ **PRD User Stories** that define business requirements
- ✅ **Development environment** and technology stack decisions finalized

## Process

### Step 1: SRD Analysis and Task Planning

1. **Read and analyze the complete SRD** to understand:
   - System boundaries and responsibilities
   - Functional requirements and business logic
   - Non-functional requirements (performance, security, etc.)
   - Integration points and external dependencies
   - Database schema and data models

2. **Review related PRD user stories** to understand:
   - User workflows and acceptance criteria
   - Business context and priorities
   - End-to-end feature requirements

3. **Consult system architecture and ADRs** to understand:
   - Technology stack and framework decisions
   - Integration patterns and communication protocols
   - Security and performance architectural patterns

### Step 2: Task Decomposition Strategy

Break down the SRD into logical implementation phases:

#### Core Implementation Categories

- **Infrastructure & Setup**: Environment setup, configuration, dependencies
- **Data Layer**: Database schema, migrations, data access objects
- **Core Business Logic**: Domain models, business rules, algorithms
- **Service Layer**: Application services, business orchestration
- **Integration Layer**: External APIs, message queues, event handling
- **Presentation Layer**: Controllers, API endpoints, user interfaces
- **Security Implementation**: Authentication, authorization, data protection
- **Testing & Validation**: Unit tests, integration tests, end-to-end tests
- **Documentation & Deployment**: Code documentation, deployment scripts

#### Task Granularity Guidelines

- **Scope**: Each task should be completable in 2-6 hours by a competent developer
- **Atomicity**: Tasks should have single, clear outcomes
- **Dependencies**: Clear prerequisite tasks and blocking relationships
- **Testability**: Each task should produce verifiable, testable results
- **Traceability**: Tasks should map back to specific SRD requirements and PRD user stories

### Step 3: Task Numbering and Organization

Use **sequential numbering** with descriptive names:

**Format**: `[NNNN]-[short-task-name].md`

**Numbering Strategy**:
- Start with `0001` for the first task
- Use increments of 1 for each subsequent task
- Leave gaps (e.g., 0010, 0020) for major phases to allow insertion of new tasks
- Number tasks in **dependency order** when possible

**Examples**:
```
0001-setup-project-structure.md
0002-configure-database-connection.md
0003-create-user-entity-model.md
0010-implement-user-repository.md
0011-implement-authentication-service.md
0020-create-login-api-endpoint.md
0021-create-user-registration-endpoint.md
```
### Step 4: Individual Task File Structure

Each task file should follow this **standardized template**:

```markdown
# Task [NNNN]: [Task Title]

## Context
**Related SRD**: `srd-[system-name].md` (section X.X)
**Related PRD User Story**: [Story title from PRD]
**System**: [system-name]
**Component**: [specific component or layer]

## Objective
[Clear, one-sentence description of what this task accomplishes]

## Acceptance Criteria
- [ ] Specific, testable condition 1
- [ ] Specific, testable condition 2
- [ ] Specific, testable condition 3

## Technical Requirements
### Implementation Details
- [Specific technical approaches or patterns to use]
- [Framework-specific considerations]
- [Integration points or dependencies]

### File Changes Expected
- `path/to/file1.ext` - [what changes are expected]
- `path/to/file2.ext` - [what changes are expected]

### Database Changes (if applicable)
- [Migration scripts needed]
- [Schema changes required]

## Testing Requirements
- [ ] Unit tests for [specific functionality]
- [ ] Integration tests for [specific interactions]
- [ ] Manual testing steps (if applicable)

## Dependencies
**Prerequisite Tasks**: 
- [ ] Task [NNNN]: [task name]
- [ ] Task [NNNN]: [task name]

**Blocking Tasks** (tasks that depend on this one):
- Task [NNNN]: [task name]

## Definition of Done
- [ ] Code implemented according to acceptance criteria
- [ ] All tests passing (unit and integration)
- [ ] Code reviewed (if team workflow requires)
- [ ] Documentation updated (inline comments, README changes)
- [ ] No regression in existing functionality

## Notes
[Any additional context, gotchas, or considerations for the implementer]
```

### Step 5: Task File Management and Quality Assurance

#### Directory Structure
**Monorepo**:
```
services/[system-name]/tasks/
├── 0001-setup-project-structure.md
├── 0002-configure-database-connection.md
└── 0003-create-user-entity-model.md
```

**Polyrepo** (within each system repository):
```
[system-name]/tasks/
├── 0001-setup-project-structure.md
├── 0002-configure-database-connection.md
└── 0003-create-user-entity-model.md
```

#### Quality Validation Checklist
Before finalizing task generation:

- [ ] **Completeness**: All SRD requirements have corresponding tasks
- [ ] **Granularity**: No task is too large (>6 hours) or too small (<1 hour)
- [ ] **Dependencies**: Task dependencies are clearly mapped and achievable
- [ ] **Testability**: Each task has clear acceptance criteria and testing approach
- [ ] **Traceability**: Tasks clearly link back to SRD requirements and PRD user stories

## Integration with Development Workflow

### Developer Handoff Process
1. **Context Setting**: Each task provides sufficient context for autonomous implementation
2. **Clear Outcomes**: Acceptance criteria define exactly what "done" means
3. **Quality Gates**: Built-in validation ensures quality standards are met
4. **Progress Tracking**: Checkbox format enables clear progress monitoring

### Continuous Improvement
- **Feedback Collection**: Capture lessons learned during task execution
- **Template Refinement**: Update task templates based on development team feedback
- **Estimation Accuracy**: Track actual vs. estimated task completion times
- **Dependency Optimization**: Refine task dependencies based on actual development flow

This task generation approach ensures smooth transition from system requirements to actual code implementation while maintaining full traceability through the spec-driven development process.
- Check for proper error handling

### Dependency Management

- Identify all task dependencies
- Order tasks logically
- Flag potential blocking issues
- Plan for parallel development where possible

## File Management

### Task List Storage

- Save as `task-list-[feature-name].md` in `/tasks` directory
- Keep task list version controlled
- Update progress regularly
- Archive completed task lists

### Progress Tracking

- Update task status as work progresses
- Add notes about implementation decisions
- Track time spent on each task
- Document any deviations from original plan

## Common Task Patterns

### Frontend Tasks

- Component creation and styling
- State management implementation
- API integration
- User interaction handling
- Responsive design implementation

### Backend Tasks

- API endpoint creation
- Database operations
- Business logic implementation
- Authentication and authorization
- Error handling and validation

### Testing Tasks

- Unit test creation
- Integration test setup
- End-to-end test scenarios
- Performance testing
- Security testing

### DevOps Tasks

- CI/CD pipeline setup
- Deployment configuration
- Monitoring and logging
- Database migrations
- Environment configuration