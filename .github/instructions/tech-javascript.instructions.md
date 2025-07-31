---
description: JavaScript development standards and best practices
applyTo: "**/*.js"
---

# JavaScript Development Standards

## 🏗️ Architecture & Navigation
- **Root Standards**: [General Coding Standards](./tech-general-coding.instructions.md)
- **Security Guidelines**: [Security & OWASP](./security-owasp.instructions.md)
- **Performance Guidelines**: [Performance Optimization](./tech-performance-optimization.instructions.md)
- **Language Evolution**: Consider [TypeScript](./tech-typescript.instructions.md) for type safety

---

## 🟨 JavaScript-Specific Context

- **JavaScript Version**: ES2020+ (ES2022+ preferred for new projects)
- **Runtime Environments**: Node.js 18+, Modern browsers (ES6+ support)
- **Code Style**: ESLint + Prettier with Airbnb or Standard configurations
- **Common Frameworks**: Express, React (without TypeScript), Vue, Node.js applications
- **Module System**: ES Modules (import/export), CommonJS for legacy Node.js

## 🔧 JavaScript Language Standards

### Modern JavaScript Features
- **ES Modules**: Use import/export statements for module management
- **Arrow Functions**: Use arrow functions for concise syntax, traditional functions for methods
- **Destructuring**: Use object and array destructuring for cleaner code
- **Template Literals**: Use template strings for string interpolation and multiline strings
- **Async/Await**: Prefer async/await over Promise chains for better readability

### Variable Declaration & Scope
- **const/let**: Use `const` by default, `let` when reassignment needed, never `var`
- **Block Scope**: Understand and leverage block scoping properly
- **Hoisting**: Be aware of hoisting behavior with functions and variables
- **Temporal Dead Zone**: Understand TDZ with let/const declarations
- **Closure Management**: Properly manage closures to avoid memory leaks

### Function Design
- **Pure Functions**: Prefer pure functions without side effects when possible
- **Function Expressions**: Use appropriate function declaration style for context
- **Parameters**: Use default parameters, rest parameters, and destructuring
- **Return Values**: Always return meaningful values, avoid implicit undefined returns
- **Function Length**: Keep functions small and focused on single responsibilities

### Object & Array Operations
- **Object Creation**: Use object literals, Object.create(), or class syntax appropriately
- **Property Access**: Use dot notation when possible, bracket notation when dynamic
- **Array Methods**: Leverage array methods (map, filter, reduce, forEach) over traditional loops
- **Spread Operator**: Use spread syntax for copying arrays/objects and function arguments
- **Object Shorthand**: Use property and method shorthand syntax

## 📁 Project Structure

```
src/
├── index.js                        # Application entry point
├── config/                         # Configuration management
│   ├── index.js                    # Main config exports
│   ├── database.js                 # Database configuration
│   ├── environment.js              # Environment variables
│   └── constants.js                # Application constants
├── controllers/                    # Request handlers
│   ├── base/
│   │   └── BaseController.js
│   ├── userController.js
│   └── productController.js
├── services/                       # Business logic layer
│   ├── base/
│   │   └── BaseService.js
│   ├── userService.js
│   └── productService.js
├── repositories/                   # Data access layer
│   ├── base/
│   │   └── BaseRepository.js
│   ├── userRepository.js
│   └── productRepository.js
├── models/                         # Data models
│   ├── base/
│   │   └── BaseModel.js
│   ├── User.js
│   └── Product.js
├── middleware/                     # Express middleware
│   ├── auth.js
│   ├── validation.js
│   ├── errorHandler.js
│   └── logging.js
├── routes/                         # Route definitions
│   ├── index.js                    # Main route exports
│   ├── userRoutes.js
│   └── productRoutes.js
├── utils/                          # Utility functions
│   ├── validators.js               # Input validation
│   ├── helpers.js                  # General helpers
│   ├── logger.js                   # Logging utilities
│   └── errorTypes.js               # Custom error classes
├── types/                          # JSDoc type definitions
│   ├── index.js                    # Type definitions export
│   ├── user.js
│   └── product.js
└── static/                         # Static assets
    ├── css/
    ├── js/
    └── images/

tests/
├── __mocks__/                      # Mock implementations
├── fixtures/                       # Test data
├── unit/                           # Unit tests
├── integration/                    # Integration tests
├── helpers/                        # Test utilities
└── setup.js                       # Test configuration
```

## 🧪 JavaScript Testing Standards

### Testing Framework & Tools
- **Primary Framework**: Jest for Node.js, Mocha/Chai as alternatives
- **Browser Testing**: Playwright, Cypress for end-to-end testing
- **Mocking**: Jest mocks, Sinon.js for more complex mocking needs
- **Coverage**: Jest built-in coverage, NYC for non-Jest projects
- **API Testing**: Supertest for HTTP endpoint testing

### Test Organization
- **Test Structure**: Mirror source directory structure in tests
- **Test Naming**: Descriptive test names using `describe` and `it/test` blocks
- **Setup/Teardown**: Use proper setup and teardown for test isolation
- **Async Testing**: Proper async/await or Promise handling in tests
- **Mock Strategy**: Mock external dependencies, use real implementations for internal logic

## 🚫 JavaScript Anti-Patterns

### Language Misuse
- **var Usage**: Using `var` instead of `const`/`let`
- **== vs ===**: Using loose equality instead of strict equality
- **Global Variables**: Polluting global scope with unnecessary variables
- **Callback Hell**: Nested callbacks instead of async/await or Promises
- **Type Coercion**: Relying on implicit type coercion

