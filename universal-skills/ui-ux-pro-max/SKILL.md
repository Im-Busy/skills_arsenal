---
name: ui-ux-pro-max
description: AI-powered design intelligence toolkit with 161 reasoning rules, 67 UI styles, 161 color palettes, 57 font pairings, 25 chart types, 99 UX guidelines, and 15 tech stacks. Use when building ANY UI component, page, app, or dashboard. Automatically generates complete design systems from requirements.
version: 2.0
---

# UI UX Pro Max Skill

A searchable database of professional UI/UX design intelligence. Provides recommendations for styles, colors, typography, layouts, charts, UX best practices, and stack-specific guidelines across 161 product types.

## When to Use

Activate this skill when:
- Building any UI: landing pages, dashboards, forms, components, mobile apps
- The user asks for design help, UI recommendations, or style guidance
- Starting a new project and need a complete design system
- Need color palette recommendations for a specific industry/product
- Need font pairing recommendations
- Building a dashboard and need chart type recommendations
- Need UX best practices or anti-pattern warnings
- Need stack-specific UI guidelines (React, Vue, Tailwind, SwiftUI, Flutter, etc.)

## How to Use

### Step 1: Generate a Design System
When the user describes their project, run:
```
python3 search.py "{product type or description}" --design-system -p "{Project Name}"
```

This produces a complete design system with:
- Landing page pattern and section structure
- UI style recommendation with CSS keywords
- Color palette with specific hex values
- Typography pairing with Google Fonts import
- Key effects and animations
- Anti-patterns to avoid
- Pre-delivery checklist

### Step 2: Search Specific Domains
```
# UI Style recommendations
python3 search.py "minimalist dashboard" --domain style

# Color palettes
python3 search.py "fintech dark banking" --domain color

# Font pairings
python3 search.py "elegant serif luxury" --domain typography

# Landing page structure
python3 search.py "SaaS conversion" --domain landing

# Chart recommendations
python3 search.py "analytics dashboard" --domain chart

# UX best practices
python3 search.py "form validation accessibility" --domain ux

# Product type matching
python3 search.py "healthcare patient portal" --domain product

# Icon recommendations
python3 search.py "navigation icons" --domain icons

# App interface patterns
python3 search.py "mobile navigation" --domain app-interface

# Google Fonts search
python3 search.py "modern sans-serif" --domain google-fonts
```

### Step 3: Stack-Specific Guidelines
```
python3 search.py "responsive grid" --stack react
python3 search.py "form validation" --stack html-tailwind
python3 search.py "navigation" --stack flutter
python3 search.py "state management" --stack nextjs
```

Available stacks: react, nextjs, vue, svelte, astro, swiftui, react-native, flutter, html-tailwind, shadcn, jetpack-compose, angular, laravel, nuxtjs, nuxt-ui, threejs

### Domains Available
- `style` - 67 UI styles (Glassmorphism, Minimalism, Brutalism, Bento Grid, etc.)
- `color` - 161 industry-specific color palettes
- `typography` - 57 curated font pairings
- `landing` - 24 landing page patterns
- `chart` - 25 chart type recommendations
- `ux` - 99 UX best practices and anti-patterns
- `product` - 161 product type rules with reasoning
- `icons` - Icon libraries and guidelines
- `app-interface` - Mobile UI patterns
- `google-fonts` - Google Fonts database

### Reasoning Rules (161 Product Categories)

The engine matches these product categories to recommend appropriate design:

| Category | Examples |
|----------|----------|
| Tech & SaaS | SaaS, B2B Service, Developer Tool, AI Platform, Cybersecurity |
| Finance | Fintech, Banking, Insurance, Personal Finance |
| Healthcare | Medical Clinic, Pharmacy, Dental, Veterinary, Mental Health |
| E-commerce | General, Luxury, Marketplace, Subscription Box, Food Delivery |
| Services | Beauty/Spa, Restaurant, Hotel, Legal, Home Services |
| Creative | Portfolio, Agency, Photography, Gaming, Music |
| Lifestyle | Habit Tracker, Recipe, Meditation, Weather, Diary |
| Emerging Tech | Web3, Spatial Computing, Quantum, Drones |

Each rule includes:
- Recommended landing page pattern
- Style priorities (BM25 ranked)
- Color mood
- Typography mood
- Key effects and animations
- Anti-patterns (what NOT to do)

### Data Files

All data files live in this skill directory and can be accessed directly:
`C:\Dev\skills\ui-ux-pro-max\data\`

For detailed design principles, UX guidelines, and anti-patterns, see `ux-guidelines.csv`.
