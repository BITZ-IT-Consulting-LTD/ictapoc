# WCAG 2.1 AA/AAA Accessibility Implementation Guide

## Overview
This application implements WCAG 2.1 Level AA compliance with AAA enhancements where feasible. This guide documents the accessibility features and best practices for developers.

## Color Contrast Compliance

### Text Colors (WCAG 1.4.3 & 1.4.6)
All text colors meet WCAG AAA standards (7:1 contrast ratio):

- **Primary Text** (`--text-main: #0f172a`): 15.3:1 contrast on white
- **Secondary Text** (`--text-muted: #475569`): 7.4:1 contrast on white
- **Status Colors**: All adjusted for minimum 4.5:1 contrast
  - Success: `#059669` (darker green)
  - Danger: `#dc2626` (adjusted red)
  - Warning: `#d97706` (darker amber)
  - Info: `#2563eb` (darker blue)

### Interactive Elements
- **Primary Button**: `#C41E3A` - WCAG AA compliant
- **Focus Indicators**: `#2563eb` - High contrast blue
- **Borders**: `#cbd5e1` - Enhanced visibility

## Keyboard Navigation (WCAG 2.1.1 & 2.4.7)

### Focus Management
All interactive elements have visible focus indicators:

```css
:focus-visible {
  outline: 3px solid var(--border-focus);
  outline-offset: 2px;
  border-radius: var(--radius-sm);
}
```

### Skip Links (WCAG 2.4.1)
Add skip navigation link at the top of your HTML:

```html
<a href="#main-content" class="skip-link">Skip to main content</a>
```

The skip link is hidden until focused via keyboard.

## Touch Target Sizes (WCAG 2.5.5)

All interactive elements meet the minimum 44x44px touch target size:

```css
--touch-target-min: 44px;
```

Applied to:
- All buttons (`.button`)
- Form inputs (`.form__input`, `.form__select`)
- Icon buttons (`.button--icon`)
- Navigation links

## Form Accessibility

### Required Fields (WCAG 3.3.2)
Mark required fields with visual and programmatic indicators:

```html
<div class="form__group">
  <label for="email" class="form__label form__label--required">
    Email Address
  </label>
  <input 
    type="email" 
    id="email" 
    name="email" 
    class="form__input"
    required
    aria-required="true"
    aria-describedby="email-helper"
  >
  <span id="email-helper" class="form__helper-text">
    We'll never share your email
  </span>
</div>
```

### Error States (WCAG 3.3.1 & 3.3.3)
Display clear error messages with visual and programmatic indicators:

```html
<div class="form__group">
  <label for="username" class="form__label form__label--required">
    Username
  </label>
  <input 
    type="text" 
    id="username" 
    class="form__input form__input--error"
    aria-invalid="true"
    aria-describedby="username-error"
  >
  <div id="username-error" class="form__error-message" role="alert">
    Username must be at least 3 characters
  </div>
</div>
```

## Screen Reader Support

### Screen Reader Only Content (WCAG 4.1.3)
Hide content visually but keep it accessible to screen readers:

```html
<span class="sr-only">Loading...</span>
<button aria-label="Close dialog">
  <span aria-hidden="true">×</span>
  <span class="sr-only">Close</span>
</button>
```

### ARIA Live Regions
For dynamic content updates:

```html
<!-- Polite announcements -->
<div aria-live="polite" aria-atomic="true" class="sr-only">
  Form submitted successfully
</div>

<!-- Urgent announcements -->
<div aria-live="assertive" aria-atomic="true" class="sr-only">
  Error: Connection lost
</div>
```

## Motion Preferences (WCAG 2.3.3)

The design system respects user motion preferences:

```css
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}
```

## High Contrast Mode

Support for users with high contrast preferences:

```css
@media (prefers-contrast: high) {
  :root {
    --border-color: #000000;
    --text-muted: #1f2937;
  }
}
```

## Component Accessibility Checklist

### Buttons
- ✅ Minimum 44x44px touch target
- ✅ Visible focus indicator
- ✅ Disabled state with `aria-disabled`
- ✅ Descriptive labels or `aria-label`
- ✅ Active/pressed state feedback

### Forms
- ✅ Associated labels with `for` attribute
- ✅ Required field indicators (visual + `aria-required`)
- ✅ Error messages with `aria-invalid` and `aria-describedby`
- ✅ Helper text linked via `aria-describedby`
- ✅ Disabled state clearly indicated

### Navigation
- ✅ Skip links for keyboard users
- ✅ Current page indicated with `aria-current="page"`
- ✅ Semantic `<nav>` landmarks
- ✅ Keyboard accessible dropdowns

### Modals/Dialogs
- ✅ `role="dialog"` and `aria-modal="true"`
- ✅ `aria-labelledby` pointing to title
- ✅ `aria-describedby` for description
- ✅ Focus trap within modal
- ✅ Return focus on close
- ✅ ESC key to close

### Tables
- ✅ `<th>` elements with `scope` attribute
- ✅ `<caption>` for table description
- ✅ Responsive horizontal scroll
- ✅ Row headers for data tables

## Testing Recommendations

### Automated Testing
- **axe DevTools**: Browser extension for automated accessibility testing
- **WAVE**: Web accessibility evaluation tool
- **Lighthouse**: Built into Chrome DevTools

### Manual Testing
1. **Keyboard Navigation**: Tab through entire interface
2. **Screen Reader**: Test with NVDA (Windows) or VoiceOver (Mac)
3. **Zoom**: Test at 200% zoom level
4. **Color Blindness**: Use color blindness simulators
5. **High Contrast**: Enable system high contrast mode

### Keyboard Shortcuts to Test
- `Tab`: Navigate forward
- `Shift + Tab`: Navigate backward
- `Enter`: Activate buttons/links
- `Space`: Toggle checkboxes, activate buttons
- `Esc`: Close modals/dialogs
- `Arrow keys`: Navigate within components (tabs, dropdowns)

## Common Patterns

### Accessible Button
```html
<button 
  class="button button--primary" 
  type="button"
  aria-label="Submit application"
>
  <span aria-hidden="true">→</span>
  Submit
</button>
```

### Accessible Icon Button
```html
<button 
  class="button button--icon" 
  type="button"
  aria-label="Delete item"
>
  <span aria-hidden="true">🗑</span>
  <span class="sr-only">Delete</span>
</button>
```

### Accessible Form Group
```html
<div class="form__group">
  <label for="password" class="form__label form__label--required">
    Password
  </label>
  <input 
    type="password" 
    id="password" 
    class="form__input"
    required
    aria-required="true"
    aria-describedby="password-requirements"
    minlength="8"
  >
  <span id="password-requirements" class="form__helper-text">
    Must be at least 8 characters with one number
  </span>
</div>
```

### Accessible Status Message
```html
<div 
  role="status" 
  aria-live="polite" 
  class="badge badge--success"
>
  <span aria-hidden="true">✓</span>
  Application approved
</div>
```

## Resources

- [WCAG 2.1 Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)
- [MDN Accessibility](https://developer.mozilla.org/en-US/docs/Web/Accessibility)
- [WebAIM](https://webaim.org/)
- [A11y Project](https://www.a11yproject.com/)
- [ARIA Authoring Practices](https://www.w3.org/WAI/ARIA/apg/)

## Support

For accessibility questions or issues, please contact the development team or file an issue in the project repository.
