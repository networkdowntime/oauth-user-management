---
description: Systematic implementation task execution workflow as the final phase of spec-driven development
applyTo: "**/*.{js,ts,py,java,go,rs,rb,php,cs,kt,swift,c,cpp,h,hpp,scala,clj,ex,erl,hs,ml,fs,dart,lua,r,jl,nim,zig}"
---

# Implementation Task Execution Workflow

## Overview

This workflow provides a systematic approach to executing numbered implementation tasks ([NNNN]-[task-name].md) generated from System Requirements Documents (SRDs). This is the **final phase** of spec-driven development where specifications become working code.

**Position in Spec-Driven Flow**: BRD → PRDs with User Stories → System Architecture (with ADRs) → SRDs → **Implementation Tasks** → **Code Implementation**

## Core Principles

### Sequential Task Execution

- **Execute one task at a time** - Complete current task fully before starting the next
- **Follow dependency order** - Respect prerequisite tasks defined in task files
- **Seek confirmation** - Request user approval before starting each new task
- **Wait for explicit approval** - User must respond "yes", "y", "continue", or equivalent

### Quality-First Implementation

- **Meet acceptance criteria** - Every acceptance criteria checkbox must be validated
- **Maintain traceability** - Reference SRD requirements and PRD user stories in code
- **Follow architectural decisions** - Implement according to ADRs and system architecture
- **Test comprehensively** - Validate functionality at unit, integration, and system levels

### Documentation and Progress Tracking

- **Update task status immediately** - Mark tasks as completed `[x]` when finished
- **Document file changes** - Maintain accurate record of modified files
- **Commit with context** - Reference task numbers and SRD sections in commit messages
- **Maintain living documentation** - Update README, API docs, and inline comments

## Implementation Protocol

### Step 1: Task Preparation and Context Setting

1. **Read the complete task file** (`[NNNN]-[task-name].md`)
   - Understand the objective and context
   - Review acceptance criteria and technical requirements
   - Identify file changes and database modifications needed
   - Note testing requirements and dependencies

2. **Validate prerequisites**
   - Confirm all prerequisite tasks are completed
   - Verify development environment is properly configured
   - Ensure required dependencies are installed and accessible
   - Check that database schema and external services are available

3. **Review related documentation**
   - **SRD section**: Understand detailed system requirements
   - **PRD user stories**: Understand business context and user value
   - **ADRs**: Review architectural decisions that impact implementation
   - **Existing codebase**: Understand current patterns and conventions

4. **Request user confirmation**
   ```
   Ready to implement Task [NNNN]: [Task Title]
   
   This task will:
   - [Brief description of what will be implemented]
   - [Expected file changes]
   - [Testing approach]
   
   Estimated duration: [X] hours
   
   Should I proceed? (yes/y to continue)
   ```

### Step 2: Implementation Execution

1. **Plan the implementation approach**
   - Break down the task into logical code changes
   - Identify the order of file modifications
   - Plan testing strategy (unit tests first, then integration)
   - Consider error handling and edge cases

2. **Implement following best practices**
   - **Write tests first** (when using TDD approach)
   - **Implement in small increments** with frequent testing
   - **Follow coding standards** defined in language-specific instruction files
   - **Add meaningful comments** explaining business logic and complex decisions
   - **Handle errors gracefully** with appropriate error messages and logging

3. **Validate each acceptance criteria**
   - **Test functionality** against each acceptance criteria checkbox
   - **Verify integration points** work as expected
   - **Check performance requirements** if specified in the task
   - **Validate security considerations** (authentication, authorization, data protection)

### Step 3: Quality Assurance and Testing

1. **Execute comprehensive testing**
   ```bash
   # Language-specific examples
   npm test              # Node.js/JavaScript
   pytest                # Python
   mvn test              # Java/Maven
   cargo test            # Rust
   go test ./...         # Go
   dotnet test           # .NET/C#
   ```

2. **Perform manual validation**
   - Test user workflows defined in related PRD user stories
   - Verify edge cases and error conditions
   - Check integration with external systems
   - Validate data persistence and retrieval

3. **Code quality checks**
   - Run linting tools and fix any issues
   - Check code coverage and aim for targets defined in SRD
   - Review code against architectural patterns defined in ADRs
   - Ensure no regression in existing functionality

