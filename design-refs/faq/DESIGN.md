---
name: Pro-Service Editorial
colors:
  surface: '#f8f9ff'
  surface-dim: '#cbdbf5'
  surface-bright: '#f8f9ff'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#eff4ff'
  surface-container: '#e5eeff'
  surface-container-high: '#dce9ff'
  surface-container-highest: '#d3e4fe'
  on-surface: '#0b1c30'
  on-surface-variant: '#45464d'
  inverse-surface: '#213145'
  inverse-on-surface: '#eaf1ff'
  outline: '#76777d'
  outline-variant: '#c6c6cd'
  surface-tint: '#565e74'
  primary: '#000000'
  on-primary: '#ffffff'
  primary-container: '#131b2e'
  on-primary-container: '#7c839b'
  inverse-primary: '#bec6e0'
  secondary: '#0058be'
  on-secondary: '#ffffff'
  secondary-container: '#2170e4'
  on-secondary-container: '#fefcff'
  tertiary: '#000000'
  on-tertiary: '#ffffff'
  tertiary-container: '#191c1e'
  on-tertiary-container: '#818486'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#dae2fd'
  primary-fixed-dim: '#bec6e0'
  on-primary-fixed: '#131b2e'
  on-primary-fixed-variant: '#3f465c'
  secondary-fixed: '#d8e2ff'
  secondary-fixed-dim: '#adc6ff'
  on-secondary-fixed: '#001a42'
  on-secondary-fixed-variant: '#004395'
  tertiary-fixed: '#e0e3e5'
  tertiary-fixed-dim: '#c4c7c9'
  on-tertiary-fixed: '#191c1e'
  on-tertiary-fixed-variant: '#444749'
  background: '#f8f9ff'
  on-background: '#0b1c30'
  surface-variant: '#d3e4fe'
typography:
  display-lg:
    fontFamily: Epilogue
    fontSize: 72px
    fontWeight: '800'
    lineHeight: 80px
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Epilogue
    fontSize: 48px
    fontWeight: '700'
    lineHeight: 56px
    letterSpacing: -0.01em
  headline-lg-mobile:
    fontFamily: Epilogue
    fontSize: 32px
    fontWeight: '700'
    lineHeight: 40px
    letterSpacing: -0.01em
  headline-md:
    fontFamily: Epilogue
    fontSize: 30px
    fontWeight: '600'
    lineHeight: 38px
  body-lg:
    fontFamily: Inter
    fontSize: 18px
    fontWeight: '400'
    lineHeight: 28px
  body-md:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  label-md:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '600'
    lineHeight: 20px
    letterSpacing: 0.05em
rounded:
  sm: 0.125rem
  DEFAULT: 0.25rem
  md: 0.375rem
  lg: 0.5rem
  xl: 0.75rem
  full: 9999px
spacing:
  unit: 8px
  container-max: 1280px
  gutter: 24px
  margin-mobile: 16px
  margin-desktop: 48px
  stack-sm: 8px
  stack-md: 16px
  stack-lg: 32px
  section-padding: 120px
---

## Brand & Style

The design system is engineered for local service providers who aspire to a "premium-tier" market position. It bridges the gap between high-end editorial magazines and functional utility. The aesthetic is rooted in **Minimalism** with **Modern Corporate** precision, emphasizing clarity, structural integrity, and authority.

The emotional goal is to evoke "Quiet Confidence." By stripping away decorative clutter like heavy shadows and gradients, the design system allows the quality of the service—and the photography of the work—to lead. The interface acts as a high-end gallery for blue-collar and white-collar professional services alike.

## Colors

The palette is anchored by **Deep Charcoal** (Primary) to provide a sense of stability and institutional trust. **Service Blue** (Secondary) is the high-energy accent, reserved strictly for calls to action and critical status indicators to maintain its visual impact.

- **Primary (#0F172A):** Used for typography, heavy structural elements, and high-contrast backgrounds.
- **Secondary (#3B82F6):** The singular "Service Blue" accent. Use sparingly for interactive elements.
- **Surface (#F8FAFC):** A crisp, off-white background that reduces eye strain compared to pure white.
- **Muted (#64748B):** Used for secondary text, borders, and decorative rules to create hierarchy without noise.

## Typography

This design system uses a high-contrast pairing to achieve an editorial feel. **Epilogue** provides a bold, geometric, and authoritative voice for headlines. Its tight letter-spacing and heavy weights mimic high-end architectural or lifestyle journals. 

**Inter** is utilized for all functional and body copy, ensuring maximum legibility across all device types. For labels and small caps, increase letter spacing to maintain a "structured" and professional appearance. Large display headings should always use negative letter spacing to feel "locked-in" and intentional.

## Layout & Spacing

The layout follows a **Fixed Grid** philosophy for desktop to ensure content remains readable and premium. We utilize a 12-column grid with generous 24px gutters.

- **Vertical Rhythm:** A strict 8px/12px increment system. Elements should be spaced in multiples of 8 (e.g., 16, 32, 64).
- **Whitespace:** Emphasize large section padding (120px+) to separate distinct service offerings. This "breathable" space is what defines the premium feel.
- **Responsive Behavior:** On mobile, margins shrink to 16px, and the 12-column grid collapses into a single-column stack. Typography scales down specifically for `headline-lg` to prevent awkward word-breaking.

## Elevation & Depth

This design system rejects heavy shadows in favor of **Tonal Layering** and **Low-Contrast Outlines**. 

Depth is communicated through:
- **1px Rules:** Use subtle `#E2E8F0` borders to define card boundaries and section breaks.
- **Background Shifts:** Moving from a pure white surface to a `#F8FAFC` container creates a subtle sense of "lifting" without the need for blurs.
- **Image Crops:** Use sharp, hard-edged containers for imagery. When a "hover" state is required, a simple 1px inset border or a slight grayscale-to-color transition is preferred over a drop shadow.

## Shapes

The shape language is "Soft-Mechanical." While the brand is modern, it avoids overly "bubbly" or playful curves. 

- **Standard Radius:** 4px (Soft) for most components to provide a hint of approachability.
- **Interactive Radius:** 8px (Large) for primary buttons to make them feel more tactile and distinct from the surrounding structural grid.
- **Imagery:** Strictly square or 4px rounded corners. Do not use circles or organic shapes for image masks.

## Components

### Buttons
- **Primary:** Solid `#0F172A` background with white text. High-contrast and authoritative.
- **Secondary (Outline):** 1px border in `#0F172A`. Clean and sophisticated.
- **Tertiary:** Text-only with a trailing 16px arrow icon (→). Used for "Learn More" links within editorial layouts.

### Input Fields
Inputs should be minimalist: a 1px border on the bottom only, or a very light 4-sided border. Use `Inter` at 16px for input text to prevent iOS zoom-on-focus. Labels should use the `label-md` style, positioned above the field.

### Cards
Cards should not have shadows. Use a 1px border in `#E2E8F0`. Padding inside cards should be generous (minimum 32px) to maintain the editorial feel.

### Lists & Feature Blocks
Features should be presented with high-quality icons (minimalist line-art) or small, high-contrast badges. Use the 8px grid to ensure icon-to-text alignment is pixel-perfect.

### Editorial Image Blocks
Images should often bleed to one edge of the container or utilize "offset" layouts where the image overlaps a background color block, reinforcing the grid-based architecture.