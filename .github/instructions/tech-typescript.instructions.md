---
description: TypeScript development standards and best practices for all TypeScript frameworks
applyTo: "**/*.ts,**/*.tsx"
---

# TypeScript Development Standards

## 🏗️ Architecture & Navigation
- **Root Standards**: [General Coding Standards](./tech-general-coding.instructions.md)
- **Security Guidelines**: [Security & OWASP](./security-owasp.instructions.md)
- **Performance Guidelines**: [Performance Optimization](./tech-performance-optimization.instructions.md)
- **Framework Extensions**: [Angular](./tech-angular.instructions.md) | [React](./tech-reactjs.instructions.md)

---

## 🔷 TypeScript-Specific Context

- **TypeScript Version**: 4.9+ (prefer 5.0+ for new projects)
- **Target Environment**: ES2020+, Node.js 18+, Modern browsers
- **Code Style**: Strict TypeScript configuration with ESLint + Prettier
- **Common Frameworks**: Angular, React, Node.js, Express, NestJS
- **Architecture Patterns**: Component-based, Modular, Clean Architecture

## 🔧 TypeScript Language Standards

### Type Safety & Strict Configuration
- **Strict Mode**: Enable `strict: true` in tsconfig.json with all strict flags
- **Type Annotations**: Explicit types for function parameters, return values, and complex variables
- **No Any**: Avoid `any` type; use `unknown` with type guards when necessary
- **Null Safety**: Handle null/undefined with optional chaining (`?.`) and nullish coalescing (`??`)
- **Type Guards**: Use type predicates and discriminated unions for runtime type safety

### Type System Best Practices
- **Interfaces vs Types**: Prefer interfaces for object shapes, type aliases for unions/primitives
- **Generics**: Use generics for reusable, type-safe components and functions
- **Utility Types**: Leverage built-in utility types (Partial, Pick, Omit, Record, etc.)
- **Union Types**: Use union types for values that can be one of several types
- **Literal Types**: Use string/number literal types for precise value constraints

### Modern TypeScript Features
- **Template Literal Types**: Use for type-safe string manipulation
- **Conditional Types**: Implement type-level logic for complex type transformations
- **Mapped Types**: Create new types by transforming existing ones
- **Decorators**: Use experimentally when supported by your framework
- **Assertion Functions**: Implement custom assertion functions for type narrowing

### Code Organization
- **Module System**: Use ES modules with proper import/export statements
- **Type Definitions**: Organize types in dedicated files (types/, @types/)
- **Barrel Exports**: Use index files to create clean public APIs
- **Path Mapping**: Configure path aliases in tsconfig for clean imports
- **Declaration Files**: Generate .d.ts files for libraries

## 📁 Project Structure

```
src/
├── types/                          # Global type definitions
│   ├── index.ts                    # Main type exports
│   ├── api.ts                      # API-related types
│   ├── common.ts                   # Common/shared types
│   └── domain/                     # Domain-specific types
│       ├── user.ts
│       └── product.ts
├── interfaces/                     # Interface definitions
│   ├── IRepository.ts
│   ├── IService.ts
│   └── IController.ts
├── models/                         # Data models
│   ├── base/
│   │   ├── BaseEntity.ts
│   │   └── BaseModel.ts
│   └── entities/
│       ├── User.ts
│       └── Product.ts
├── services/                       # Business logic services
│   ├── base/
│   │   └── BaseService.ts
│   ├── UserService.ts
│   └── ProductService.ts
├── repositories/                   # Data access layer
│   ├── base/
│   │   └── BaseRepository.ts
│   ├── UserRepository.ts
│   └── ProductRepository.ts
├── controllers/                    # Request handlers
│   ├── base/
│   │   └── BaseController.ts
│   ├── UserController.ts
│   └── ProductController.ts
├── utils/                          # Utility functions
│   ├── types.ts                    # Type utility functions
│   ├── validators.ts               # Validation utilities
│   └── helpers.ts                  # General helpers
├── config/                         # Configuration
│   ├── database.ts
│   ├── environment.ts
│   └── constants.ts
└── main.ts                         # Application entry point

tests/
├── __mocks__/                      # Mock implementations
├── fixtures/                       # Test data
├── unit/                           # Unit tests
├── integration/                    # Integration tests
└── types/                          # Test type definitions
```

## 🧪 TypeScript Testing Standards

### Testing Framework & Tools
- **Primary Framework**: Jest with ts-jest, Vitest for modern projects
- **Type Testing**: Use @ts-expect-error and type-only imports for type tests
- **Mocking**: Jest mocks with proper TypeScript typing
- **Coverage**: Istanbul/NYC with minimum 90% coverage requirement
- **API Testing**: Supertest for HTTP API testing with proper typing

### Type-Safe Testing
- **Test Types**: Define types for test data and mock objects
- **Mock Typing**: Properly type mocks and stubs for type safety
- **Assertion Types**: Use typed assertion libraries (expect with TypeScript)
- **Test Utilities**: Create type-safe test utilities and factories
- **Error Testing**: Test error types and exception scenarios

## 🚫 TypeScript Anti-Patterns

### Type System Misuse
- **Any Abuse**: Using `any` type to bypass type checking
- **Type Assertions**: Overusing `as` assertions instead of proper type guards
- **Implicit Any**: Allowing implicit any through loose configuration
- **Object Literals**: Using object literals instead of proper interfaces
- **Function Overloads**: Overusing function overloads when generics would work

### Code Organization Issues
- **Large Type Files**: Monolithic type files instead of modular organization
- **Circular Dependencies**: Creating circular imports between modules
- **Mixed Concerns**: Mixing types with implementation in the same file
- **Global Scope Pollution**: Declaring too many global types
- **Missing Type Exports**: Not properly exporting types from modules

## 🎯 TypeScript Best Practices

### Development Workflow
- **Compiler Options**: Use strict compiler options and enable useful strict flags
- **IDE Integration**: Leverage TypeScript language server features fully
- **Type Checking**: Run tsc --noEmit in CI/CD for type checking
- **Incremental Compilation**: Use project references for large codebases
- **Build Optimization**: Configure proper build and watch modes

### Advanced Type Patterns
- **Branded Types**: Use branded types for domain-specific primitives
- **State Machines**: Model state with discriminated unions
- **Builder Pattern**: Implement type-safe builder patterns with fluent APIs
- **Event Systems**: Create type-safe event systems with mapped types
- **API Contracts**: Define strict API contracts with TypeScript types

### Performance Considerations
- **Type Complexity**: Keep types simple to reduce compilation time
- **Lazy Loading**: Use dynamic imports for large modules
- **Tree Shaking**: Structure code for effective dead code elimination
- **Bundle Analysis**: Analyze and optimize TypeScript compilation output
- **Memory Usage**: Monitor TypeScript compiler memory usage in large projects

## 📚 Reference Links

### Official Documentation
- [TypeScript Documentation](https://www.typescriptlang.org/docs/)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/handbook/intro.html)
- [TypeScript Release Notes](https://www.typescriptlang.org/docs/handbook/release-notes/overview.html)
- [TSConfig Reference](https://www.typescriptlang.org/tsconfig)

### Essential Tools & Libraries
- [ESLint TypeScript Rules](https://typescript-eslint.io/)
- [Prettier TypeScript](https://prettier.io/docs/en/configuration.html)
- [Jest TypeScript](https://jestjs.io/docs/getting-started#using-typescript)
- [ts-node](https://typestrong.org/ts-node/)
- [Type-fest Utility Types](https://github.com/sindresorhus/type-fest)