---
description: Quarkus development standards and framework-specific best practices
applyTo: "**/*.java"
---

# Quarkus Development Standards

## 🏗️ Architecture & Navigation
- **Root Standards**: [General Coding Standards](./tech-general-coding.instructions.md)
- **Language Standards**: [Java Development](./tech-java.instructions.md)
- **Security Guidelines**: [Security & OWASP](./security-owasp.instructions.md)
- **Performance Guidelines**: [Performance Optimization](./tech-performance-optimization.instructions.md)
- **Related Frameworks**: [Spring Boot](./tech-springboot.instructions.md) (alternative Java framework)

---

## 🚀 Quarkus-Specific Context

- **Quarkus Version**: 3.x+ with Java 17+ (prefer 21+ for new projects)
- **Build Tools**: Maven (preferred) or Gradle with Quarkus plugins
- **Architecture Focus**: Cloud-native, performance optimization, GraalVM compatibility
- **Standards**: Jakarta EE and MicroProfile conventions for enterprise patterns
- **Deployment**: Container-first design with native compilation support

## 🔧 Quarkus Framework Standards

### CDI & Dependency Injection
- **Scope Management**: Use `@ApplicationScoped` for singleton beans instead of `@Singleton`
- **Constructor Injection**: Use constructor injection with `@Inject` for dependency injection
- **Request Scoping**: Prefer `@RequestScoped` for request-specific beans to optimize memory
- **Configuration Injection**: Use `@ConfigProperty` for type-safe configuration injection
- **Performance**: Implement proper CDI scope management for optimal performance and memory usage

### REST & JAX-RS Implementation
- **JAX-RS Annotations**: Use JAX-RS annotations (`@Path`, `@GET`, `@POST`, etc.) for REST endpoints
- **Path Design**: Apply `@Path` with descriptive, RESTful endpoint paths
- **Content Negotiation**: Use `@Consumes(MediaType.APPLICATION_JSON)` and `@Produces(MediaType.APPLICATION_JSON)`
- **Response Handling**: Return proper HTTP status codes with `Response` class for complex responses
- **Rate Limiting**: Implement rate limiting for public endpoints using Quarkus extensions

### Data Access with Panache
- **Entity Design**: Prefer Panache entities (extend `PanacheEntity`) over traditional JPA entities
- **Repository Pattern**: Use Panache repositories (`PanacheRepository<T>`) for complex queries
- **Transaction Management**: Always use `@Transactional` for data modifications in service methods
- **Query Optimization**: Use named queries for complex database operations and performance optimization
- **Pagination**: Implement proper pagination using Panache's built-in pagination support

### Configuration Management
- **Configuration Files**: Use `application.properties` or `application.yaml` for configuration
- **Environment Profiles**: Leverage Quarkus profiles for environment-specific configurations
- **Type Safety**: Use `@ConfigProperty` with proper type conversion and validation
- **External Configuration**: Support for external configuration sources and hot reloading
- **Secret Management**: Integrate with secret management solutions (Kubernetes secrets, Vault)

## 📁 Quarkus Project Structure

```
src/
├── main/
│   ├── java/
│   │   └── com/company/project/
│   │       ├── Application.java              # Quarkus application main class (optional)
│   │       ├── config/                       # Configuration classes
│   │       │   ├── DatabaseConfig.java
│   │       │   ├── SecurityConfig.java
│   │       │   └── OpenApiConfig.java
│   │       ├── rest/                         # JAX-RS resources
│   │       │   ├── UserResource.java
│   │       │   ├── ProductResource.java
│   │       │   └── exception/
│   │       │       └── ExceptionMapper.java
│   │       ├── service/                      # Business services
│   │       │   ├── UserService.java
│   │       │   └── ProductService.java
│   │       ├── repository/                   # Panache repositories
│   │       │   ├── UserRepository.java
│   │       │   └── ProductRepository.java
│   │       ├── entity/                       # Panache entities
│   │       │   ├── BaseEntity.java
│   │       │   ├── User.java
│   │       │   └── Product.java
│   │       ├── dto/                          # Data Transfer Objects
│   │       │   ├── UserDto.java
│   │       │   ├── CreateUserRequest.java
│   │       │   └── ApiResponse.java
│   │       ├── security/                     # Security components
│   │       │   ├── JwtGenerator.java
│   │       │   ├── AuthService.java
│   │       │   └── SecurityIdentity.java
│   │       ├── health/                       # Health checks
│   │       │   ├── DatabaseHealthCheck.java
│   │       │   └── CustomHealthCheck.java
│   │       ├── exception/                    # Custom exceptions
│   │       │   ├── BusinessException.java
│   │       │   └── ValidationException.java
│   │       └── util/                         # Utility classes
│   │           ├── DateUtils.java
│   │           └── ValidationUtils.java
│   ├── resources/
│   │   ├── application.properties            # Main configuration
│   │   ├── application-dev.properties        # Development profile
│   │   ├── application-prod.properties       # Production profile
│   │   ├── application-test.properties       # Test profile
│   │   ├── META-INF/
│   │   │   ├── openapi.yaml                 # OpenAPI specification
│   │   │   └── resources/                   # Static resources
│   │   └── db/migration/                    # Flyway migrations
│   │       ├── V1__Create_users_table.sql
│   │       └── V2__Create_products_table.sql
│   └── docker/                              # Docker configurations
│       ├── Dockerfile.jvm
│       ├── Dockerfile.native
│       └── docker-compose.yml
└── test/
    ├── java/
    │   └── com/company/project/
    │       ├── rest/                        # Resource tests
    │       │   ├── UserResourceTest.java
    │       │   └── UserResourceIT.java      # Integration tests
    │       ├── service/                     # Service tests
    │       │   └── UserServiceTest.java
    │       ├── repository/                  # Repository tests
    │       │   └── UserRepositoryTest.java
    │       └── TestLifecycleManager.java    # Test lifecycle management
    └── resources/
        └── application-test.properties      # Test configuration
```

