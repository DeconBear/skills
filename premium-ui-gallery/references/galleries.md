# Curated Design Gallery Reference

This file is the routing + extraction reference for the 10 design-inspiration galleries bundled with the `premium-ui-gallery` skill. The **Routing Table** at the top maps UI sections to the best gallery to consult. The **Gallery Profiles** below give URL structure, browsing patterns, and concrete takeaways for each.

## Routing Table

Match the UI section the user is working on to the best gallery. Default to the first entry; add a second if the style direction calls for it.

| UI Section / Need                    | Primary Gallery                            | Secondary (for style or depth)                  |
| ------------------------------------ | ------------------------------------------ | ----------------------------------------------- |
| Full landing page / marketing site   | `landing.love`                             | `godly` (recent.design), `saaspo` (SaaS only)   |
| Whole-site inspiration (any vertical)| `curated.design` (Craftwork)               | `landing.love`, `godly`                          |
| Section-level pattern (hero, pricing)| `curated.design` → `/curated/sections`     | `component.gallery`                              |
| SaaS landing page specifically       | `saaspo`                                   | `landing.love` (filter `/collection/gsap` etc.) |
| Navbar / top navigation              | `navbar.gallery`                           | `component.gallery`                              |
| CTA button / conversion section      | `cta.gallery`                              | `landing.love` (hero CTAs)                       |
| Mobile app screen / pattern          | `mobbin`                                   | `component.gallery` (mobile components)         |
| Onboarding / sign-up / paywall flow  | `mobbin`                                   | —                                                |
| Brand identity, logo, color system   | `rebrand.gallery`                          | `hugeicons` (logo assets)                        |
| Icon set / icon family               | `hugeicons`                                | `mobbin` (for in-context usage)                  |
| Generic UI component (card, form…)   | `component.gallery`                        | `mobbin`                                         |
| Premium "god-tier" visual showcase   | `godly` (recent.design)                    | `landing.love`                                   |

**Style-direction overrides:**

- 3D / WebGL / Three.js → `landing.love` collections (`/collection/webgl`, `/collection/threejs`), then `godly`.
- Dark mode → `landing.love` style filter `/style/dark-mode` (610+ entries).
- Gradient → `landing.love` `/style/gradient`.
- Horizontal scroll → `landing.love` Horizontal Scroll category.
- Mobile-first product UX → `mobbin`.

---

## Gallery Profiles

### 1. curated.design (now Craftwork Curated)

- **URL**: https://curated.design → redirects to https://craftwork.design/curated/websites/
- **What it curates**: Hand-picked full websites and reusable UI sections, plus a marketplace of Figma/Framer/Webflow templates, UI kits, illustrations, 3D, fonts, and icons.
- **Browse structure**:
  - Websites: `/curated/websites` filtered by category (Agency, Portfolio, Web3, Tech, AI, Marketing, Design Tools, Development Tools, E-commerce, Finance, Productivity, Desktop Apps, Web Apps, Mobile Apps)
  - Sections: `/curated/sections` (granular UI patterns: hero, pricing, footer, navbar, etc.)
  - Catalog (assets): `/catalog/figma`, `/catalog/framer`, `/catalog/webflow`, `/catalog/ui-kits`, etc.
- **Best for**: Whole-site direction, section-level patterns, vertical-specific inspiration (fintech, Web3, agency, AI), and finding ready-made Figma/Framer kits to bootstrap.
- **Takeaways to extract**: Industry-specific hero composition, how a vertical handles trust signals, pricing-table structure, footer information architecture.

### 2. landing.love

- **URL**: https://landing.love
- **What it curates**: 2,000+ landing pages and marketing sites, each captured as a **full-page video recording** (not just a screenshot — see how it scrolls, animates, transitions).
- **Browse structure**:
  - Categories (48): `/categories/{slug}` — e.g. `/categories/saas`, `/categories/3d-website`, `/categories/portfolio`, `/categories/agency`, `/categories/ecommerce`, `/categories/horizontal-scroll`
  - Styles: `/style/dark-mode`, `/style/gradient`, `/style/retro`, `/style/light-mode`
  - Collections (by tech): `/collection/gsap` (179), `/collection/webgl` (123), `/collection/threejs` (65)
  - Platforms (no-code output): `/platform/webflow` (99), `/platform/framer` (24)
  - Individual: `/sites/{slug}`
  - Pagination: `/page/{n}` up to ~139
