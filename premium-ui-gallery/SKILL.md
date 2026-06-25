---
name: premium-ui-gallery
description: This skill should be used when the user asks to design, redesign, or implement high-end, polished frontend UI — landing pages, SaaS marketing sites, navbars, CTAs, components, branding/color systems, or iconography — and wants the agent to draw inspiration from a curated set of professional design galleries. It bundles a curated knowledge base of 10 design-inspiration resources (curated.design / Craftwork, landing.love, saaspo, navbar.gallery, cta.gallery, mobbin, rebrand.gallery, hugeicons, component.gallery, godly / recent.design), a routing table that maps each UI section to the best gallery to consult, and a high-end UI design checklist. Use it whenever the user says things like "make this look premium", "借鉴这些设计画廊", "参考 landing.love / mobbin / navbar.gallery", "高端前端 UI", or explicitly invokes one of the listed galleries.
---

# Premium UI Gallery

## Overview

Produce high-end frontend UI by consulting a curated set of professional design-inspiration galleries, extracting the specific pattern the task needs, and synthesizing it into production code that follows a high-end design checklist. The skill encodes what each of the 10 galleries is good for, the URL patterns for browsing them, and the design principles that separate premium UI from generic UI.

## When to use

Invoke this skill when the user:

- Asks to build or improve a landing page, marketing site, SaaS site, dashboard, or app screen and wants it to look "premium", "high-end", "professional", or "像顶级 SaaS 那样".
- Explicitly references one or more of: curated.design, landing.love, saaspo, navbar.gallery, cta.gallery, mobbin, rebrand.gallery, hugeicons, component.gallery, godly / recent.design.
- Wants inspiration for a specific UI element: navbar, hero, pricing, CTA button, form, card, footer, brand colors, icon set, mobile pattern, etc.
- Says "借鉴 / 参考 / 看一下" these galleries, or asks the agent to browse them for ideas.

Do **not** invoke for backend logic, data modeling, or pure functionality work with no visual surface.

## Workflow

Follow these steps in order. Skip a step only with a clear reason.

### 1. Identify the UI surface and section

Ask, or infer from the request, the answers to:

- **Surface**: landing page, dashboard, mobile app screen, marketing site, component, icon set, brand system?
- **Section(s)**: hero, navbar, CTA, pricing, feature grid, testimonial, footer, form, onboarding screen, settings, etc.?
- **Style direction**: minimal, dark mode, 3D/WebGL, gradient, retro, illustration-heavy, enterprise-clean, playful?
- **Constraints**: framework (React/Vue/HTML), responsive, accessibility, performance budget?

### 2. Route to the right gallery

Consult `references/galleries.md` and pick the 1–2 best galleries for the section and style. The routing table at the top of that file maps section → gallery. Prefer galleries with live, high-quality examples over generic stock.

If the user already named a gallery, honor that and go straight to its section in `references/galleries.md`.

### 3. Extract the pattern, not the pixels

From the chosen gallery, identify:

- **Layout system**: grid, flex, container width, vertical rhythm, spacing scale.
- **Typography**: font family, size scale, weight pairs, line-height, letter-spacing.
- **Color system**: background, surface, text, accent, border, state (hover/active/disabled). Note contrast ratios and whether it's a dark or light theme.
- **Motion**: entry animation, hover state, scroll-triggered effect, micro-interaction timing/easing.
- **Asset choices**: icon style (stroke / duotone / solid), imagery (3D, photo, illustration), density.
- **Content shape**: how many words in the hero headline, how the value prop is structured, social proof placement.

Do not copy a site's copy or imagery verbatim. Extract the *pattern* and rewrite.

### 4. Apply the high-end UI checklist

Before writing code, cross-check the design against `references/design-principles.md`. Premium UI consistently satisfies these — generic UI skips them. Resolve every "weak" item before shipping.

### 5. Implement with semantic, production-ready code

- Use semantic HTML (`header`, `nav`, `main`, `section`, `article`, `footer`).
- Establish a design-token layer (CSS custom properties or Tailwind config) for color, spacing, type, radius, shadow, motion.
- Choose a type system (e.g. Inter/Geist for UI, a serif for editorial contrast, or a display face for hero) and stick to a 4–6 step scale.
- Add real interactive states: hover, focus-visible, active, disabled. No static mockups.
- Respect `prefers-reduced-motion` and `prefers-color-scheme`.
- Keep CSS organized: tokens → base → components → utilities.
- Use `hugeicons` (or similar consistent family) for icons — never mix stroke + solid across one UI.

### 6. Verify and refine

- Render and screenshot the result. Compare against the inspiration gallery entry that drove the design.
- Check spacing rhythm (does the vertical cadence feel consistent?), contrast (WCAG AA minimum), and motion (does it feel intentional, not decorative?).
- If something looks generic, return to step 2 and pull a stronger reference.

## Resources

### references/galleries.md

The full curated knowledge base. Contains a **routing table** at the top (UI section → recommended gallery) and one detailed section per gallery covering:

- What it curates and what it's best for
- URL structure and browsing patterns
- Concrete takeaways the agent should apply

Load this file when step 2 (routing) or step 3 (extraction) runs. The routing table alone is small enough to skim; the per-gallery sections are read on demand.

### references/design-principles.md

A distilled checklist of what separates high-end UI from generic UI: typography, color, spacing, motion, imagery, hierarchy, microinteractions, and accessibility. Apply this at step 4 before implementing. Treat it as a hard gate — every "weak" item must be resolved.

## Output expectations

The final deliverable is real, runnable frontend code (HTML/CSS/JS, React, Vue, etc. as the project requires) that:

1. Clearly traces its design language to a specific gallery entry or pattern.
2. Satisfies the design-principles checklist.
3. Uses a consistent design-token system and one icon family.
4. Has real interactive states and respects motion/accessibility preferences.
5. Looks like it could ship on a real product page — not a tutorial mockup.

When presenting the result, briefly cite which gallery inspired which section so the user can verify the lineage.
