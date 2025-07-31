---
description: Core Java development standards and best practices for all Java frameworks
applyTo: "**/*.java"
---

# Java Development Standards

## 🏗️ Architecture & Navigation
- **Root Standards**: [General Coding Standards](./tech-general-coding.instructions.md)
- **Security Guidelines**: [Security & OWASP](./security-owasp.instructions.md)
- **Performance Guidelines**: [Performance Optimization](./tech-performance-optimization.instructions.md)
- **Framework Extensions**: [Spring Boot](./tech-springboot.instructions.md) | [Quarkus](./tech-quarkus.instructions.md)

---

## ☕ Java-Specific Context

- **Java Version**: 17+ LTS (prefer 21+ for new projects)
- **Code Style**: Google Java Style Guide, Oracle Code Conventions
- **Build Tools**: Maven (preferred), Gradle
- **Architecture Patterns**: Layered, Hexagonal, Clean Architecture, Microservices
- **Common Frameworks**: Spring Boot, Quarkus, Jakarta EE

## 🔧 Java Language Standards

### Code Quality & Modern Java Features
- **Java Version**: Use Java 17+ features (records, sealed classes, pattern matching, text blocks)
- **Access Modifiers**: Use appropriate access levels (`private` by default, minimize `public`)
- **Immutability**: Prefer `final` for variables, use immutable objects when possible
- **Null Safety**: Use `Optional<T>` for potentially null return values, avoid returning null
- **Resource Management**: Always use try-with-resources for automatic resource cleanup

### Object-Oriented Design
- **SOLID Principles**: Apply Single Responsibility, Open/Closed, Liskov Substitution, Interface Segregation, Dependency Inversion
- **Design Patterns**: Use appropriate patterns (Factory, Builder, Strategy, Observer) when they solve real problems
- **Composition over Inheritance**: Prefer composition and interfaces over inheritance hierarchies
- **Encapsulation**: Keep implementation details private, expose behavior through well-defined interfaces

### Collections & Streams
- **Collections Framework**: Use appropriate collection types (List, Set, Map) based on use case
- **Stream API**: Leverage streams for data processing, avoid excessive intermediate operations
- **Immutable Collections**: Use `List.of()`, `Set.of()`, `Map.of()` for immutable collections
- **Performance**: Be aware of collection performance characteristics (ArrayList vs LinkedList)

### Exception Handling
- **Checked vs Unchecked**: Use checked exceptions for recoverable errors, unchecked for programming errors
- **Custom Exceptions**: Create specific exception types for different error scenarios
- **Exception Hierarchy**: Organize exceptions in meaningful hierarchies
- **Resource Cleanup**: Ensure proper resource cleanup in finally blocks or try-with-resources

## 📁 Project Structure

```
src/
├── main/
│   ├── java/
│   │   └── com/company/project/
│   │       ├── Application.java           # Main application class
│   │       ├── config/                    # Configuration classes
│   │       │   ├── DatabaseConfig.java
│   │       │   └── SecurityConfig.java
│   │       ├── controller/                # REST controllers
│   │       │   ├── BaseController.java
│   │       │   └── UserController.java
│   │       ├── service/                   # Business logic
│   │       │   ├── UserService.java
│   │       │   └── impl/
│   │       │       └── UserServiceImpl.java
│   │       ├── repository/                # Data access layer
│   │       │   ├── UserRepository.java
│   │       │   └── impl/
│   │       │       └── UserRepositoryImpl.java
│   │       ├── model/                     # Domain models
│   │       │   ├── entity/                # JPA entities
│   │       │   ├── dto/                   # Data transfer objects
│   │       │   └── enums/                 # Enums
│   │       ├── exception/                 # Custom exceptions
│   │       │   ├── BusinessException.java
│   │       │   └── handler/
│   │       │       └── GlobalExceptionHandler.java
│   │       └── util/                      # Utility classes
│   │           ├── DateUtils.java
│   │           └── ValidationUtils.java
│   └── resources/
│       ├── application.yml                # Configuration files
│       ├── logback.xml                    # Logging configuration
│       └── static/                        # Static resources
└── test/
    ├── java/
    │   └── com/company/project/
    │       ├── integration/               # Integration tests
    │       ├── unit/                      # Unit tests
    │       └── TestApplication.java       # Test configuration
    └── resources/
        └── application-test.yml           # Test configuration
```

## 🧪 Java Testing Standards

### Testing Framework & Tools
- **Primary Framework**: JUnit 5 with Mockito for mocking
- **Integration Testing**: Spring Boot Test, TestContainers for database tests
- **Coverage**: JaCoCo with minimum 90% coverage requirement
- **API Testing**: RestAssured for REST API testing
- **Performance Testing**: JMeter, Gatling for load testing

