# BEM Quick Reference Guide

## 🎯 Quick Component Lookup

### Stats Card
```html
<div class="stats-card stats-card--info">
  <div class="stats-card__overlay"></div>
  <div class="stats-card__content">
    <div class="stats-card__icon-wrapper">
      <div class="stats-card__icon-container">
        <div class="stats-card__icon-glow"></div>
        <div class="stats-card__icon">
          <i class="bi bi-icon"></i>
        </div>
      </div>
    </div>
    <div class="stats-card__text-content">
      <h3 class="stats-card__label">Label</h3>
      <div class="stats-card__value-wrapper">
        <span class="stats-card__value">123</span>
      </div>
      <p class="stats-card__sublabel">Description</p>
    </div>
  </div>
  <div class="stats-card__accent-line"></div>
</div>
```

**Variants**: `--info`, `--warning`, `--primary`, `--success`, `--danger`

---

### Button
```html
<button class="button button--primary button--small button--pill">
  <i class="button__icon bi bi-plus"></i>
  Text
</button>
```

**Variants**: `--primary`, `--secondary`, `--ghost`, `--success`, `--danger`  
**Sizes**: `--small`, `--large`  
**Shapes**: `--pill`, `--square`

---

### Toolbar Filter
```html
<div class="toolbar">
  <div class="toolbar__filters">
    <div class="toolbar__filter-group">
      <i class="toolbar__filter-icon bi bi-search"></i>
      <input type="text" class="toolbar__filter-input" placeholder="...">
    </div>
  </div>
</div>
```

---

### Table
```html
<div class="card">
  <div class="table-container">
    <table class="table">
      <thead>
        <tr class="table__header-row">
          <th class="table__header-cell">Header</th>
        </tr>
      </thead>
      <tbody>
        <tr class="table__row">
          <td class="table__cell">Data</td>
        </tr>
      </tbody>
    </table>
  </div>
</div>
```

---

## 🎨 Color Variants

| Variant | Use Case | Color |
|---------|----------|-------|
| `--info` | Information, neutral metrics | Cyan |
| `--warning` | Warnings, pending items | Yellow |
| `--primary` | Primary actions, key metrics | Blue |
| `--success` | Success states, positive metrics | Green |
| `--danger` | Errors, destructive actions | Red |

---

## 📐 Spacing Scale

| Variable | Value | Pixels |
|----------|-------|--------|
| `--spacing-1` | 0.25rem | 4px |
| `--spacing-2` | 0.5rem | 8px |
| `--spacing-3` | 0.75rem | 12px |
| `--spacing-4` | 1rem | 16px |
| `--spacing-5` | 1.25rem | 20px |
| `--spacing-6` | 1.5rem | 24px |
| `--spacing-8` | 2rem | 32px |

---

## 🔤 Typography Scale

| Variable | Value | Pixels |
|----------|-------|--------|
| `--font-size-xs` | 0.75rem | 12px |
| `--font-size-sm` | 0.875rem | 14px |
| `--font-size-base` | 1rem | 16px |
| `--font-size-lg` | 1.125rem | 18px |
| `--font-size-xl` | 1.25rem | 20px |
| `--font-size-2xl` | 1.5rem | 24px |
| `--font-size-3xl` | 1.875rem | 30px |

---

## 📱 Responsive Breakpoints

| Breakpoint | Min Width | Columns (Stats Grid) |
|------------|-----------|---------------------|
| Mobile | < 768px | 1 |
| Tablet | 768px | 2 |
| Desktop | 1024px | 3 |

---

## ✨ Common Utility Classes

### Spacing
- `u-mb-4` - Margin bottom (16px)
- `u-mb-8` - Margin bottom (32px)
- `u-mt-4` - Margin top (16px)
- `u-p-6` - Padding all sides (24px)

### Flexbox
- `u-flex` - Display flex
- `u-flex-col` - Flex direction column
- `u-items-center` - Align items center
- `u-justify-end` - Justify content end
- `u-gap-2` - Gap 8px
- `u-gap-4` - Gap 16px

