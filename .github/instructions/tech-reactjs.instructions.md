---
description: React development standards and framework-specific best practices
applyTo: "**/*.jsx,**/*.tsx,**/*.js,**/*.ts"
---

# React Development Standards

## 🏗️ Architecture & Navigation
- **Root Standards**: [General Coding Standards](./tech-general-coding.instructions.md)
- **Language Standards**: [TypeScript Development](./tech-typescript.instructions.md) (recommended) | [JavaScript Development](./tech-javascript.instructions.md)
- **Security Guidelines**: [Security & OWASP](./security-owasp.instructions.md)
- **Performance Guidelines**: [Performance Optimization](./tech-performance-optimization.instructions.md)
- **Related Frameworks**: [Angular](./tech-angular.instructions.md) (alternative frontend framework)

---

## ⚛️ React-Specific Context

- **React Version**: 18+ (prefer 19+ for new projects)
- **Language**: TypeScript preferred for type safety, JavaScript for simpler projects
- **Build Tools**: Vite (preferred), Create React App, Next.js, or custom Webpack
- **Architecture Patterns**: Component composition, Hooks-based, Feature-driven
- **Ecosystem**: React Router, React Query/SWR, state management libraries

## 🔧 React Framework Standards

### Component Architecture
- **Functional Components**: Use functional components with hooks as the primary pattern
- **Component Composition**: Prefer composition over inheritance for component design
- **Single Responsibility**: Each component should have a single, well-defined purpose
- **Props Interface**: Define clear, typed interfaces for component props
- **Component Hierarchy**: Organize components in logical hierarchies with clear data flow

### Hooks & State Management
- **Built-in Hooks**: Master useState, useEffect, useContext, useReducer, useMemo, useCallback
- **Custom Hooks**: Extract reusable stateful logic into custom hooks
- **Effect Dependencies**: Properly manage useEffect dependencies to avoid infinite loops
- **Performance Hooks**: Use useMemo and useCallback for performance optimization
- **State Colocation**: Keep state as close to where it's used as possible

### Modern React Patterns
- **Concurrent Features**: Leverage React 18+ concurrent features (Suspense, Transitions)
- **Error Boundaries**: Implement error boundaries for graceful error handling
- **Code Splitting**: Use React.lazy and Suspense for dynamic imports
- **Portal Usage**: Use ReactDOM.createPortal for modals and overlays
- **Ref Management**: Proper use of useRef and forwardRef for DOM access

## 📁 React Project Structure

```
src/
├── components/                      # Reusable UI components
│   ├── ui/                         # Basic UI components
│   │   ├── Button/
│   │   │   ├── Button.tsx
│   │   │   ├── Button.test.tsx
│   │   │   ├── Button.stories.tsx
│   │   │   └── index.ts
│   │   ├── Input/
│   │   ├── Modal/
│   │   └── index.ts               # Barrel exports
│   ├── layout/                    # Layout components
│   │   ├── Header/
│   │   ├── Sidebar/
│   │   ├── Footer/
│   │   └── Layout/
│   └── common/                    # Common shared components
│       ├── LoadingSpinner/
│       ├── ErrorBoundary/
│       └── ProtectedRoute/
├── features/                      # Feature-based organization
│   ├── auth/
│   │   ├── components/           # Feature-specific components
│   │   │   ├── LoginForm/
│   │   │   └── SignupForm/
│   │   ├── hooks/               # Feature-specific hooks
│   │   │   ├── useAuth.ts
│   │   │   └── useLogin.ts
│   │   ├── services/            # API calls and business logic
│   │   │   └── authService.ts
│   │   ├── types/               # Feature-specific types
│   │   │   └── auth.types.ts
│   │   └── index.ts            # Feature exports
│   ├── dashboard/
│   ├── profile/
│   └── products/
├── hooks/                        # Global custom hooks
│   ├── useApi.ts
│   ├── useLocalStorage.ts
│   ├── useDebounce.ts
│   └── index.ts
├── services/                     # Global services
│   ├── api/
│   │   ├── client.ts            # API client configuration
│   │   ├── endpoints.ts         # API endpoints
│   │   └── types.ts            # API response types
│   ├── storage/
│   └── analytics/
├── store/                        # State management
│   ├── slices/                  # Redux Toolkit slices or Zustand stores
│   ├── providers/               # Context providers
│   ├── selectors/               # Reselect selectors
│   └── index.ts
├── utils/                        # Utility functions
│   ├── constants.ts
│   ├── helpers.ts
│   ├── formatters.ts
│   └── validators.ts
├── types/                        # Global type definitions
│   ├── api.ts
│   ├── common.ts
│   └── index.ts
├── styles/                       # Global styles
│   ├── globals.css
│   ├── variables.css
│   └── components.css
├── assets/                       # Static assets
│   ├── images/
│   ├── icons/
│   └── fonts/
├── pages/                        # Page components (if using file-based routing)
│   ├── HomePage/
│   ├── AboutPage/
│   └── NotFoundPage/
├── App.tsx                       # Main App component
├── main.tsx                      # Application entry point
└── vite-env.d.ts                # Environment type definitions

tests/
├── __mocks__/                    # Mock implementations
├── fixtures/                     # Test data
├── helpers/                      # Test utilities
├── setup.ts                     # Test setup configuration
└── integration/                  # Integration tests
```