### Test Organization
- **Test Structure**: Mirror source package structure in test directory
- **Test Naming**: `given_when_then` or `should_when_given` naming convention
- **Test Categories**: Unit (@Test), Integration (@SpringBootTest), End-to-End
- **Mock Strategy**: Mock external dependencies, use real objects for internal collaboration
- **Test Data**: Use builder pattern or test data factories for complex objects

### Best Practices
- **Test Independence**: Each test should be independent and repeatable
- **Assertions**: Use meaningful assertions with descriptive failure messages
- **Test Doubles**: Prefer mocks over stubs, avoid over-mocking
- **Test Coverage**: Focus on business logic, critical paths, and edge cases
- **Performance**: Keep tests fast, use parallel execution when possible

## 🚫 Java Anti-Patterns

### Code Smells to Avoid
- **God Classes**: Avoid classes with too many responsibilities
- **Primitive Obsession**: Use value objects instead of primitive types for domain concepts
- **String Constants**: Use enums or constants classes instead of magic strings
- **Null Checks Everywhere**: Use Optional and null-safe design patterns
- **Exception Swallowing**: Never catch and ignore exceptions without proper handling

### Common Mistakes
- **Improper equals/hashCode**: Always implement both methods consistently
- **Memory Leaks**: Be careful with static collections, listeners, and thread locals
- **Synchronization Issues**: Understand thread safety and use appropriate synchronization
- **Resource Leaks**: Always close streams, connections, and other resources
- **Performance Issues**: Avoid premature optimization, profile before optimizing

## 🎯 Java Best Practices

### Development Workflow
- **Code Quality Gates**: Use static analysis tools (SpotBugs, PMD, Checkstyle)
- **Documentation**: JavaDoc for all public APIs, meaningful method and class documentation
- **Dependency Management**: Keep dependencies up-to-date, manage transitive dependencies
- **Build Automation**: Use Maven or Gradle with proper plugin configuration
- **Code Review**: Focus on design, business logic, and maintainability

### Production Considerations
- **Logging**: Use SLF4J with Logback or Log4j2, structured logging for production
- **Monitoring**: JVM metrics, application metrics, health checks
- **Configuration**: Externalized configuration, environment-specific properties
- **Security**: Input validation, secure coding practices, dependency scanning
- **Performance**: JVM tuning, garbage collection optimization, profiling

## 📚 Reference Links