### Step 4: Documentation and Commit

1. **Update inline documentation**
   - Add/update comments explaining business logic
   - Update function/method documentation
   - Add usage examples for complex functionality

2. **Update project documentation**
   - Update README if new setup steps are required
   - Update API documentation for new endpoints
   - Update database schema documentation for changes

3. **Commit with proper context**
   ```bash
   git add .
   git commit -m "Implement Task [NNNN]: [brief description]
   
   - [Specific implementation details]
   - [Reference to SRD section]
   - [Related PRD user story]
   
   Closes: [NNNN]-[task-name].md"
   ```

### Step 5: Task Completion and Handoff

1. **Mark task as completed**
   - Update the task file: mark all acceptance criteria as `[x]`
   - Update any task tracking systems or boards
   - Note any deviations from original plan and rationale

2. **Validate Definition of Done**
   - [ ] All acceptance criteria met
   - [ ] All tests passing (unit and integration)
   - [ ] Code reviewed (if team workflow requires)
   - [ ] Documentation updated
   - [ ] No regression in existing functionality
   - [ ] Proper error handling implemented
   - [ ] Security considerations addressed

3. **Prepare for next task**
   - Review upcoming tasks that are now unblocked
   - Identify any new dependencies that emerged during implementation
   - Update task dependencies if implementation revealed new requirements
## Error Handling and Troubleshooting

### Common Implementation Challenges

1. **Unclear Requirements**
   - **Action**: Review related SRD section and PRD user story for clarification
   - **Escalation**: If still unclear, document specific questions and request clarification

2. **Technical Blockers**
   - **Action**: Review relevant ADRs for architectural guidance
   - **Fallback**: Implement temporary solution with clear technical debt documentation
   - **Escalation**: For complex blockers, create new ADR or seek architectural review

3. **Test Failures**
   - **Action**: Debug systematically, starting with unit tests, then integration tests
   - **Documentation**: Record root cause and resolution for future reference

4. **Performance Issues**
   - **Action**: Profile the implementation and compare against SRD performance requirements
   - **Optimization**: Apply performance patterns defined in system architecture

### Recovery Procedures

1. **If implementation deviates from acceptance criteria**:
   - Roll back to last working state
   - Re-analyze task requirements
   - Plan alternative implementation approach
   - Document lessons learned

2. **If tests consistently fail**:
   - Review test setup and dependencies
   - Verify database state and external service availability
   - Check for environment-specific configuration issues

## Integration with Spec-Driven Development

### Traceability Maintenance

- **Every code change** should trace back to specific SRD requirements
- **Business logic** should reference relevant PRD user stories in comments
- **Architectural patterns** should follow decisions documented in ADRs
- **Error handling** should align with system-wide error handling strategies

### Quality Gates

Before marking any task complete:

1. **Requirements Validation**: Feature meets all acceptance criteria
2. **Architecture Compliance**: Implementation follows established patterns and ADRs
3. **User Story Fulfillment**: Feature enables the user workflows defined in PRDs
4. **System Integration**: Feature works correctly with other system components
5. **Performance Compliance**: Feature meets non-functional requirements from SRD

### Continuous Improvement

- **Capture Implementation Insights**: Document any discoveries that impact future tasks
- **Update Architectural Decisions**: If implementation reveals need for architectural changes
- **Refine Task Estimates**: Track actual vs. estimated time for better future planning
- **Enhance Documentation**: Update SRDs and PRDs based on implementation learnings

## Best Practices Summary

### Code Quality
- **Follow established patterns**: Use architectural patterns defined in ADRs
- **Maintain consistency**: Follow coding standards from language-specific instruction files
- **Write self-documenting code**: Clear variable names and function signatures
- **Add contextual comments**: Explain business logic and complex algorithms

### Testing Strategy
- **Test at multiple levels**: Unit tests for individual functions, integration tests for workflows
- **Cover edge cases**: Test boundary conditions and error scenarios
- **Performance testing**: Validate against requirements defined in SRD
- **User acceptance testing**: Validate against PRD user stories

