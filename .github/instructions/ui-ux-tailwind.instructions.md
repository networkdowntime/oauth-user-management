---
description: UI/UX design standards and component patterns using Tailwind CSS
applyTo: "**/*.css,**/*.scss,**/*.html"
---
# UI/UX Design Standards with Tailwind CSS

## 1. Purpose
Establish consistent, accessible, and scalable UI design and development practices using Tailwind CSS. Ensure components are mobile-first, performant, and reusable across projects.

## 2. Scope
Covers core UI primitives, layout patterns, component spacing, and standardized implementations of tables, lists, modals, headers, sidebars, and interactive elements.

## 3. Design System Standards

- **Styling Framework**: Tailwind CSS (v3+), configured with extended theme for colors, typography, spacing.
- **Icons**: Heroicons, Lucide, or Feather Icons for consistency.
- **Typography**: Tailwind typography plugin (`prose`) for content-heavy sections.
- **Design Tokens**: Centralized color palette, spacing scale, and component variants.
- **Documentation**: Component library with design specifications and usage guidelines.

## 4. General UI/UX Design Best Practices

### 4.1 Spacing System
- Use Tailwind's spacing scale (`p-2`, `m-4`, `gap-6`, etc.).
- **Component internal padding**: `p-4` default for cards, modals, sections.
- **Between sections**: `mb-6` or `mt-8` depending on layout direction.
- **Grid/list spacing**: `gap-4` to `gap-6` for most items.
- Avoid inline styles — extend the Tailwind theme if necessary.

### 4.2 Responsive Layouts
- Use `grid`, `flex`, and responsive utilities like `sm:`, `md:`, `lg:`, `xl:`.
- Prioritize mobile layouts first (`flex-col`, `w-full`, etc.) and scale up.

### 4.3 Typography & Colors
- Use Tailwind typography plugin (`prose`) for content-heavy components.
- Semantic HTML (e.g., `<h1>`, `<section>`, `<nav>`) with Tailwind classes (`text-xl font-semibold`, etc.).
- Maintain contrast: use Tailwind’s `text-gray-800` on `bg-white` or dark-mode variants.
- Establish and enforce a design token system (in `tailwind.config.js`) for primary colors, border radius, box shadow, etc.

## 5. Common UI Components

### 5.1 Tables
- Responsive wrapper with horizontal scroll: `overflow-x-auto`.
- Use `<thead>`, `<tbody>`, `<tr>`, `<th>`, `<td>` with `text-left`, `px-4`, `py-2`.
- Apply zebra-striping: `odd:bg-gray-50` or `even:bg-white`.
- Support sorting and pagination with controlled state.
- Minimum column padding: `px-4`, row padding: `py-2`.

### 5.2 Lists (Cards or Rows)
- Use `ul > li` with consistent spacing: `mb-4` or `gap-4`.
- For grid-style lists: `grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6`.
- Cards: `bg-white rounded-2xl shadow-md p-4`.
- Include optional avatars or icons via `flex items-center gap-3`.

### 5.3 Modals
- Use `fixed inset-0 bg-black/50 z-50 flex items-center justify-center`.
- Modal container: `bg-white rounded-xl p-6 w-full max-w-md shadow-xl`.
- Include focus management, keyboard support (`Esc` to close), and ARIA roles:
  - `role="dialog"` with `aria-modal="true"` and accessible labeling.
- Consider using headless UI libraries for accessibility compliance.

### 5.4 Headers (App Top Bar)
- Sticky: `sticky top-0 z-40 bg-white shadow`.
- Layout: `flex justify-between items-center px-6 py-4`.
- Title: `text-lg font-semibold text-gray-800`.
- Right-side actions: buttons or icons spaced with `gap-4`.

### 5.5 Sidebars
- Fixed or collapsible: `w-64 h-screen bg-gray-100 border-r`.
- Mobile: toggleable using `sm:hidden` / `block`.
- Navigation structure:
  - `<nav>` with list: `flex flex-col gap-2 p-4`.
  - Active link style: `bg-blue-100 text-blue-700 font-medium`.

## 6. Accessibility (WCAG 2.1 AA)

- All components must be keyboard navigable.
- Use semantic HTML first (`<button>`, `<label>`, etc.) and ARIA only as fallback.
- Ensure screen reader compatibility with `aria-label`, `aria-labelledby`, and `aria-describedby`.
- Validate forms with accessible error messages using `aria-invalid` and `aria-describedby`.

## 7. Performance Guidelines

- Use progressive loading for images with `loading="lazy"` attribute.
- Minimize unused CSS by configuring Tailwind's purge/content settings.
- Optimize font loading with `font-display: swap` and preload critical fonts.
- Use CSS containment (`contain: layout style paint`) for isolated components.
- Implement efficient CSS custom properties for theming.

## 8. Component Design Workflow

- **Design System First**: Establish design tokens and component specifications before implementation.
- Each component must:
  - Support theming (light/dark mode).
  - Include loading, empty, and error states.
  - Be responsive with defined breakpoints.
  - Be accessible (WCAG 2.1 AA compliant).
- Design specifications should include:
  - Visual hierarchy and spacing
  - Interactive states (hover, focus, active, disabled)
  - Accessibility requirements

## 9. Example Tailwind Utility Patterns

| Use Case            | Tailwind Classes Example                                      |
|---------------------|---------------------------------------------------------------|
| Standard Card       | `bg-white p-4 rounded-2xl shadow-sm`                          |
| Action Button       | `bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700`|
| Section Container   | `max-w-7xl mx-auto px-4 sm:px-6 lg:px-8`                      |
| Grid List           | `grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6`        |
| Modal Overlay       | `fixed inset-0 bg-black/50 z-50 flex items-center justify-center` |
| Table Header Cell   | `text-left text-sm font-semibold text-gray-600 px-4 py-2`     |

## 10. Advanced UI Patterns

### 10.1 Design Tokens Configuration
```css
/* tailwind.config.js example */
module.exports = {
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#f0f9ff',
          500: '#3b82f6',
          900: '#1e3a8a'
        }
      },
      spacing: {
        '18': '4.5rem',
        '88': '22rem'
      }
    }
  }
}
```

### 10.2 Component State Classes
- **Default**: Base styling with neutral colors
- **Hover**: `hover:` utilities for interactive feedback
- **Focus**: `focus:ring-2 focus:ring-blue-500 focus:outline-none`
- **Active**: `active:` utilities for pressed states
- **Disabled**: `disabled:opacity-50 disabled:cursor-not-allowed`

### 10.3 Dark Mode Implementation
- Use `dark:` variant utilities for dark mode styles
- Implement CSS custom properties for seamless theme switching
- Ensure sufficient contrast ratios in both themes

## 11. Utility Enhancement Libraries
- **clsx** or **classnames** for conditional class handling
- **Tailwind Variants** or **cva** for managing component variants
- **Headless UI** libraries for accessible, unstyled components

## 12. Documentation & Design Handoff
- All components should be documented with:
  - Design specifications and usage guidelines
  - Accessibility requirements and testing results
  - Responsive behavior across breakpoints
  - Interactive state definitions
- Design handoff should include:
  - Complete design system documentation
  - Component specifications with spacing, colors, and typography
  - Accessibility annotations and requirements
  - Implementation guidelines and best practices
