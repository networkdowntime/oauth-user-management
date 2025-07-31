---
applyTo: "**"
---
# Project General Coding Standards

## 🏗️ Architecture Overview

This file serves as the root of our coding standards hierarchy. All language and framework-specific files inherit from these universal principles.

### 📋 Apply These Universal Standards to All Code:
- [Security & OWASP Guidelines](./security-owasp.instructions.md)
- [Self-Explanatory Code & Commenting](./tech-code-commenting.instructions.md)  
- [Performance Optimization](./tech-performance-optimization.instructions.md)

### 🌐 Language-Specific Standards:
- [Java Development](./tech-java.instructions.md) → [Spring Boot](./tech-springboot.instructions.md) | [Quarkus](./tech-quarkus.instructions.md)
- [JavaScript Development](./tech-javascript.instructions.md)
- [TypeScript Development](./tech-typescript.instructions.md) → [Angular](./tech-angular.instructions.md) | [React](./tech-reactjs.instructions.md)
- [Python Development](./tech-python.instructions.md)

## Priorities In Order
- **Security**: Always prioritize security best practices and OWASP guidelines.
- **User Experience**: Ensure the code contributes to a positive user experience.
- **Maintainability**: Write code that is easy to read, maintain, and extend.
- **Scalability**: Design code to handle growth in data and user load.
- **Testability**: Write code that is easy to test and debug.
- **Performance**: Optimize for performance without sacrificing maintainability, scalability, or readability.

## Naming Conventions
- Use clear, descriptive names that indicate purpose and scope
- Follow language-specific conventions:
  - **PascalCase**: Classes, interfaces, components, type aliases  
  - **camelCase**: Variables, functions, methods, properties
  - **ALL_CAPS**: Constants and environment variables
  - **kebab-case**: CSS classes, file names (when appropriate)
- Avoid cryptic abbreviations and single-letter variables (except for iterators)
- Use meaningful names over comments when possible

## Error Handling & Logging
- **Never ignore errors**: Always handle, log, or properly rethrow exceptions
- Use try/catch blocks for all error-prone operations (async, I/O, external calls)
- Implement proper error boundaries and centralized error handling
- **Logging Standards**:
  - Use structured logging with appropriate log levels (DEBUG, INFO, WARN, ERROR)
  - Include sufficient context in log messages for debugging, where possible include request IDs, user IDs, and timestamps to allow correlation of logs.
  - Use parameterized logging to avoid string concatenation
  - Don't log sensitive information (passwords, API keys, PII)
- **Custom Error Classes**: Create specific error types for different failure scenarios
- **Graceful Degradation**: Provide fallback behavior when possible

## Input Validation & Data Handling
- **Validate all inputs**: Use appropriate validation frameworks and annotations
- **Sanitize user data**: Prevent injection attacks and data corruption
- **Handle null/undefined safely**: Use optional chaining, null checks, or Optional types
- **Implement comprehensive validation**: Check data types, ranges, formats, and business rules
- **Provide meaningful error messages**: Help users understand validation failures

## Configuration & Environment Management
- **Never hardcode configuration**: Use environment variables, configuration files, or configuration management services
- **Externalize secrets**: Use secure secret management (environment variables, secret stores)
- **Support multiple environments**: Ensure configuration works across dev, staging, production
- **Make applications locally runnable**: Developers should run code without modifying the codebase
- **Document configuration requirements**: List all required environment variables and settings

## Configurations
- Connections to external services (e.g., databases, APIs) should be configurable via environment variables or configuration files.
- The developer should be able to run the code locally without needing to modify the codebase.
- When deploying containers, the configuration should be flexible to allow for different environments (development, staging, production) without code changes.

## Dependencies
- Use well-maintained libraries and frameworks.
- Avoid unnecessary dependencies to keep the project lightweight.
- Use the latest stable versions of libraries, but ensure compatibility with the project.
- Use the latest stable version of the programming language and framework.

## Network Ports
- Use standard ports for services (e.g., 80 for HTTP, 443 for HTTPS) when deploying containers.
- For local development, use ports that do not conflict with common services (e.g., 3000, 8080).
- Ensure that when running complex environments locally (e.g., microservices), the port mappings are well-documented and do not overlap.

## Programming Style
- When writing functions or methods:
    - Ensure they are small and focused on a single task.
    - Where possible, prefer functions that return values over those that modify state as they are easier to test and reason about.

## Documentation & Comments
- **Write clear documentation**: Document public APIs, complex algorithms, and business logic
- **Use appropriate comment levels**: Follow language-specific documentation standards (JSDoc, Javadoc, etc.)
- **Document design decisions**: Explain WHY certain approaches were chosen in project level docs/adr/adr-{system-name-decision-name-id}.md files.  For polyrepo projects, use a consistent format across all repos. For monorepo projects, use the root monorepo's docs/adr directory.
- **Keep documentation current**: Update documentation when code changes
- **Prefer self-documenting code**: Use meaningful names and clear structure over excessive commenting

## Testing
- **Write comprehensive unit tests**: Test all critical functionality with high coverage (aim for 90%+ code & branch coverage)
- **Use appropriate testing frameworks**: Choose well-established testing tools for your language/framework
- **Mock external dependencies**: Isolate tests from databases, APIs, and other external services
- **Test both happy paths and edge cases**: Include error scenarios, boundary conditions, and invalid inputs
- **Ensure tests are fast and reliable**: Tests should run quickly and consistently
- **Use descriptive test names**: Test names should clearly describe what is being tested
- **Follow testing patterns**: Use Arrange-Act-Assert (AAA) or similar structured approaches
- **Include integration tests**: Test component interactions and end-to-end workflows
- **Maintain test independence**: Tests should be able to run in any order without affecting each other

## Code Organization & Architecture
- **Separate concerns**: Keep business logic, data access, and presentation layers distinct  
- **Use appropriate design patterns**: Apply established patterns for common problems
- **Organize by feature/domain**: Group related functionality together rather than by technical layer
- **Keep functions/methods small**: Focus on single responsibilities and clear interfaces
- **Prefer composition over inheritance**: Use dependency injection and composition for flexibility
- **Implement proper abstraction**: Hide implementation details behind clear interfaces
- **Use consistent project structure**: Follow established conventions for your language/framework

## Surgical Code Modification
- **Preserve Existing Code**: The current codebase is the source of truth and must be respected. Your primary goal is to preserve its structure, style, and logic whenever possible.
- **Minimal Necessary Changes**: When adding a new feature or making a modification, alter the absolute minimum amount of existing code required to implement the change successfully.
- **Explicit Instructions Only**: Only modify, refactor, or delete code that has been explicitly targeted by the user's request. Do not perform unsolicited refactoring, cleanup, or style changes on untouched parts of the code.
- **Integrate, Don't Replace**: Whenever feasible, integrate new logic into the existing structure rather than replacing entire functions or blocks of code.

## Workflow
- Critically plan out features and changes before starting development.
- Break down large tasks into smaller, manageable pieces.
- Changes should be small, incremental, tested, and where possible non-breaking to reduce risk.
- Run tests frequently to catch issues early.  Ideally, implement an appropriate test to validate each code change.
- Use version control effectively, with clear commit messages and branching strategies.
- Regularly review and refactor code to improve system architecture, readability, and maintainability.
