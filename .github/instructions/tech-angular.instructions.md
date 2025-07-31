---
description: Angular development standards and framework-specific best practices
applyTo: "**/*.ts,**/*.html,**/*.scss,**/*.css"
---

# Angular Development Standards

## 🏗️ Architecture & Navigation
- **Root Standards**: [General Coding Standards](./tech-general-coding.instructions.md)
- **Language Standards**: [TypeScript Development](./tech-typescript.instructions.md)
- **Security Guidelines**: [Security & OWASP](./security-owasp.instructions.md)
- **Performance Guidelines**: [Performance Optimization](./tech-performance-optimization.instructions.md)
- **Related Frameworks**: [React](./tech-reactjs.instructions.md) (alternative frontend framework)

---

## 🅰️ Angular-Specific Context

- **Angular Version**: 15+ (prefer 18+ for new projects with latest features)
- **Language**: TypeScript (required for Angular)
- **Build Tools**: Angular CLI with Webpack or esbuild
- **Architecture Patterns**: Standalone components, Feature modules, Lazy loading
- **State Management**: Angular Signals, NgRx for complex state, Services for simple state

## 🔧 Angular Framework Standards

### Architecture & Project Structure
- **Standalone Components**: Use standalone components as the default (Angular 14+)
- **Feature Organization**: Organize code by feature modules or domains for scalability
- **Lazy Loading**: Implement lazy loading for feature modules to optimize performance
- **Dependency Injection**: Use Angular's DI system effectively with proper service hierarchies
- **Component Strategy**: Clear separation between smart (container) and presentational components

### Component Design & Lifecycle
- **Lifecycle Hooks**: Implement OnInit, OnDestroy, and other lifecycle hooks appropriately
- **Modern APIs**: Use `input()`, `output()`, `viewChild()`, `contentChild()` functions (Angular 17+)
- **Change Detection**: Leverage OnPush change detection strategy for performance optimization
- **Template Logic**: Keep templates clean, move complex logic to component classes or services
- **Reactive Programming**: Use RxJS operators and Angular Signals for reactive programming

### Angular Signals & State Management
- **Signal APIs**: Use `signal()`, `computed()`, and `effect()` for reactive state management
- **Writable Signals**: Use writable signals for mutable component state
- **Computed Signals**: Leverage computed signals for derived state calculations
- **Effect Management**: Use effects sparingly and clean them up properly
- **Service State**: Manage shared state in services using signals or observables

## 📁 Angular Project Structure

```
src/
├── app/
│   ├── core/                        # Singleton services and core functionality
│   │   ├── guards/
│   │   │   ├── auth.guard.ts
│   │   │   └── role.guard.ts
│   │   ├── interceptors/
│   │   │   ├── auth.interceptor.ts
│   │   │   ├── error.interceptor.ts
│   │   │   └── logging.interceptor.ts
│   │   ├── services/
│   │   │   ├── auth.service.ts
│   │   │   ├── api.service.ts
│   │   │   └── notification.service.ts
│   │   └── models/
│   │       ├── user.model.ts
│   │       └── api-response.model.ts
│   ├── shared/                      # Shared components, directives, pipes
│   │   ├── components/
│   │   │   ├── loading-spinner/
│   │   │   │   ├── loading-spinner.component.ts
│   │   │   │   ├── loading-spinner.component.html
│   │   │   │   └── loading-spinner.component.scss
│   │   │   ├── confirmation-dialog/
│   │   │   └── data-table/
│   │   ├── directives/
│   │   │   ├── highlight.directive.ts
│   │   │   └── click-outside.directive.ts
│   │   ├── pipes/
│   │   │   ├── safe-html.pipe.ts
│   │   │   └── truncate.pipe.ts
│   │   └── validators/
│   │       ├── custom-validators.ts
│   │       └── async-validators.ts
│   ├── features/                    # Feature modules
│   │   ├── auth/
│   │   │   ├── components/
│   │   │   │   ├── login/
│   │   │   │   └── register/
│   │   │   ├── services/
│   │   │   │   └── auth-feature.service.ts
│   │   │   ├── models/
│   │   │   │   └── login.model.ts
│   │   │   └── auth.routes.ts
│   │   ├── dashboard/
│   │   │   ├── components/
│   │   │   ├── services/
│   │   │   └── dashboard.routes.ts
│   │   └── user-management/
│   │       ├── components/
│   │       ├── services/
│   │       └── user-management.routes.ts
│   ├── layout/                      # Layout components
│   │   ├── header/
│   │   ├── sidebar/
│   │   ├── footer/
│   │   └── main-layout/
│   ├── app.component.ts             # Root component
│   ├── app.component.html
│   ├── app.component.scss
│   ├── app.config.ts               # Application configuration
│   └── app.routes.ts               # Application routing
├── assets/                          # Static assets
│   ├── images/
│   ├── icons/
│   ├── i18n/                       # Internationalization files
│   └── styles/
│       ├── _variables.scss
│       ├── _mixins.scss
│       └── themes/
├── environments/                    # Environment configurations
│   ├── environment.ts
│   ├── environment.prod.ts
│   └── environment.test.ts
├── styles.scss                     # Global styles
├── main.ts                         # Application bootstrap
└── index.html                      # Main HTML file

e2e/                                # End-to-end tests
├── src/
│   ├── app.e2e-spec.ts
│   └── app.po.ts
└── protractor.conf.js

tests/                              # Unit tests
├── helpers/
├── mocks/
└── fixtures/
```