## 🧪 Quarkus Testing Standards

### Testing Framework & Annotations
- **Quarkus Test**: Use `@QuarkusTest` for integration tests with full Quarkus context
- **Unit Testing**: Use JUnit 5 for unit tests without Quarkus context
- **Native Testing**: Use `@QuarkusIntegrationTest` for native build testing
- **Test Resources**: Use `@QuarkusTestResource` for external service management
- **TestContainers**: Integrate TestContainers for database and service testing

### Testing Best Practices
- **Test Categories**: Separate unit tests, integration tests, and native tests
- **Resource Management**: Use Quarkus test resources for managing external dependencies
- **Profile Testing**: Use test profiles for test-specific configuration
- **Performance Testing**: Include startup time and memory consumption tests
- **REST Testing**: Use RestAssured for comprehensive REST endpoint testing

### Continuous Testing
- **Development Mode**: Leverage Quarkus dev mode for continuous testing
- **Test Automation**: Integrate tests into CI/CD pipelines with native compilation
- **Coverage**: Use JaCoCo for code coverage with appropriate thresholds
- **Performance Benchmarks**: Include performance benchmarks in test suites
- **Native Compatibility**: Ensure tests pass in both JVM and native modes

## 🚫 Quarkus Anti-Patterns

### Performance Issues
- **Reflection Heavy Code**: Avoid extensive reflection usage without proper GraalVM configuration
- **Large Dependency Trees**: Including unnecessary dependencies that increase startup time
- **Improper Scoping**: Using inappropriate CDI scopes affecting memory and performance
- **Blocking Operations**: Using blocking operations without proper thread pool configuration
- **Startup Overhead**: Performing expensive operations during application startup

### Configuration Problems
- **Runtime Configuration**: Trying to change build-time configuration at runtime
- **Profile Misuse**: Incorrectly using Quarkus profiles or mixing with other profile systems
- **Extension Conflicts**: Using conflicting extensions without proper resolution
- **Native Build Issues**: Not testing native builds or ignoring native compilation warnings
- **Security Misconfig**: Misconfiguring security extensions or leaving defaults in production

## 🎯 Quarkus Best Practices

### Cloud-Native Development
- **Container Optimization**: Optimize Docker images for size and startup time
- **Resource Limits**: Configure appropriate resource limits for containers
- **Health Endpoints**: Implement comprehensive health checks for orchestration platforms
- **Metrics Integration**: Use MicroProfile Metrics for application monitoring
- **Configuration Sources**: Use cloud-native configuration sources (ConfigMaps, Secrets)

### Performance Optimization
- **Native Compilation**: Optimize for GraalVM native compilation when needed
- **Startup Time**: Minimize application startup time through proper configuration
- **Memory Footprint**: Optimize memory usage for container environments
- **Build Time**: Optimize build times through proper caching and incremental compilation
- **Runtime Performance**: Profile and optimize hot paths in the application

### Production Readiness
- **Observability**: Implement proper logging, metrics, and tracing
- **Security**: Configure security extensions properly for production environments
- **Resilience**: Implement circuit breakers, timeouts, and retry mechanisms
- **Documentation**: Generate and maintain OpenAPI documentation
- **Monitoring**: Set up application and infrastructure monitoring

