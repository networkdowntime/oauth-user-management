---
description: Spring Boot development standards and framework-specific best practices
applyTo: "**/*.java"
---

# Spring Boot Development Standards

## 🏗️ Architecture & Navigation
- **Root Standards**: [General Coding Standards](./tech-general-coding.instructions.md)
- **Language Standards**: [Java Development](./tech-java.instructions.md)
- **Security Guidelines**: [Security & OWASP](./security-owasp.instructions.md)
- **Performance Guidelines**: [Performance Optimization](./tech-performance-optimization.instructions.md)
- **Related Frameworks**: [Quarkus](./tech-quarkus.instructions.md) (alternative Java framework)

---

## 🍃 Spring Boot-Specific Context

- **Spring Boot Version**: 3.x+ with Java 17+ for optimal performance
- **Spring Ecosystem**: Spring Framework 6.x, Spring Security, Spring Data
- **Configuration**: YAML preferred over properties, externalized configuration
- **Architecture Patterns**: Layered Architecture, Hexagonal, Clean Architecture
- **Cloud Native**: Spring Cloud, Spring Boot Actuator for production-ready features

## 🔧 Spring Boot Framework Standards

### Project Setup & Configuration
- **Dependencies**: Use Spring Boot starters for consistent dependency management
- **Configuration**: Use `application.yml` for externalized configuration over properties
- **Profiles**: Implement Spring profiles for environment-specific configurations (dev, test, prod)
- **Configuration Properties**: Use `@ConfigurationProperties` for type-safe configuration binding
- **External Configuration**: Use Spring Cloud Config or environment variables for secrets

### Dependency Injection & Bean Management
- **Constructor Injection**: Use constructor injection for all required dependencies (recommended)
- **Field Declaration**: Declare dependency fields as `private final` when using constructor injection
- **Annotation Usage**: Apply standard Spring annotations appropriately:
  - `@Service` for business logic services
  - `@Repository` for data access components
  - `@RestController` for REST endpoints
  - `@Component` for general-purpose beans
  - `@Configuration` for configuration classes
- **Conditional Beans**: Use `@Conditional` annotations for environment-specific bean creation
- **Bean Scopes**: Understand and use appropriate bean scopes (@Singleton, @RequestScope, @SessionScope)

### Spring Boot Architecture Patterns
- **Package Organization**: Organize by feature/domain following Spring Boot conventions
- **Controller Responsibilities**: Keep controllers thin—delegate business logic to service classes
- **Auto-Configuration**: Leverage Spring Boot's auto-configuration capabilities
- **Layer Separation**: Maintain clear separation between web, service, and data access layers
- **Exception Handling**: Implement global exception handling with `@ControllerAdvice`

### Spring Data & Database Integration
- **Repository Pattern**: Use Spring Data JPA repositories for standard data access patterns
- **Custom Repositories**: Implement custom repositories only when complex queries are needed
- **Transaction Management**: Use `@Transactional` on service methods, not repository methods
- **Database Migrations**: Use Flyway or Liquibase for database schema versioning
- **Connection Pooling**: Configure appropriate connection pooling (HikariCP) for production
- **Query Optimization**: Use `@Query` annotations for custom queries, avoid N+1 problems

### Spring Security Integration
- **Authentication**: Implement proper authentication mechanisms (JWT, OAuth2, Basic Auth)
- **Authorization**: Use method-level security with `@PreAuthorize` and `@PostAuthorize`
- **Security Configuration**: Configure security through `SecurityFilterChain` beans
- **CORS Configuration**: Properly configure CORS for cross-origin requests
- **Security Headers**: Implement security headers (CSP, HSTS, X-Frame-Options)

## 📁 Spring Boot Project Structure

