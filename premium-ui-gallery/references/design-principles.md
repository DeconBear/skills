# High-End UI Design Checklist

This is the hard gate between "generic UI" and "premium UI". Run through it before shipping any frontend work produced under the `premium-ui-gallery` skill. Every weak item must be resolved or deliberately justified.

Use it as a self-audit: for each section, mark the work **Strong / Acceptable / Weak** and fix the Weak items.

---

## 1. Typography

- [ ] **Typeface choice is intentional**, not the default. Strong picks: Inter, Geist, Söhne, IBM Plex, General Sans, Switzer, Satoshi, Cabinet Grotesk, or a pairing with a serif (Fraunces, Editorial New, Source Serif). Avoid system-default `Arial` / `Times`.
- [ ] **Type scale has 4–6 steps**, not 10+. Use a modular scale (1.125, 1.2, 1.25, 1.333, 1.5 ratio) — display / h1 / h2 / h3 / body / small.
- [ ] **Display sizes are big enough** to be expressive — 56–120px on desktop for hero headlines on premium sites. Don't be shy.
- [ ] **Line-height is set by purpose**: tight (1.05–1.15) for display, normal (1.4–1.6) for body, loose (1.6+) for long-form.
- [ ] **Letter-spacing**: slightly negative (−0.01 to −0.04em) for large display type, normal for body, slightly positive (+0.02 to +0.08em) for ALL CAPS labels.
- [ ] **Font weights used purposefully**: 2–3 weights max per page (e.g. 400, 500, 700). Don't load the whole family.
- [ ] **Variable font** preferred when available — one file, all weights, smaller payload.
- [ ] **Self-hosted or properly preloaded** — no FOUT flash, no layout shift (`font-display: swap` + `size-adjust` or `next/font`).
- [ ] **Numerals are tabular** in tables/pricing (`font-variant-numeric: tabular-nums`).

## 2. Color

