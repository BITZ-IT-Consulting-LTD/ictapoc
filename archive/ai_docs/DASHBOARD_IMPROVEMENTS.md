# Dashboard View Improvements - Implementation Guide

## Changes Made

### 1. Added Sidebar Navigation Styles
- Added `.dashboard-layout` for grid-based sidebar + content layout
- Added `.dashboard-sidebar` for sticky sidebar positioning
- Added `.sidebar-nav` and `.sidebar-nav__item` for left-aligned navigation
- Responsive: stacks vertically on mobile, side-by-side on desktop (1024px+)

### 2. Required Template Changes

Replace the citizen portal horizontal tabs (lines 22-39) with this sidebar structure:

```vue
<!-- CITIZEN PORTAL VIEW -->
<section v-if="user.role === 'citizen'" class="citizen-portal">
  <div class="dashboard-layout">
    <!-- Left Sidebar Navigation -->
    <aside class="dashboard-sidebar">
      <div class="card">
        <div class="card__body p-0">
          <nav class="sidebar-nav" aria-label="Citizen portal navigation">
            <button 
              @click="citizenCurrentTab = 'inbox'"
              class="sidebar-nav__item"
              :class="{ 'sidebar-nav__item--active': citizenCurrentTab === 'inbox' }"
            >
              <i class="bi bi-envelope-paper-fill sidebar-nav__icon"></i>
              <span class="sidebar-nav__text">Official Inbox</span>
              <i v-if="citizenCurrentTab === 'inbox'" class="bi bi-chevron-right sidebar-nav__arrow"></i>
            </button>
            
            <button 
              @click="citizenCurrentTab = 'services'"
              class="sidebar-nav__item"
              :class="{ 'sidebar-nav__item--active': citizenCurrentTab === 'services' }"
            >
              <i class="bi bi-grid-3x3-gap-fill sidebar-nav__icon"></i>
              <span class="sidebar-nav__text">Service Catalogue</span>
              <i v-if="citizenCurrentTab === 'services'" class="bi bi-chevron-right sidebar-nav__arrow"></i>
            </button>
          </nav>
        </div>
      </div>
    </aside>

    <!-- Main Content Area -->
    <div class="dashboard-content">
      <!-- Keep existing tab content here -->
      <div v-if="citizenCurrentTab === 'inbox'" class="tab-content">
        <!-- Existing inbox content -->
      </div>
      
      <div v-if="citizenCurrentTab === 'services'" class="tab-content">
        <!-- Existing services content -->
      </div>
    </div>
  </div>
</section>
```

### 3. Key Features

✅ **Left-aligned sidebar navigation** - Consistent with admin panel  
✅ **Sticky positioning** - Sidebar stays visible while scrolling  
✅ **Active state indicator** - Left border + background highlight  
✅ **Hover effects** - Smooth transitions  
✅ **Responsive** - Mobile-friendly stacking  
✅ **Accessible** - Proper ARIA labels and keyboard navigation  
✅ **Icon + Text + Arrow** - Clear visual hierarchy  

### 4. Visual Design

- **Active State**: Primary color background with left border
- **Hover State**: Light gray background
- **Icons**: 1.125rem size for visibility
- **Spacing**: 1rem vertical padding for touch-friendly targets
- **Typography**: 0.9375rem font size, 600 weight (700 when active)

### 5. Layout Behavior

- **Mobile (<1024px)**: Sidebar stacks on top, full width
- **Desktop (≥1024px)**: Sidebar 280px wide, content fills remaining space
- **Sidebar**: Sticky positioning with 2rem top offset
- **Gap**: 2rem between sidebar and content

## Benefits

1. **Consistency**: Matches admin panel navigation pattern
2. **Better UX**: Easier to scan vertically aligned options
3. **More Space**: Horizontal space freed up for content
4. **Scalability**: Easy to add more navigation items
5. **Accessibility**: Better keyboard navigation and screen reader support

## Implementation Status

✅ Styles added to DashboardView.vue  
⏳ Template update required (manual step)  

## Next Steps

1. Update the citizen portal template section (lines 22-166)
2. Test responsive behavior on mobile and desktop
3. Verify accessibility with keyboard navigation
4. Consider applying same pattern to officer/staff view if needed