```
src/
├── main/
│   ├── java/
│   │   └── com/company/project/
│   │       ├── ProjectApplication.java       # Main Spring Boot application class
│   │       ├── config/                       # Configuration classes
│   │       │   ├── DatabaseConfig.java
│   │       │   ├── SecurityConfig.java
│   │       │   ├── SwaggerConfig.java
│   │       │   └── WebConfig.java
│   │       ├── controller/                   # REST controllers
│   │       │   ├── advice/
│   │       │   │   └── GlobalExceptionHandler.java
│   │       │   ├── UserController.java
│   │       │   └── ProductController.java
│   │       ├── service/                      # Business logic services
│   │       │   ├── UserService.java
│   │       │   ├── ProductService.java
│   │       │   └── impl/
│   │       │       ├── UserServiceImpl.java
│   │       │       └── ProductServiceImpl.java
│   │       ├── repository/                   # Data repositories
│   │       │   ├── UserRepository.java
│   │       │   ├── ProductRepository.java
│   │       │   └── custom/
│   │       │       ├── UserRepositoryCustom.java
│   │       │       └── UserRepositoryImpl.java
│   │       ├── entity/                       # JPA entities
│   │       │   ├── BaseEntity.java
│   │       │   ├── User.java
│   │       │   └── Product.java
│   │       ├── dto/                          # Data Transfer Objects
│   │       │   ├── request/
│   │       │   │   ├── CreateUserRequest.java
│   │       │   │   └── UpdateUserRequest.java
│   │       │   └── response/
│   │       │       ├── UserResponse.java
│   │       │       └── ApiResponse.java
│   │       ├── security/                     # Security components
│   │       │   ├── JwtAuthenticationFilter.java
│   │       │   ├── UserDetailsServiceImpl.java
│   │       │   └── SecurityUtils.java
│   │       ├── exception/                    # Custom exceptions
│   │       │   ├── BusinessException.java
│   │       │   ├── ResourceNotFoundException.java
│   │       │   └── ValidationException.java
│   │       └── util/                         # Utility classes
│   │           ├── DateUtils.java
│   │           └── ValidationUtils.java
│   └── resources/
│       ├── application.yml                   # Main configuration
│       ├── application-dev.yml               # Development profile
│       ├── application-prod.yml              # Production profile
│       ├── application-test.yml              # Test profile
│       ├── logback-spring.xml               # Logging configuration
│       ├── db/migration/                    # Flyway migrations
│       │   ├── V1__Create_users_table.sql
│       │   └── V2__Create_products_table.sql
│       └── static/                          # Static web assets
└── test/
    ├── java/
    │   └── com/company/project/
    │       ├── ProjectApplicationTests.java
    │       ├── controller/                   # Controller tests
    │       │   ├── UserControllerTest.java
    │       │   └── integration/
    │       │       └── UserControllerIT.java
    │       ├── service/                      # Service tests
    │       │   └── UserServiceTest.java
    │       ├── repository/                   # Repository tests
    │       │   └── UserRepositoryTest.java
    │       └── config/                       # Test configuration
    │           └── TestConfig.java
    └── resources/
        ├── application-test.yml             # Test-specific configuration
        └── test-data.sql                    # Test data scripts
```

## 🧪 Spring Boot Testing Standards

### Testing Framework & Annotations
- **Spring Boot Test**: Use `@SpringBootTest` for integration tests
- **Test Slices**: Use test slices for focused testing:
  - `@WebMvcTest` for controller layer testing
  - `@DataJpaTest` for repository layer testing
  - `@JsonTest` for JSON serialization testing
  - `@MockBean` for mocking Spring beans
- **TestContainers**: Use TestContainers for database integration tests
- **Test Profiles**: Use `@ActiveProfiles("test")` for test-specific configuration

### Testing Best Practices
- **Test Categories**: Separate unit tests, integration tests, and end-to-end tests
- **Mock Strategy**: Mock external dependencies, use real Spring context for integration tests
- **Test Data**: Use `@Sql` annotations for test data setup, `@Transactional` for cleanup
- **Security Testing**: Test security configurations with `@WithMockUser` and `@WithUserDetails`
- **API Testing**: Use MockMvc for testing REST endpoints

## 🚫 Spring Boot Anti-Patterns

### Configuration Issues
- **Property Sprawl**: Hardcoding configuration values instead of using externalized configuration
- **Profile Misuse**: Creating too many profiles or using profiles incorrectly
- **Bean Definition**: Defining beans manually when auto-configuration would work
- **Component Scanning**: Over-broad component scanning affecting startup time
- **Circular Dependencies**: Creating circular bean dependencies

### Architecture Problems
- **Fat Controllers**: Putting business logic in controller methods
- **Service Layer Bypass**: Directly calling repositories from controllers
- **Transaction Misuse**: Using `@Transactional` inappropriately or on wrong layers
- **Exception Handling**: Not implementing proper global exception handling
- **Security Gaps**: Misconfiguring Spring Security or bypassing security

## 🎯 Spring Boot Best Practices

### Production Readiness
- **Actuator Endpoints**: Configure Spring Boot Actuator for monitoring and management
- **Health Checks**: Implement custom health indicators for dependencies
- **Metrics**: Use Micrometer for application metrics collection
- **Logging**: Configure structured logging with correlation IDs
- **Security**: Implement proper authentication, authorization, and security headers