- [ ] **Token system in place** (`--color-bg`, `--color-surface`, `--color-text`, `--color-text-muted`, `--color-border`, `--color-accent`, `--color-success/warning/error`). No hex literals scattered through components.
- [ ] **Light AND dark mode considered** — at minimum, dark mode tokens defined. Respect `prefers-color-scheme`.
- [ ] **Contrast meets WCAG AA**: 4.5:1 for body, 3:1 for large text. Check the muted text — it almost always fails.
- [ ] **Accent color is used sparingly** — one primary accent, used 5–15% of the surface, not everywhere.
- [ ] **Surfaces have elevation, not just different grays** — use shadow, border, or a subtle gradient to separate layers.
- [ ] **No pure black (#000) or pure white (#fff)** in light/dark UIs unless deliberate. Use near-black (`#0A0A0A`) and near-white (`#FAFAFA`) for softer feel.
- [ ] **Gradient, if used, is restrained** — two stops, similar lightness, on a focused element (hero text, button hover, divider). Avoid rainbow gradients.

## 3. Spacing & Layout

- [ ] **8pt (or 4pt) grid** — every spacing value is a multiple of 4 or 8. Tokens: `xs/sm/md/lg/xl/2xl/3xl`.
- [ ] **Container width is intentional** — 1200–1440px for marketing, 1024–1280px for app. Centered, with horizontal padding.
- [ ] **Vertical rhythm is consistent** — section padding follows a regular cadence (e.g. 96/128/160px on desktop, 64/80px on mobile).
- [ ] **Whitespace is generous** — premium UIs breathe. When in doubt, add more space.
- [ ] **Grid is real** — use CSS Grid for the main layout, Flex for components. Avoid floats, avoid `inline-block` layout hacks.
- [ ] **Responsive is designed, not patched** — define breakpoints (`sm 640 / md 768 / lg 1024 / xl 1280 / 2xl 1536`) and reflow the layout at each, don't just shrink things.
- [ ] **Mobile-first or desktop-first is a conscious choice** — pick one and stay consistent.

## 4. Motion

- [ ] **Motion has a purpose** — entrance, attention, feedback, or spatial orientation. No decorative bouncing.
- [ ] **One easing curve family** — `cubic-bezier(0.22, 1, 0.36, 1)` (ease-out-quart) is a strong default for entrances. `cubic-bezier(0.4, 0, 0.2, 1)` (standard) for state changes.
- [ ] **Two durations** — fast (150–250ms) for micro-interactions, slow (400–800ms) for entrances. No in-between.
- [ ] **`prefers-reduced-motion` respected** — wrap all animation in a media query that disables transform/opacity-heavy motion.
- [ ] **Stagger is subtle** — 30–80ms between siblings, not 200ms+.
- [ ] **Scroll-driven motion is opt-in and brief** — pin/parallax for ≤1 viewport height, then release.
- [ ] **Loading states use skeleton or shimmer**, not spinners, for content. Spinners only for actions.
- [ ] **Page transitions** (if any) are <300ms and use a single property (opacity or transform), not both.

## 5. Imagery & Iconography

- [ ] **One icon family** — e.g. `hugeicons` stroke-rounded, Lucide, Phosphor, Tabler. Don't mix stroke + solid. Match corner radius to button radius.
- [ ] **Icons sized by context** — 16px in dense UI, 20–24px in chrome, 32–48px in hero/features.
- [ ] **Imagery is high-quality and consistent** — same illustration style, same photo treatment (B&W with one accent? Gradient overlay? Grain?).
- [ ] **3D / WebGL used purposefully** — one hero scene, not scattered. Falls back gracefully to a static image or video.
- [ ] **Logos in a logo wall are monochrome** — convert to a single tone unless the brand specifically requires color. Use `<img>` with `grayscale` filter or a CSS class.
- [ ] **All imagery is optimized** — modern formats (AVIF/WebP), `srcset` for responsive, `loading="lazy"` below the fold, `width`/`height` to prevent CLS.

## 6. Hierarchy & Focus

- [ ] **One primary action per view** — if there are two equal buttons, the design hasn't decided what it wants.
- [ ] **F-pattern or Z-pattern is intentional** — eye lands where the value prop is.
- [ ] **CTA above the fold** — visible without scrolling on a 1440×900 viewport.
- [ ] **Headline does the work** — sub-headline and supporting copy supplement; they don't compete.
- [ ] **Section transitions are marked** — eyebrow tag, divider, or generous whitespace separates sections.
- [ ] **Density matches content** — marketing is sparse, dashboards are dense, forms are medium. Don't mix.

## 7. Components & States

- [ ] **Every interactive element has hover, focus-visible, active, disabled** — no static mockups.
- [ ] **Focus rings are visible and styled** — don't `outline: none` without a replacement.
- [ ] **Buttons have a clear hierarchy**: primary (filled accent), secondary (outline or filled neutral), tertiary (text/link). Use them consistently.
- [ ] **Form inputs have labels (not just placeholders), helper text, and error states**.
- [ ] **Empty states have an illustration, a headline, and a primary action**.
- [ ] **Loading states are present** for async actions (button shows spinner, content shows skeleton).
- [ ] **Error states are friendly and actionable** — not "Error 500".

## 8. Accessibility

- [ ] **Semantic HTML** — `<header>`, `<nav>`, `<main>`, `<section>`, `<article>`, `<footer>`, `<button>`, `<a>`. Not `<div>` everywhere.
- [ ] **Heading order is logical** — h1 once per page, then h2, h3… no skipping levels.
- [ ] **Color is not the only signal** — error states use icon + color, links have underline or other cue, focus has ring.
- [ ] **Keyboard navigation works** — Tab order, Enter/Space activation, Esc to close overlays.
- [ ] **Alt text on all meaningful images**; decorative images get `alt=""`.
- [ ] **`prefers-reduced-motion` and `prefers-color-scheme` respected**.

## 9. Code Quality

- [ ] **Design tokens centralized** — CSS custom properties at `:root` or Tailwind config, not hard-coded throughout.
- [ ] **CSS is organized** — tokens → base/reset → components → utilities. Or Tailwind with a consistent class order.
- [ ] **No dead code, no unused classes, no leftover debug styles**.
- [ ] **Responsive uses container queries or a clear breakpoint system** — not 47 random media queries.
- [ ] **No `!important`** except in `:where()` resets or third-party overrides.
- [ ] **Performance budget considered** — JS bundle, font weight count, image weight, animation count.

## 10. Premium tells (the "10x" indicators)

These separate premium from acceptable:

- [ ] **Custom cursor or hover affordance** on key interactive elements (links, cards).
- [ ] **Marquee or logo wall with a soft fade** at the edges, not a hard cutoff.
- [ ] **A small piece of considered motion** in the hero (one element: a 3D object that follows the cursor, a marquee, a text reveal).
- [ ] **A signature visual element** — a gradient mesh, a custom illustration style, a distinctive button shape, a unique icon treatment — used consistently.
- [ ] **Footer is well-designed, not an afterthought** — column hierarchy, social row, legal row, newsletter input styled to match.
- [ ] **404 / empty / loading pages are designed**, not the framework default.
- [ ] **Microcopy is human** — "Oops, that didn't work" not "An error occurred". "Get a demo" not "Contact sales".
- [ ] **The product screenshot / 3D render in the hero has a real background** — not a flat color, not a white void. A subtle gradient, a soft shadow, a stage.

---

## How to use this checklist

1. After extracting a pattern from a gallery and before writing code, **read this file**.
2. For each section, decide what the design will do. Write it down if it helps.
3. After implementing, **re-read this file as an audit**. Mark Weak items and fix them.
4. The "Premium tells" section is what users *feel* but can't name. Skim it last and ask: does this UI have at least 3 of these?