### Official Documentation
- [Oracle Java Documentation](https://docs.oracle.com/en/java/)
- [Oracle Code Conventions](https://www.oracle.com/java/technologies/javase/codeconventions-contents.html)
- [Google Java Style Guide](https://google.github.io/styleguide/javaguide.html)
- [Effective Java Best Practices](https://github.com/jbloch/effective-java-3e-source-code)

### Essential Tools & Libraries
- [Maven Documentation](https://maven.apache.org/guides/)
- [JUnit 5 Documentation](https://junit.org/junit5/docs/current/user-guide/)
- [Mockito Framework](https://javadoc.io/doc/org.mockito/mockito-core/latest/org/mockito/Mockito.html)
- [SLF4J Logging](http://www.slf4j.org/manual.html)
- [TestContainers](https://www.testcontainers.org/)
- Don't throw literals—always throw Error objects to preserve stack traces

### Documentation and Comments
- Write clear and concise comments for each class, method, and complex logic
- Use Javadoc for public APIs and methods to ensure clarity for consumers
- Document why certain design decisions were made, not just what the code does
- For libraries or external dependencies, mention their usage and purpose in comments

## Code Organization and Architecture

### Package Structure
- Organize code by feature/domain rather than by layer for better maintainability
- Use standard Java package naming conventions (com.company.project.feature)
- Separate concerns: keep business logic, data access, and presentation layers distinct
- Create utility classes as final with private constructors

### Dependency Management
- Use constructor injection for all required dependencies
- Declare dependency fields as `private final`
- Avoid field injection in favor of constructor injection
- Use dependency injection frameworks appropriately (CDI, Spring DI, etc.)

### Design Patterns
- Follow separation of concerns principles
- Use DTOs for data transfer between layers
- Avoid God classes or putting too much logic in single classes
- Organize code by feature/module rather than technical layers
- Implement proper abstraction and encapsulation

## Data Handling and Validation

### Input Validation
- Follow general validation guidelines in tech-general-coding.instructions.md
- Use Bean Validation (JSR-380) annotations (`@NotNull`, `@Size`, `@Valid`, etc.)
- Handle validation errors gracefully with meaningful error messages

### Database Access
- Always use parameterized queries to prevent SQL injection
- Use modern ORM frameworks (JPA, Hibernate) with proper entity mapping
- Implement proper transaction management
- Use named queries for complex database operations
- Implement proper pagination for list endpoints

## Logging and Monitoring

### Logging Standards
- Use SLF4J for all logging (`private static final Logger logger = LoggerFactory.getLogger(MyClass.class)`)
- Do not use concrete implementations (Logback, Log4j2) or `System.out.println()` directly
- Use parameterized logging: `logger.info("User {} logged in with role {}", userId, role)`
- Log at appropriate levels (DEBUG, INFO, WARN, ERROR)
- Include sufficient context in log messages for debugging

### Security Considerations
- Follow comprehensive security guidelines in security-owasp.instructions.md
- Use parameterized queries for all database operations
- Implement proper authentication and authorization patterns
- Don't hardcode secrets or sensitive configuration values
- Use environment variables or configuration management for secrets

## Core Java Best Practices

### ✅ Patterns to Follow

- Use constructor injection for dependency injection (framework-agnostic)
- Use DTOs for data transfer between application layers
- Validate inputs with Bean Validation annotations (`@NotNull`, `@Valid`, etc.)
- Handle exceptions with proper try-catch blocks and meaningful error messages
- Use SLF4J for logging with parameterized messages
- Organize code by feature/domain for better maintainability
- Write clear Javadoc for public classes and methods
- Use appropriate access modifiers and encapsulation principles

### 🚫 Patterns to Avoid

- Don't use field injection—prefer constructor injection for testability
- Avoid exposing internal entities directly—use DTOs for external interfaces
- Don't hardcode configuration values—use externalized configuration
- Avoid God classes or putting too much logic in single classes
- Don't catch and ignore exceptions—handle or rethrow them properly
- Avoid static utility classes except for pure helper functions

## Testing Standards

### Unit Testing
- Follow general testing guidelines in tech-general-coding.instructions.md
- Use JUnit 5 for unit testing with modern testing patterns
- Use Mockito for mocking external dependencies

## Testing Standards

### Unit Testing
- Use JUnit 5 for unit testing with modern testing patterns
- Use Mockito for mocking external dependencies
- Follow Arrange-Act-Assert (AAA) structure in tests
- Test validation, edge cases, and exception flows
- Mock external dependencies using appropriate mocking frameworks
- Ensure tests are independent and can run in any order

### Test Organization
- Organize tests to mirror the main source structure
- Use descriptive test method names that explain what is being tested
- Write tests that are maintainable and easy to understand
- Include integration tests for complex component interactions
- Test both happy path and error scenarios

### Build and Quality Assurance
- Ensure all tests pass as part of the build process
- Use build tools (Maven, Gradle) with proper test execution
- Run linting tools (Checkstyle, SpotBugs, PMD) for code quality
- Verify projects build successfully after code changes
- Implement continuous integration practices

## Anti-Patterns to Avoid

### Code Smells
- Don't use field injection—prefer constructor injection
- Avoid exposing entities directly to clients—use DTOs
- Don't hardcode configuration values—use externalized configuration
- Avoid static utility classes for anything other than pure helper functions
- Don't ignore exceptions—always handle or properly rethrow them

### Security Anti-Patterns
- Never hardcode secrets, passwords, or API keys in source code
- Don't use string concatenation for SQL queries—use parameterized queries
- Avoid exposing sensitive data in logs or error messages
- Don't skip input validation for any user-provided data

## Framework Integration
- For Spring Boot specific patterns, see tech-springboot.instructions.md
- For Quarkus specific patterns, see tech-quarkus.instructions.md
- Framework-specific annotations and patterns should be documented in their respective files
- This file covers language-level Java patterns that apply across all frameworks

## References

- [Java Language Specification](https://docs.oracle.com/javase/specs/)
- [Java Code Conventions (Oracle)](https://www.oracle.com/java/technologies/javase/codeconventions-contents.html)
- [Google Java Style Guide](https://google.github.io/styleguide/javaguide.html)
- [JUnit 5 Documentation](https://junit.org/junit5/docs/current/user-guide/)
- [Mockito Documentation](https://site.mockito.org/)
- [Bean Validation (Jakarta)](https://jakarta.ee/specifications/bean-validation/)
- [SLF4J Logging](http://www.slf4j.org/manual.html)
- [Effective Java by Joshua Bloch](https://www.oreilly.com/library/view/effective-java-3rd/9780134686097/)