### Development Workflow
- **Dev Services**: Leverage Quarkus Dev Services for development dependencies
- **Hot Reload**: Use Quarkus dev mode for efficient development cycles
- **Extension Management**: Properly manage and update Quarkus extensions
- **Build Optimization**: Optimize Maven/Gradle build configurations
- **IDE Integration**: Configure proper IDE support for Quarkus development

## 📚 Reference Links

### Official Documentation
- [Quarkus Documentation](https://quarkus.io/guides/)
- [Quarkus Reference Guide](https://quarkus.io/guides/all-config)
- [MicroProfile Specifications](https://microprofile.io/specifications/)
- [Jakarta EE Documentation](https://jakarta.ee/specifications/)

### Essential Extensions & Tools
- [Quarkus Extensions](https://quarkus.io/extensions/)
- [Panache ORM Guide](https://quarkus.io/guides/hibernate-orm-panache)
- [RESTEasy Reactive](https://quarkus.io/guides/resteasy-reactive)
- [SmallRye Config](https://quarkus.io/guides/config-reference)
- [GraalVM Documentation](https://www.graalvm.org/latest/docs/)

### Cloud Native & DevOps
- [Quarkus Container Images](https://quarkus.io/guides/container-image)
- [Kubernetes Deployment](https://quarkus.io/guides/deploying-to-kubernetes)
- [OpenShift Integration](https://quarkus.io/guides/deploying-to-openshift)
- [Tekton Pipelines](https://quarkus.io/guides/building-with-tekton)
- Use `@ConfigProperty` for type-safe configuration property injection
- Prefer environment variables for sensitive data and cloud deployments
- Use Quarkus profiles for different environments (dev, test, prod)
- Leverage Quarkus configuration hot-reload in development mode

### Quarkus Development and Build Optimization
- Leverage Quarkus Dev Mode for faster development cycles and hot reloading
- Implement build-time optimizations using Quarkus extensions and compile-time processing
- Configure native builds with GraalVM for optimal performance using quarkus-maven-plugin
- Use Quarkus extension ecosystem for common functionality (security, metrics, health)
- Optimize startup time and memory usage for cloud-native deployments


### Quarkus Testing Framework
- Use `@QuarkusTest` for integration tests with Quarkus test framework
- Use JUnit 5 for unit tests with Quarkus-specific extensions
- Use `@QuarkusIntegrationTest` for native build and container tests
- Mock external dependencies using `@QuarkusTestResource` and test containers
- Use RestAssured for REST endpoint testing with Quarkus integration
- Use `@Transactional` annotations for tests that modify database state
- Implement test containers for database integration testing

### Quarkus Logging and Monitoring
- Use Quarkus logging capabilities (unified logging with JBoss Logging)
- Configure log levels and formats using Quarkus configuration
- Implement health checks using Quarkus SmallRye Health extension
- Use Quarkus metrics with Micrometer for application monitoring
- Implement distributed tracing with Quarkus OpenTelemetry integration

### Quarkus Security Implementation
- Use Quarkus Security extensions (e.g., `quarkus-smallrye-jwt`, `quarkus-oidc`)
- Implement role-based access control (RBAC) using MicroProfile JWT or OIDC
- Use Quarkus security annotations for method-level security
- Implement proper authentication flows with Quarkus security providers
- Validate all input parameters using Bean Validation with Quarkus integration

## Quarkus Anti-Patterns
- Don't use field injection in tests—use constructor injection for better testability
- Don't hardcode configuration values—use Quarkus configuration system
- Don't ignore exceptions—implement proper error handling with Quarkus patterns
- Avoid traditional JPA patterns when Panache provides simpler alternatives
- Don't skip native compilation testing for production deployments

## Quarkus Performance Optimization
- Use Quarkus build-time processing for compile-time optimizations
- Implement proper reflection configuration for native builds
- Use Quarkus extensions instead of traditional Java libraries when available
- Optimize memory usage for GraalVM native images
- Leverage Quarkus caching extensions for performance improvements

## Quarkus References
- [Quarkus Documentation](https://quarkus.io/guides/)
- [Quarkus Extensions](https://quarkus.io/extensions/)
- [MicroProfile Specifications](https://microprofile.io/specifications/)
- [GraalVM Native Image](https://www.graalvm.org/22.0/reference-manual/native-image/)
- [Quarkus Testing Guide](https://quarkus.io/guides/getting-started-testing)