## 🧪 Angular Testing Standards

### Testing Framework & Tools
- **Primary Framework**: Jasmine + Karma for unit tests, Protractor/Cypress for E2E
- **Component Testing**: TestBed for component integration testing
- **Service Testing**: Isolated testing with proper mocking
- **HTTP Testing**: HttpClientTestingModule for HTTP service testing
- **Coverage**: Istanbul with minimum 90% coverage requirement

### Testing Best Practices
- **Component Testing**: Test component behavior, not implementation details
- **Service Testing**: Mock dependencies and test business logic
- **Integration Testing**: Test component-service integration
- **E2E Testing**: Test critical user workflows and business processes
- **Accessibility Testing**: Include a11y testing in component tests

### Angular-Specific Testing Patterns
```typescript
// Component testing with TestBed
describe('UserComponent', () => {
  let component: UserComponent;
  let fixture: ComponentFixture<UserComponent>;
  let userService: jasmine.SpyObj<UserService>;

  beforeEach(() => {
    const spy = jasmine.createSpyObj('UserService', ['getUsers']);
    
    TestBed.configureTestingModule({
      imports: [UserComponent],
      providers: [{ provide: UserService, useValue: spy }]
    });
    
    fixture = TestBed.createComponent(UserComponent);
    component = fixture.componentInstance;
    userService = TestBed.inject(UserService) as jasmine.SpyObj<UserService>;
  });

  it('should load users on init', () => {
    userService.getUsers.and.returnValue(of(mockUsers));
    component.ngOnInit();
    expect(userService.getUsers).toHaveBeenCalled();
  });
});
```

## 🚫 Angular Anti-Patterns

### Component Design Issues
- **Large Components**: Creating monolithic components with too many responsibilities
- **Template Complexity**: Putting too much logic in templates
- **Memory Leaks**: Not unsubscribing from observables in OnDestroy
- **Change Detection**: Overusing default change detection without OnPush optimization
- **Direct DOM Manipulation**: Bypassing Angular's rendering with direct DOM access

### Architecture Problems
- **Circular Dependencies**: Creating circular dependencies between modules/services
- **Shared Mutable State**: Sharing mutable state between components without proper management
- **Service Coupling**: Tightly coupling services without proper abstraction
- **Route Coupling**: Creating tight coupling between route parameters and components
- **Module Organization**: Poor module organization leading to large bundle sizes

### Performance Issues
- **Subscription Management**: Not properly managing RxJS subscriptions
- **Unnecessary Computations**: Performing expensive operations in templates
- **Large Bundle Sizes**: Not implementing proper lazy loading strategies
- **Change Detection Triggers**: Creating unnecessary change detection cycles
- **Memory Management**: Not cleaning up resources and event listeners

## 🎯 Angular Best Practices

### Performance Optimization
- **OnPush Strategy**: Use OnPush change detection for better performance
- **TrackBy Functions**: Implement trackBy functions for ngFor loops
- **Lazy Loading**: Implement route-based lazy loading for better initial load times
- **Preloading**: Use preloading strategies for frequently accessed routes
- **Bundle Analysis**: Regularly analyze and optimize bundle sizes

### Reactive Programming
- **RxJS Operators**: Master essential RxJS operators (map, filter, switchMap, catchError)
- **Async Pipe**: Use async pipe in templates to automatically handle subscriptions
- **Subject Usage**: Use Subjects appropriately for component communication
- **Error Handling**: Implement proper error handling in observable streams
- **Memory Management**: Always unsubscribe from observables to prevent memory leaks