- **Best for**: Landing-page composition, scroll-driven animation, 3D / WebGL hero scenes, dark-mode typography, and seeing motion in context (videos reveal what screenshots can't).
- **Takeaways to extract**: Hero scroll choreography, sticky/scroll-pinned section behavior, gradient + grain texture combos, how dark UIs handle type contrast, GSAP scrolltrigger patterns.

### 3. saaspo

- **URL**: https://saaspo.com
- **What it curates**: Curated screenshots of real SaaS marketing sites — pricing pages, feature pages, home pages — tagged by category (analytics, CRM, marketing, dev tools, AI, finance, HR, etc.).
- **Browse structure**: Homepage grid of screenshots with category tags; click an entry to see the source site. Filter by tag/vertical. No rigid `/category/{slug}` pattern — primarily tag-driven.
- **Best for**: SaaS-specific conventions: how pricing is presented, how feature grids are composed, trust signals (SOC2, GDPR, customer logos), comparison-table patterns, "how [competitor] does it".
- **Takeaways to extract**: SaaS hero structure (headline + sub + product screenshot + dual CTA), feature-block rhythm (alternating image/text rows), pricing-tier composition (3-tier, "most popular" highlight, annual/monthly toggle), footer link taxonomy.

### 4. navbar.gallery

- **URL**: https://navbar.gallery
- **What it curates**: Real navbar screenshots from production sites (Cloudflare, Asana, Velt, Browserbase, etc.), each tagged by pattern type.
- **Browse structure**:
  - All: `/browse`
  - By type: `/type/{type}` — `dropdowns`, `mega-menu`, `side-bar`, `search-bar`, `announcement-bar`, `full-screen`, `breadcrumbs`, `static`, `sticky`
  - Detail: `/navbar/{site-name}` (e.g. `/navbar/cloudflare`)
  - Blog: `/blog`
- **Best for**: Choosing and implementing a navigation pattern. Pick the right *type* first, then study 3–5 real examples.
- **Takeaways to extract**:
  - **Sticky/static**: backdrop-blur on scroll, border vs. shadow when "stuck", logo swap on scroll.
  - **Dropdown**: hover vs. click trigger, animation (fade/slide), how mega-menu columns are laid out, focus management for a11y.
  - **Mega menu**: 2–4 column grid, imagery placement, featured promo area, dividers.
  - **Full-screen**: overlay animation, escape-to-close, large type, primary nav + secondary nav.
  - **Announcement bar**: dismissibility, color/contrast, link styling, persistence across pages.

### 5. cta.gallery

- **URL**: https://cta.gallery
- **What it curates**: Individual Call-to-Action components from real sites — buttons, forms, modals, pricing prompts, newsletter signups, download prompts.
- **Browse structure**:
  - Individual: `/cta/{slug}` (e.g. `/cta/durable`, `/cta/langchain`)
  - Categories: `/categories/button`, `/categories/call-to-buy`, `/categories/download`, `/categories/form`, `/categories/modal-pop-up`, `/categories/navigation`, `/categories/newsletter`, `/categories/pricing`
  - Filters on home: industry, mode (dark/light, etc.)
  - Supporting: `/templates`, `/cta-tips`
- **Best for**: Writing high-conversion CTA copy, choosing button visual treatment, and structuring form CTAs (input + submit) vs. single-button CTAs.
- **Takeaways to extract**:
  - **Button**: shape (pill vs. rounded-md vs. square), color (one accent vs. neutral), size relative to body, hover state (lift, glow, color shift), label verbosity (2–4 words).
  - **Form CTA**: input + button alignment, placeholder copy, submit label, helper text, error state.
  - **Modal/popup**: trigger, size, dismiss affordance, primary action hierarchy.
  - **Pricing prompt**: framing ("Start free", "Get a demo", "Talk to sales"), what's included in the click, secondary action.
  - Copy patterns: action verb + object ("Start building", "Get a demo"), outcome framing ("Ship faster"), low-friction ("Try free for 14 days").

### 6. mobbin

- **URL**: https://mobbin.com
- **What it curates**: The largest library of **real mobile (iOS/Android) and web app** design patterns — thousands of apps, captured screen-by-screen, organized by pattern and flow.
- **Browse structure**:
  - By app: `/apps/{app-name}`
  - By pattern/screen type: `/patterns/{pattern}` — e.g. onboarding, sign-up, sign-in, paywall, checkout, empty states, error states, settings, profile, search, notifications, navigation
  - By flow: `/flows/{flow-name}`
  - By UI element: `/ui/{element}` — buttons, lists, cards, tabs, toolbars, sheets, modals
  - Web app patterns: `/web/{app-name}` for desktop product UX references
- **Best for**: Mobile-first product design, app onboarding, paywall/subscription prompts, native navigation patterns, empty/error/loading states, mobile component anatomy.
- **Takeaways to extract**:
  - **Onboarding**: number of screens, progress indicator, permission ask order, value-prop framing, skip pattern.
  - **Sign-up / sign-in**: social-login button order, form field count, password rules surface area, "continue with…" hierarchy.
  - **Paywall**: feature comparison vs. price-only, trial framing, restore-purchase placement, "skip for now" affordance.
  - **Empty states**: illustration + headline + primary action, what "first run" looks like.
  - **Settings**: grouped list pattern, destructive actions, account section placement.

### 7. rebrand.gallery

- **URL**: https://rebrand.gallery
- **What it curates**: Real corporate rebrands and visual-identity launches — Walmart, Netflix, Semrush, Etsy, Schweppes, Olympique de Marseille, etc. — with logo, color, typography, and reveal assets.
- **Browse structure**:
  - Sections: `Intros` (write-ups) and `Bentos` (visual grids)
  - Detail: `/rebrand/{brand-slug}` (e.g. `/rebrand/netflix-playground`, `/rebrand/semrush-2026`)
- **Best for**: Establishing a brand color system, type pairing, logo treatment, and identity scalability for a new product/feature.
- **Takeaways to extract**:
  - **Color system**: primary + secondary + neutrals + 1 accent, light/dark variants, semantic mappings (success/warning/error).
  - **Typography pairing**: a humanist sans for UI + a display face for headlines, or a single family used at multiple weights.
  - **Logo**: how it simplifies at small sizes (favicon, app icon), monogram vs. wordmark, color modes (full color / mono / reversed).
  - **Identity scalability**: how the system holds up across web, mobile, social, and print contexts.

### 8. hugeicons

- **URL**: https://hugeicons.com
- **What it curates**: 54,000+ icons across consistent style families — a real icon *system*, not a grab bag.
- **Browse structure**:
  - By style: `/icons/{style}-{corner}` — styles: `stroke`, `twotone`, `duotone`, `solid`, `bulk`. Corners: `rounded`, `standard`, `sharp`. Examples: `/icons/stroke-rounded`, `/icons/solid-rounded`, `/icons/bulk-sharp`.
  - By category: e.g. business, communication, finance, weather
  - Logos: `/logos` (free brand logos)
  - Generator: `/icon-font-generator`
- **Integrations**: NPM packages, SVG, icon-font CDN, framework-specific packages for **React, React Native, Vue, Angular, Svelte, Flutter, WordPress, VS Code**, Figma plugin, Framer plugin, Sketch, Illustrator. Also exposes an MCP server.
- **Best for**: Choosing **one** icon family and using it consistently across an entire UI. The corner-style choice (rounded vs. sharp) should match the product's overall geometry.
- **Takeaways to extract**:
  - **Pick one style and stick to it** — mixing stroke + solid in one UI looks generic.
  - **Match corner radius** — if buttons are 12px, pick `rounded` icons; if buttons are 4px, pick `standard` or `sharp`.
  - **Default size**: 20–24px in UI chrome, 16px in dense tables.
  - **Stroke width consistency** — if the icon family is 1.5px stroke, keep the rest of the line work (dividers, borders) compatible.

### 9. component.gallery

- **URL**: https://component.gallery
- **What it curates**: A categorized gallery of UI components (buttons, cards, navigation, footers, pricing tables, modals, forms, headers) scraped from real websites, each linking back to its source.
- **Browse structure**: Browse by component type. Each component page shows multiple real-world examples with a link to the live site.
- **Best for**: Comparing how many real products solve the same component — e.g. "show me 10 ways real sites do a pricing table" or "10 ways to do a card grid". Great for picking conventions, not for novel design.
- **Takeaways to extract**:
  - Common component anatomy (what's always present).
  - Variants worth supporting (default / hover / focused / disabled / loading).
  - Responsive collapse behavior.
  - Accessibility primitives (focus rings, ARIA, keyboard handling).

### 10. godly.website (now recent.design)

- **URL**: https://godly.website → redirects to https://recent.design (and serves http://recent.design/?ref=godly)
- **What it curates**: A curated feed of "god-tier" websites — premium visual design, strong typography, considered motion, often by studios or design-led tech companies. The original godly.website brand; recent.design is the successor.
- **Browse structure**: Browse by category/tag (SaaS, agency, portfolio, AI, Web3, etc.) and by recency. Cards link out to the live site.
- **Best for**: Pushing the visual ceiling — when the rest of the galleries feel too "normal", this is where to find the most art-directed, animation-heavy, type-driven examples. Use it to set the bar for the hero, the type system, and the motion language.
- **Takeaways to extract**:
  - **Hero type scale**: how big can the headline go before it breaks? (Often 72–160px on desktop.)
  - **Type pairing**: editorial serif × geometric sans, or a single variable font at multiple weights.
  - **Motion language**: a consistent easing curve and duration scale used everywhere.
  - **Negative space**: how much whitespace is "enough" — premium UIs use a lot.
  - **Asset treatment**: grain, gradient mesh, 3D renders, custom illustrations.

---

## How to use this file in practice

1. **Skim the routing table** when the user describes a section — pick the primary gallery.
2. **Open the gallery's profile** above and follow the URL pattern to browse live examples.
3. **Pull 2–3 specific entries** (the URL slugs in each profile are good starting points) and study their layout, type, color, and motion.
4. **Extract the pattern** (not the pixels) and apply it with the project's brand tokens.
5. If the live site is unreachable (some galleries block scraping), use the profile's "Takeaways to extract" as a working summary — they encode the same lessons.

When fetching live examples, prefer targeted URLs (e.g. `/type/mega-menu` on navbar.gallery, `/collection/gsap` on landing.love) over the homepage so the result set is focused.