## 🧪 React Testing Standards

### Testing Framework & Tools
- **Primary Framework**: Jest + React Testing Library for component testing
- **E2E Testing**: Playwright or Cypress for end-to-end testing
- **Visual Testing**: Storybook + Chromatic for visual regression testing
- **Component Testing**: Focus on behavior rather than implementation details
- **Accessibility Testing**: Use @testing-library/jest-dom and axe-core

### Testing Best Practices
- **User-Centric Testing**: Test components from the user's perspective
- **Query Priority**: Use getByRole, getByLabelText over getByTestId
- **Async Testing**: Proper async testing with waitFor and findBy queries
- **Mock Strategy**: Mock external dependencies, test component behavior
- **Component Isolation**: Test components in isolation with proper props

### Testing Patterns
```tsx
// Good: Testing behavior, not implementation
test('should submit form with valid data', async () => {
  const onSubmit = jest.fn();
  render(<ContactForm onSubmit={onSubmit} />);
  
  await user.type(screen.getByLabelText(/name/i), 'John Doe');
  await user.type(screen.getByLabelText(/email/i), 'john@example.com');
  await user.click(screen.getByRole('button', { name: /submit/i }));
  
  expect(onSubmit).toHaveBeenCalledWith({
    name: 'John Doe',
    email: 'john@example.com'
  });
});
```

## 🚫 React Anti-Patterns

### Component Design Issues
- **Prop Drilling**: Passing props through multiple component levels unnecessarily
- **Large Components**: Creating monolithic components with too many responsibilities
- **Inline Object Creation**: Creating objects/functions in render that cause unnecessary re-renders
- **Direct DOM Manipulation**: Bypassing React's virtual DOM with direct DOM access
- **Key Misuse**: Using array indices as keys for dynamic lists

### Performance Problems
- **Unnecessary Re-renders**: Not using React.memo, useMemo, or useCallback appropriately
- **Effect Dependencies**: Missing or incorrect dependencies in useEffect
- **State Structure**: Storing derived state instead of computing it
- **Large Bundle Sizes**: Not implementing proper code splitting
- **Memory Leaks**: Not cleaning up subscriptions and event listeners

### State Management Issues
- **Global State Overuse**: Putting everything in global state instead of local state
- **State Mutation**: Directly mutating state objects
- **Complex State Logic**: Not using useReducer for complex state transitions
- **Context Overuse**: Using Context for frequently changing values
- **Stale Closures**: Accessing stale values in useEffect or event handlers

## 🎯 React Best Practices

### Performance Optimization
- **Component Memoization**: Use React.memo for expensive components
- **Hook Optimization**: Optimize expensive calculations with useMemo
- **Callback Optimization**: Memoize callbacks with useCallback
- **Bundle Splitting**: Implement route-based and component-based code splitting
- **Image Optimization**: Use proper image loading and optimization techniques

### Accessibility (a11y)
- **Semantic HTML**: Use proper semantic HTML elements
- **ARIA Attributes**: Implement appropriate ARIA labels and roles
- **Keyboard Navigation**: Ensure full keyboard accessibility
- **Screen Reader Support**: Test with screen readers
- **Color Contrast**: Maintain proper color contrast ratios

### Development Workflow
- **Component Documentation**: Use Storybook for component documentation
- **Type Safety**: Leverage TypeScript for better development experience
- **Linting**: Use ESLint with React-specific rules
- **Formatting**: Use Prettier for consistent code formatting
- **Testing**: Write comprehensive tests for components and hooks

### Production Considerations
- **Error Handling**: Implement proper error boundaries and error reporting
- **Performance Monitoring**: Use React DevTools and performance monitoring tools
- **SEO Optimization**: Implement proper meta tags and server-side rendering if needed
- **Security**: Follow security best practices for client-side applications
- **Analytics**: Implement proper user analytics and event tracking

## 📚 Reference Links