### Development Workflow
- **Angular CLI**: Leverage Angular CLI for scaffolding and building
- **Linting**: Use Angular ESLint rules for consistent code quality
- **Formatting**: Use Prettier with Angular-specific configurations
- **Type Safety**: Leverage Angular's type system for better development experience
- **Documentation**: Use Compodoc for generating Angular project documentation

### Accessibility & UX
- **Semantic HTML**: Use proper semantic HTML elements in templates
- **ARIA Support**: Implement proper ARIA attributes for accessibility
- **Keyboard Navigation**: Ensure full keyboard accessibility
- **Screen Reader**: Test with screen readers and assistive technologies
- **Internationalization**: Use Angular i18n for multi-language support

## 📚 Reference Links

### Official Documentation
- [Angular Documentation](https://angular.dev/)
- [Angular Style Guide](https://angular.dev/style-guide)
- [Angular CLI Reference](https://angular.dev/tools/cli)
- [Angular Testing Guide](https://angular.dev/guide/testing)

### Essential Tools & Libraries
- [Angular Material](https://material.angular.io/)
- [Angular CDK](https://material.angular.io/cdk/categories)
- [NgRx State Management](https://ngrx.io/)
- [Angular Universal](https://angular.dev/guide/ssr)
- [Angular PWA](https://angular.dev/ecosystem/service-workers)

### Development Tools
- [Angular DevTools](https://angular.dev/tools/devtools)
- [Compodoc Documentation](https://compodoc.app/)
- [Angular ESLint](https://github.com/angular-eslint/angular-eslint)
- [Cypress E2E Testing](https://docs.cypress.io/guides/component-testing/angular/overview)
- [Storybook for Angular](https://storybook.js.org/docs/get-started/angular)
- Handle loading and error states with signals and proper UI feedback
- Use Angular's `AsyncPipe` to handle observables in templates when combining signals with RxJS

### Data Fetching
- Use Angular's `HttpClient` with Angular-specific typing patterns
- Implement Angular `HttpInterceptor` for request/response transformation
- Use Angular's `inject()` function for dependency injection in standalone components
- Implement caching strategies using Angular services and RxJS patterns
- Store API response data in Angular Signals for reactive updates
- Handle API errors with Angular interceptors and proper error boundaries

### Security
- Sanitize user inputs using Angular's built-in sanitization
- Implement route guards for authentication and authorization
- Use Angular's `HttpInterceptor` for CSRF protection and API authentication headers
- Validate form inputs with Angular's reactive forms and custom validators
- Follow Angular's security best practices (e.g., avoid direct DOM manipulation)

### Performance
- Enable production builds with `ng build --prod` for optimization
- Use lazy loading for routes to reduce initial bundle size
- Optimize change detection with `OnPush` strategy and signals for fine-grained reactivity
- Use trackBy in `ngFor` loops to improve rendering performance
- Implement server-side rendering (SSR) or static site generation (SSG) with Angular Universal (if specified)

### Testing
- Use Angular's testing framework: Jasmine and Karma for unit tests
- Use Angular's `TestBed` for component testing with Angular-specific setup
- Test Angular Signals integration and reactive state updates
- Use Angular testing utilities for mocking services and dependencies
- Mock HTTP requests using Angular's `HttpClientTestingModule`
- Test Angular-specific features: components, services, directives, pipes, guards

## Angular Implementation Process
1. Plan Angular project structure with feature modules and routing strategy
2. Define Angular-specific interfaces and models for components and services
3. Scaffold Angular components, services, and pipes using Angular CLI schematics
4. Implement Angular services with dependency injection and Signal-based state
5. Build Angular components with proper lifecycle management and data binding
6. Implement Angular reactive forms with validators and error handling
7. Apply Angular styling patterns with component encapsulation and theming
8. Configure Angular routing with lazy loading and route guards
9. Add Angular-specific error handling using interceptors and error boundaries
10. Write Angular tests using TestBed and Angular testing utilities
11. Optimize Angular performance with OnPush strategy and bundle analysis

## Angular-Specific Guidelines
- Follow Angular's naming conventions and file structure patterns
- Use Angular CLI schematics for consistent code generation
- Document Angular components and services with Angular-focused JSDoc patterns
- Leverage Angular CDK for accessibility utilities and common UI patterns
- Use Angular's built-in i18n package for internationalization features
- Create Angular shared modules and feature modules for code organization
- Use Angular Signals consistently throughout the application for reactive programming
- Leverage Angular's dependency injection for service composition and testability
- Follow Angular security best practices for sanitization and XSS prevention
- Use Angular DevTools for debugging and performance profiling