### Performance Optimization
- **Connection Pooling**: Optimize database connection pooling settings
- **Caching**: Implement caching with Spring Cache abstraction
- **Async Processing**: Use `@Async` for non-blocking operations
- **Lazy Loading**: Configure appropriate JPA lazy loading strategies
- **Startup Time**: Optimize application startup time with proper configuration

### Development Workflow
- **DevTools**: Use Spring Boot DevTools for development productivity
- **Profile Management**: Proper use of Spring profiles for different environments
- **Configuration Documentation**: Document all configuration properties
- **API Documentation**: Use OpenAPI/Swagger for API documentation
- **Code Quality**: Integrate static analysis tools with Spring Boot specific rules

## 📚 Reference Links

### Official Documentation
- [Spring Boot Reference Documentation](https://docs.spring.io/spring-boot/docs/current/reference/htmlsingle/)
- [Spring Framework Documentation](https://docs.spring.io/spring-framework/docs/current/reference/html/)
- [Spring Data JPA Reference](https://docs.spring.io/spring-data/jpa/docs/current/reference/html/)
- [Spring Security Reference](https://docs.spring.io/spring-security/reference/)

### Essential Tools & Libraries
- [Spring Boot Starters](https://docs.spring.io/spring-boot/docs/current/reference/htmlsingle/#using.build-systems.starters)
- [Spring Boot Actuator](https://docs.spring.io/spring-boot/docs/current/reference/htmlsingle/#actuator)
- [Micrometer Metrics](https://micrometer.io/docs)
- [TestContainers](https://www.testcontainers.org/)
- [Flyway Database Migration](https://flywaydb.org/documentation/)
- Use Spring Security for authentication and authorization
- Implement method-level security with `@PreAuthorize` and `@PostAuthorize`
- Configure security chains for different URL patterns
- Use Spring Security's CSRF protection appropriately
- Implement JWT token handling with Spring Security

### Spring Boot Web Layer
- Use `@RestController` for REST APIs
- Implement proper HTTP status codes (200, 201, 400, 404, 500)
- Use `@Valid` for request body validation with Bean Validation
- Handle exceptions using `@ControllerAdvice` and `@ExceptionHandler`
- Implement proper Content-Type handling and serialization

### Spring Boot Testing
- Use `@SpringBootTest` for integration tests
- Use `@WebMvcTest` for testing web layer components
- Use `@DataJpaTest` for testing JPA repositories
- Mock Spring beans with `@MockBean` for unit tests
- Use `@TestPropertySource` for test-specific configuration
- Implement test slices for focused testing of specific layers

### Spring Boot Actuator and Monitoring
- Enable Spring Boot Actuator for health checks and metrics
- Configure custom health indicators for external dependencies
- Use Micrometer for application metrics collection
- Implement distributed tracing with Spring Cloud Sleuth
- Configure log aggregation for production monitoring

### Spring Boot DevTools and Development
- Use Spring Boot DevTools for faster development cycles
- Configure automatic restart and live reload features
- Use Spring Boot's configuration processor for IDE support
- Implement proper error pages and error handling
- Use Spring Boot's banner customization for branding

## Spring Boot Build and Deployment
- Use Spring Boot Maven or Gradle plugins for packaging
- Configure Spring Boot fat JAR creation for deployment
- Implement health checks for container orchestration
- Use Spring Boot's embedded server configuration
- Configure SSL/TLS termination appropriately
- Run `mvn clean install` (Maven) or `./gradlew build` (Gradle) to verify builds
- Ensure all tests pass as part of the build process

## Spring Boot Anti-Patterns
- Don't use field injection (`@Autowired` on fields) - use constructor injection
- Avoid exposing JPA entities directly in REST controllers - use DTOs
- Don't hardcode configuration values - use `@Value` or `@ConfigurationProperties`
- Avoid business logic in controllers - delegate to service classes
- Don't ignore Spring Boot's auto-configuration - use it effectively

## Spring Boot References
- [Spring Boot Documentation](https://docs.spring.io/spring-boot/docs/current/reference/htmlsingle/)
- [Spring Framework Reference](https://docs.spring.io/spring-framework/docs/current/reference/html/)
- [Spring Security Reference](https://docs.spring.io/spring-security/site/docs/current/reference/html5/)
- [Spring Data JPA Reference](https://docs.spring.io/spring-data/jpa/docs/current/reference/html/)
- [Spring Boot Actuator Guide](https://docs.spring.io/spring-boot/docs/current/actuator-api/htmlsingle/)