### Performance Issues
- **DOM Manipulation**: Excessive DOM queries and manipulations
- **Memory Leaks**: Not cleaning up event listeners, timers, or references
- **Synchronous Operations**: Using synchronous APIs in Node.js applications
- **Large Bundle Sizes**: Not optimizing for bundle size in frontend applications
- **Inefficient Loops**: Using wrong loop types or inefficient iteration patterns

### Code Organization Problems
- **Monolithic Files**: Creating overly large files without proper separation
- **Mixed Concerns**: Combining UI logic with business logic
- **Tight Coupling**: Creating tightly coupled modules that are hard to test
- **No Error Boundaries**: Not implementing proper error handling strategies
- **Inconsistent Patterns**: Mixing different coding patterns within the same project

## 🎯 JavaScript Best Practices

### Development Workflow
- **Linting**: Use ESLint with appropriate configuration (Airbnb, Standard)
- **Formatting**: Use Prettier for consistent code formatting
- **Documentation**: Use JSDoc for function and class documentation
- **Package Management**: Use npm or yarn with proper semantic versioning
- **Build Tools**: Use appropriate build tools (Webpack, Rollup, esbuild)

### Performance Optimization
- **Lazy Loading**: Implement lazy loading for large modules and components
- **Code Splitting**: Split code into smaller chunks for better loading performance
- **Caching**: Implement appropriate caching strategies for API calls
- **Minification**: Minify and compress JavaScript for production
- **Tree Shaking**: Remove unused code through proper module exports

### Security Considerations
- **Input Validation**: Validate and sanitize all user inputs
- **XSS Prevention**: Prevent cross-site scripting vulnerabilities
- **CSRF Protection**: Implement CSRF tokens for state-changing operations
- **Dependency Security**: Regularly audit and update dependencies
- **Environment Variables**: Properly manage sensitive configuration

### Modern JavaScript Practices
- **Module Bundling**: Use modern bundling strategies for optimal loading
- **Polyfills**: Use targeted polyfills for browser compatibility
- **Progressive Enhancement**: Build applications that work without JavaScript
- **Service Workers**: Implement service workers for offline functionality
- **Web APIs**: Leverage modern browser APIs when appropriate

## 📚 Reference Links

### Official Documentation
- [MDN JavaScript Reference](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference)
- [ECMAScript Specifications](https://tc39.es/ecma262/)
- [Node.js Documentation](https://nodejs.org/en/docs/)
- [Web APIs Documentation](https://developer.mozilla.org/en-US/docs/Web/API)

### Essential Tools & Libraries
- [ESLint Rules](https://eslint.org/docs/rules/)
- [Prettier Configuration](https://prettier.io/docs/en/configuration.html)
- [Jest Testing Framework](https://jestjs.io/docs/getting-started)
- [Express.js Framework](https://expressjs.com/en/guide/routing.html)
- [Lodash Utility Library](https://lodash.com/docs/)

### Style Guides & Best Practices
- [Airbnb JavaScript Style Guide](https://github.com/airbnb/javascript)
- [Clean Code JavaScript](https://github.com/ryanmcdermott/clean-code-javascript)
- [JavaScript: The Good Parts](https://www.oreilly.com/library/view/javascript-the-good/9780596517748/)
- [You Don't Know JS](https://github.com/getify/You-Dont-Know-JS)

## 📁 File Structure

Use this structure as a guide when creating or updating files:

```text
src/
  controllers/
  services/
  repositories/
  types/
  utils/
tests/
  unit/
  integration/
```

## 🧶 Patterns

### ✅ Patterns to Follow

JavaScript-specific patterns:
- Use Dependency Injection and Repository Pattern where applicable
- For APIs, include:
  - Input validation with Joi / express-validator
- For UI:
  - Components should be pure and reusable
  - Avoid inline styling; use Tailwind / CSS Modules / styled-components

### 🚫 Patterns to Avoid

JavaScript-specific anti-patterns:
- Don't generate code without tests
- Avoid global state unless absolutely necessary

## 🧪 Testing Guidelines

**Follow universal testing standards in [tech-general-coding.instructions.md](./tech-general-coding.instructions.md).**

JavaScript-specific testing:
- Use Jest for unit and integration tests
- Prefer test-driven development (TDD) when modifying core logic
- Include mocks/stubs for third-party services

## 🧩 Example Prompts

- `Copilot, create a REST endpoint using Express that retrieves all books from the books table.`
- `Copilot, generate a Joi schema for a user profile with optional avatar and required name/email.`
- `Copilot, implement a React hook to debounce a search input.`
- `Copilot, write a unit test for the calculatePrice() function using mocked dependencies.`

## 🔁 Iteration & Review

- Copilot output should be reviewed and modified before committing
- If code isn't following these instructions, regenerate with more context or split the task
- Use comments to clarify intent before invoking Copilot

## 📚 References

- [JavaScript Style Guide (Airbnb)](https://github.com/airbnb/javascript)
- [MDN JavaScript Reference](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference)
- [Node.js Documentation](https://nodejs.org/en/docs)
- [Express Documentation](https://expressjs.com/)
- [React Documentation](https://reactjs.org/docs/getting-started.html)
- [Jest Testing Framework](https://jestjs.io/docs/getting-started)
- [Winston Logger Documentation](https://github.com/winstonjs/winston)
- [Joi Schema Validation](https://joi.dev/api/)
- [Prettier Code Formatter](https://prettier.io/docs/en/index.html)
- [ESLint Rules and Configuration](https://eslint.org/docs/latest/)
- [Clean Code JavaScript](https://github.com/ryanmcdermott/clean-code-javascript)