### Documentation
- **Keep it current**: Update documentation as implementation progresses
- **Maintain traceability**: Link code back to requirements documents
- **Document decisions**: Record any implementation choices and their rationale
- **Update APIs**: Keep API documentation synchronized with implementation

This systematic approach ensures that implementation tasks maintain full traceability from business requirements to working code while maintaining high quality standards throughout the spec-driven development process.

```markdown
- [x] **T001: Completed Task**
  - [x] Completed sub-task 1
  - [x] Completed sub-task 2
  
- [ ] **T002: In Progress Task**
  - [x] Completed sub-task 1
  - [ ] Current sub-task 2
  - [ ] Pending sub-task 3
```

### Relevant Files Section

Maintain an up-to-date list of all files created or modified:

```markdown
## Relevant Files
- `src/components/LoginForm.jsx` - User authentication form with validation
- `src/utils/validation.js` - Input validation helper functions
- `src/services/authService.js` - Authentication API calls
- `tests/auth.test.js` - Unit tests for authentication logic
```

## GitHub Copilot Integration

### Effective Prompting

1. **Context Setting**: Reference the current task and PRD section
2. **Specific Requests**: Ask for precise implementations
3. **Code Review**: Request validation against requirements
4. **Testing**: Generate appropriate test cases

### Example Prompts

```javascript
// Context setting
"Based on task T005 in the PRD, I need to implement user authentication..."

// Specific implementation
"Generate a login endpoint that validates email/password and returns JWT token"

// Code review
"Review this authentication middleware against the PRD security requirements"

// Testing
"Create unit tests for the login function covering success and error cases"
```

## Quality Assurance

### Before Marking Tasks Complete

- [ ] Functionality works as specified in PRD
- [ ] All edge cases are handled
- [ ] Error handling is implemented
- [ ] Code follows project conventions
- [ ] Tests are written and passing
- [ ] Documentation is updated

### Testing Strategy

1. **Unit Tests** - Test individual functions and components
2. **Integration Tests** - Test component interactions
3. **End-to-End Tests** - Test complete user workflows
4. **Manual Testing** - Verify UI/UX works as expected

## Common Execution Patterns

### Frontend Task Execution

1. Create component structure
2. Implement functionality
3. Add styling and responsive design
4. Handle user interactions and state
5. Add error handling
6. Write tests
7. Update documentation

### Backend Task Execution

1. Define API endpoints
2. Implement business logic
3. Add data validation
4. Handle errors and edge cases
5. Write unit tests
6. Test API endpoints
7. Update API documentation

### Database Task Execution

1. Design schema changes
2. Create migration scripts
3. Update models/entities
4. Test migrations
5. Verify data integrity
6. Update data access layer
7. Document schema changes

## Error Handling and Troubleshooting

### When Tests Fail

1. **Do not commit** - Fix issues before staging changes
2. **Debug systematically** - Isolate the problem
3. **Check dependencies** - Ensure all requirements are met
4. **Review PRD** - Verify implementation matches requirements
5. **Ask for help** - Request user guidance if stuck

### When Tasks Are Blocked

1. **Identify blocker** - Document what's preventing progress
2. **Communicate clearly** - Explain the issue to user
3. **Propose solutions** - Suggest alternatives or workarounds
4. **Update task list** - Mark dependencies that need resolution

## Best Practices

### Code Quality

- Follow existing code style and conventions
- Write self-documenting code with clear variable names
- Add appropriate error handling
- Include helpful code comments for complex logic
- Keep functions small and focused

### Git Practices

- Make atomic commits (one logical change per commit)
- Write clear, descriptive commit messages
- Test before committing
- Keep commit history clean and meaningful

### Documentation

- Update README files as needed
- Document API changes
- Add inline code documentation
- Keep architecture decisions recorded

### Communication

- Ask for clarification when requirements are unclear
- Provide regular progress updates
- Explain implementation decisions
- Request feedback on complex implementations

## Workflow Integration

This task execution workflow integrates with:

- **PRD Creation**: Reference PRD sections during implementation
- **Task Generation**: Follow task breakdown and dependencies
- **Code Review**: Validate implementations against PRD requirements
- **Testing**: Execute comprehensive testing strategy
- **Deployment**: Prepare code for production deployment