### Official Documentation
- [React Documentation](https://react.dev/)
- [React Hooks Reference](https://react.dev/reference/react)
- [React Testing Library](https://testing-library.com/docs/react-testing-library/intro/)
- [Create React App](https://create-react-app.dev/docs/getting-started/)

### Essential Tools & Libraries
- [Vite React Plugin](https://vitejs.dev/guide/)
- [React Router](https://reactrouter.com/en/main)
- [React Query](https://tanstack.com/query/latest)
- [Zustand State Management](https://github.com/pmndrs/zustand)
- [React Hook Form](https://react-hook-form.com/)

### Style Guides & Best Practices
- [React TypeScript Cheatsheet](https://react-typescript-cheatsheet.netlify.app/)
- [React Patterns](https://reactpatterns.com/)
- [Kent C. Dodds Testing](https://kentcdodds.com/blog/?q=testing)
- [React Performance Guide](https://react.dev/learn/render-and-commit)
- Use React composition patterns (render props, children as functions)

### State Management
- Use `useState` for local component state
- Implement `useReducer` for complex state logic
- Leverage `useContext` for sharing state across component trees
- Consider external state management (Redux Toolkit, Zustand) for complex applications
- Implement proper state normalization and data structures
- Use React Query or SWR for server state management

### Hooks and Effects
- Use `useEffect` with proper dependency arrays to avoid infinite loops
- Implement cleanup functions in effects to prevent memory leaks
- Use `useMemo` and `useCallback` for performance optimization when needed
- Create custom hooks for reusable stateful logic
- Follow the rules of hooks (only call at the top level)
- Use `useRef` for accessing DOM elements and storing mutable values

### Styling
- Use CSS Modules, Styled Components, or modern CSS-in-JS solutions
- Implement responsive design with mobile-first approach
- Follow BEM methodology or similar naming conventions for CSS classes
- Use CSS custom properties (variables) for theming
- Implement consistent spacing, typography, and color systems
- Ensure accessibility with proper ARIA attributes and semantic HTML

### Performance Optimization
- Use `React.memo` for component memoization when appropriate
- Implement code splitting with `React.lazy` and `Suspense`
- Optimize bundle size with tree shaking and dynamic imports
- Use `useMemo` and `useCallback` judiciously to prevent unnecessary re-renders
- Implement virtual scrolling for large lists
- Profile components with React DevTools to identify performance bottlenecks

### Data Fetching
- Use modern data fetching libraries (React Query, SWR, Apollo Client)
- Implement proper loading, error, and success states
- Handle race conditions and request cancellation
- Use optimistic updates for better user experience
- Implement proper caching strategies
- Handle offline scenarios and network errors gracefully

### Error Handling
- Implement React Error Boundaries for component-level error handling
- Use proper error states in React data fetching
- Implement fallback UI for React error scenarios
- Log errors appropriately for React debugging
- Handle async errors in React effects and event handlers
- Provide meaningful error messages to users in React components

### Forms and Validation
- Use controlled components for form inputs
- Implement proper form validation with libraries like Formik, React Hook Form
- Handle form submission and error states appropriately
- Implement accessibility features for forms (labels, ARIA attributes)
- Use debounced validation for better user experience
- Handle file uploads and complex form scenarios

### Routing
- Use React Router for client-side routing
- Implement nested routes and route protection
- Handle route parameters and query strings properly
- Implement lazy loading for route-based code splitting
- Use proper navigation patterns and back button handling
- Implement breadcrumbs and navigation state management

### Testing
- Write unit tests for React components using React Testing Library
- Test React component behavior, not implementation details
- Use Jest for test runner with React-specific testing patterns
- Implement integration tests for complex React component interactions
- Mock external dependencies and API calls in React tests
- Test React accessibility features and keyboard navigation

### Security
- Sanitize user inputs to prevent XSS attacks
- Validate and escape data before rendering
- Use HTTPS for all external API calls
- Implement proper authentication and authorization patterns
- Avoid storing sensitive data in localStorage or sessionStorage
- Use Content Security Policy (CSP) headers

### Accessibility
- Use semantic HTML elements appropriately
- Implement proper ARIA attributes and roles
- Ensure keyboard navigation works for all interactive elements
- Provide alt text for images and descriptive text for icons
- Implement proper color contrast ratios
- Test with screen readers and accessibility tools

## React Implementation Process
1. Plan React component architecture and data flow
2. Set up React project structure with proper folder organization
3. Define React-specific TypeScript interfaces and types
4. Implement core React components with proper styling
5. Add React state management and data fetching logic
6. Implement React routing and navigation
7. Add React form handling and validation
8. Implement React error handling and loading states
9. Add testing coverage for React components and functionality
10. Optimize React performance and bundle size
11. Ensure React accessibility compliance
12. Add React documentation and code comments

## React-Specific Guidelines
- Follow React's naming conventions (PascalCase for components, camelCase for functions)
- Use meaningful commit messages and maintain clean git history for React projects
- Implement proper React code splitting and lazy loading strategies
- Document complex React components and custom hooks with JSDoc
- Use React Developer Tools for debugging and performance analysis
- Keep React dependencies up to date and audit for security vulnerabilities
- Implement proper environment configuration for different React deployment stages
- Use React-specific ESLint rules and Prettier configurations

## React Patterns
- Higher-Order Components (HOCs) for React cross-cutting concerns
- Render props pattern for React component composition
- Compound components for related React functionality
- Provider pattern for React context-based state sharing
- Container/Presentational React component separation
- Custom React hooks for reusable logic extraction