### Text
- `u-text-center` - Text align center
- `u-text-danger` - Danger color text
- `u-font-bold` - Bold font weight

### Effects
- `u-shadow-lg` - Large shadow
- `u-shadow-xl` - Extra large shadow
- `u-rounded` - Border radius 12px

---

## 🎯 BEM Naming Cheatsheet

### Block
The standalone component:
```css
.stats-card { }
.button { }
.table { }
```

### Element
Part of a block (use `__`):
```css
.stats-card__label { }
.button__icon { }
.table__cell { }
```

### Modifier
Variation of block or element (use `--`):
```css
.stats-card--info { }
.button--primary { }
.table__cell--bold { }
```

### ❌ Don't Do This
```css
/* Too deep nesting */
.stats-card__content__icon__wrapper { }

/* Mixing block names */
.stats-card__button { }

/* Using element as standalone */
<div class="stats-card__label"></div> <!-- Missing parent block -->
```

### ✅ Do This
```css
/* Flat structure */
.stats-card__icon-wrapper { }

/* Separate blocks */
.stats-card { }
.button { }

/* Proper nesting */
<div class="stats-card">
  <h3 class="stats-card__label"></h3>
</div>
```

---

## 🔍 Accessibility Checklist

- [ ] All images have alt text
- [ ] Icon-only buttons have `aria-label`
- [ ] Form inputs have labels or `aria-label`
- [ ] Focus states are visible
- [ ] Color contrast meets WCAG AA (4.5:1)
- [ ] Touch targets are 44x44px minimum
- [ ] Keyboard navigation works
- [ ] Semantic HTML used

---

## 🚀 Performance Tips

1. **Use CSS Variables** - Easier theming, better maintainability
2. **Minimize Specificity** - Faster CSS matching
3. **Avoid Layout Thrashing** - Don't animate `width`, `height`, `top`, `left`
4. **Prefer Transforms** - Use `transform` and `opacity` for animations
5. **Lazy Load Images** - Use `loading="lazy"` attribute

---

## 🐛 Common Issues & Solutions

### Issue: Stats card hover not working
**Solution**: Ensure all required elements are present:
```html
<div class="stats-card__overlay"></div> <!-- Required -->
<div class="stats-card__accent-line"></div> <!-- Required -->
```

### Issue: Button icon misaligned
**Solution**: Use `.button__icon` class:
```html
<i class="button__icon bi bi-plus"></i>
```

### Issue: Table not scrolling on mobile
**Solution**: Wrap table in `.table-container`:
```html
<div class="table-container">
  <table class="table">...</table>
</div>
```

### Issue: Filter arrow not rotating
**Solution**: Toggle the modifier class with JavaScript:
```javascript
arrow.classList.toggle('toolbar__filter-arrow--open');
```

---

## 📦 File Structure

```
project/
├── service-registry-bem.css      # Main stylesheet
├── service-registry-bem.html     # Example implementation
├── BEM-DOCUMENTATION.md           # Full documentation
└── BEM-QUICK-REFERENCE.md         # This file
```

---

## 🎓 Learning Resources

### BEM Methodology
- [Official BEM Documentation](https://en.bem.info/)
- [BEM 101 by CSS-Tricks](https://css-tricks.com/bem-101/)

### CSS Custom Properties
- [MDN: Using CSS Custom Properties](https://developer.mozilla.org/en-US/docs/Web/CSS/Using_CSS_custom_properties)

### Accessibility
- [WCAG 2.1 Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)
- [WebAIM Contrast Checker](https://webaim.org/resources/contrastchecker/)

---

## 💡 Pro Tips

1. **Consistent Naming**: Always use lowercase with hyphens
2. **Single Responsibility**: Each class should do one thing
3. **Composition Over Inheritance**: Combine classes instead of extending
4. **Mobile First**: Design for mobile, enhance for desktop
5. **Test Across Browsers**: Don't assume it works everywhere
6. **Document Changes**: Update docs when adding components

---

**Quick Start**: Copy a component from `service-registry-bem.html`, modify the content, and you're done! 🎉
