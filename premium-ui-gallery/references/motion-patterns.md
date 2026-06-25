# Motion Patterns Catalog

> **Inspiration**: This catalog is *inspired by* the technique-driven approach of [vibe-motion](https://github.com/vibe-motion) (an open-source org focused on programmatic motion graphics). **No code was copied** — every template in `assets/motion/` is original work. The borrowings are *which patterns matter* (text mask reveal, scroll-reveal cascade, 3D hero scene, etc.) and *the discipline of treating motion as a building block*, not code.

Animation is the soul of premium UI. A static design with a few well-chosen motions outranks a "polished" design with none. Use this catalog as a vocabulary: pick a pattern, adapt it to the brand, combine two or three — never decorate with motion for its own sake.

---

## The framework: Disney's 12 principles, applied to UI

These are public-domain animation principles (Disney, 1930s) that translate directly to UI motion. Reference them when an animation feels "off" but you can't say why.

1. **Squash and stretch** — give weight. A button press squashes slightly; a modal opens with overshoot.
2. **Anticipation** — wind up before the action. A tooltip lifts a few px before fading in.
3. **Staging** — direct the eye. The animated element should be the most prominent thing on screen at that moment.
4. **Straight ahead / pose to pose** — for UI: plan keyframes (start, end), then fill the easing, not the other way around.
5. **Follow through** — things don't stop dead. A drawer slides in, then the handle settles 4px further.
6. **Slow in / slow out** — use `ease-out` for entrances, `ease-in` for exits, never `linear` for UI.
7. **Arcs** — natural motion curves, not straight lines. Mouse-follow uses a damped arc, not a snap.
8. **Secondary action** — small reinforcements. A notification slides in *and* its icon pulses once.
9. **Timing** — speed conveys meaning. Fast (150ms) = responsive; slow (600ms) = dramatic.
10. **Exaggeration** — premium UIs go 1.3× further than feels comfortable, then dial back 5%.
11. **Appeal** — every motion should feel intentional and pleasant, not robotic.
12. **Drawing** — for UI: every animation should be a *design choice*, not a default.

---

## 2D Patterns (6)

Each pattern is implemented in `assets/motion/2d-*.html`. Open the file to see a working demo, then copy the relevant CSS/JS into your project.

### 1. Scroll-reveal cascade — `assets/motion/2d-scroll-reveal.html`

- **When to use**: Hero headlines, feature lists, card grids, anything that should feel "alive" as the user scrolls.
- **Technique**: `IntersectionObserver` watches elements with `data-reveal`. On intersect, set `--in: 1` and apply a CSS transition that animates `opacity`, `translateY`, and `scale`. Stagger via `--delay` custom property (0, 60, 120ms…).
- **Why it works**: Subtle (12px translate, 0.96→1 scale) — feels inevitable, not decorative.
- **Don't**: Reveal everything. Pick the 3–5 elements per viewport that matter; leave the rest static.

### 2. Text spotlight reveal — `assets/motion/2d-text-spotlight.html`

- **When to use**: Hero headlines, section titles, dramatic reveals on marketing pages.
- **Technique**: The text is dim by default. A `linear-gradient` mask sweeps across it (CSS keyframes animating `background-position` on a clipped `::before`). The lit portion reveals the full-opacity text.
- **Why it works**: Mimics stage lighting — one of the oldest visual metaphors for "this matters."
- **Don't**: Use on body copy. Reserve for the one headline per page that earns the drama.

### 3. SVG path draw + morph — `assets/motion/2d-svg-draw.html`

- **When to use**: Logo reveals, illustration assembly, icon-on-intro, brand marks loading.
- **Technique**: For draw-on, set `stroke-dasharray: <length>; stroke-dashoffset: <length>` and animate `stroke-dashoffset` to 0. For morph, use SMIL `<animate attributeName="d">` between two paths with the same point count, or use `flubber` / `gsap` MorphSVG.
- **Why it works**: "Made by hand" feel — implies care, which implies premium.
- **Don't**: Draw every icon on every page. Use once, for a logo or hero mark. Then it's done.

### 4. Kinetic marquee — (described, no template)

- **When to use**: Logo strips, customer walls, scrolling testimonials, ticker feeds.
- **Technique**: A `display: flex` track duplicated twice, animated with `@keyframes` translating `-50%`. Pause on hover. Mask the edges with a gradient fade.
- **Why it works**: Implies social proof + momentum. Used by Stripe, Linear, Vercel.

### 5. Spring counter / progress — (described, no template)

- **When to use**: Onboarding progress bars, stat counters, score displays.
- **Technique**: For counter, ease a number from 0 to N with an overshoot easing curve (cubic-bezier with a >1 peak in the y-axis). For progress, animate `width` with a `cubic-bezier(0.22, 1, 0.36, 1)` ease-out, with tick marks.
- **Why it works**: Numbers that *land* feel more truthful than numbers that arrive linearly.

### 6. Image clip-path reveal — (described, no template)

- **When to use**: Image grids, hero media, before/after comparisons.
- **Technique**: Wrap the image in a container with `clip-path: inset(0 100% 0 0)` and animate to `inset(0 0 0 0)`. Or use a `polygon()` wipe (diagonal, iris).
- **Why it works**: Reveals the image as if the world is uncovering it. The opposite of "image faded in."

---

## 3D Patterns (4)

All 3D templates use **Three.js** loaded from CDN via importmap. No build step. ~150–250 lines each, designed to be read, adapted, and dropped into a project.

### 1. Mouse-follow 3D hero — `assets/motion/3d-mouse-follow.html`

- **When to use**: Hero sections where a 3D object is the centerpiece. Replaces a flat product screenshot.
- **Technique**: A single mesh (icosahedron or torus knot) with a custom GLSL fragment shader for the surface. Mouse position is normalized to `[-1, 1]`, lerped into a target rotation, and applied each frame (`damp` with ~0.08 factor).
- **Why it works**: Cursor parallax implies the object is *real* and *in the room*. Premium without being loud.
- **Performance**: One mesh, one shader pass, ~60fps on integrated GPUs. Falls back to a static 2D image via `prefers-reduced-motion`.

### 2. Particle field / starfield — `assets/motion/3d-particle-field.html`

- **When to use**: Hero backgrounds, "ambient" feel, data dashboards, transition states.
- **Technique**: `THREE.Points` with a custom `ShaderMaterial`. Particle position + size encoded in attributes, twinkle encoded in the fragment shader using `sin(time + offset)`. Mouse adds a small parallax shift.
- **Why it works**: Implies depth and space without literal 3D content. Works as a backdrop for any text.
- **Performance**: 2,000–5,000 particles is the sweet spot. More than 10,000 starts to show frame drops on low-end devices.

### 3. 3D photo / card wall — `assets/motion/3d-photo-wall.html`

- **When to use**: Customer logos, feature showcases, "what we built" galleries, infinite scroll alternatives.
- **Technique**: A grid of `PlaneGeometry` meshes (e.g., 5×4), each with a colored procedural texture (no external images). Slight Z-offset per cell. Scroll position drives a subtle rotation of the whole grid; mouse position adds a tilt.
- **Why it works**: Makes a flat grid feel like a 3D object. The depth sells the scale of the content.
- **Don't**: Use for content the user needs to read. The 3D effect competes with reading. Use for visual content (logos, thumbnails, color swatches).

### 4. Distortion shader plane — (described, no template)

- **When to use**: Hero image that should feel "alive" without being obviously 3D. Liquid effect.
- **Technique**: A single plane with an image texture and a custom shader that displaces vertices using noise. Animate the noise offset over time. Subtle mouse interaction.
- **Why it works**: Looks like a still image with one extra "real" property. The 1% motion is what makes it premium.
- **Watch out**: Too much distortion looks like a funhouse mirror. The displacement amplitude should be ≤5% of the image dimension.

---

## Composition: combining patterns

Premium UIs don't pick *one* motion — they pick a *choreography* of 3–5 motions that work together. The pattern is:

```
1. Page enter  → scroll-reveal cascade on hero (1.5s total, staggered)
2. Hero idle    → mouse-follow 3D hero (continuous, subtle)
3. Scroll       → 3D photo wall parallax on approach
4. Section      → text spotlight reveal on each section title
5. Detail       → SVG path draw on a single key icon
6. Idle         → kinetic marquee in the footer area
```

Rules:
- **One pattern per viewport at a time.** Don't cascade AND spotlight AND have a 3D scene competing for attention. Layer them in *time* (sequentially), not in *space* (overlapping).
- **Lead with the slowest motion** and let the faster ones support it.
- **The page should feel calmer at the end than at the start.** Initial energy → settled state.

## Performance: the budget

- **2D**: A page should have ≤3 simultaneous CSS transitions. More than that and the main thread jank starts to show on mid-range mobile.
- **3D**: One WebGL canvas per page. Each canvas should be ≤2MB GPU memory. Particle count: 5,000 is a safe upper bound.
- **Always test on a 4× CPU-throttled phone** (Chrome DevTools → Performance → CPU throttling). If it's choppy, it ships choppy for real users.
- **Defer 3D scene creation until the canvas is in or near the viewport** (`IntersectionObserver`).

## Accessibility

- **Wrap every animation in a `prefers-reduced-motion: reduce` override** that disables `transform`/`opacity` transitions and shader animation.
- **Don't rely on motion to convey meaning** — always have a static fallback (the spotlight text is also readable in dim state; the 3D object is also a static image).
- **Respect `prefers-color-scheme`** in shader uniforms so dark-mode users don't get a black canvas with black particles.
- **Keyboard focus animations** count — the focus ring transition should also respect reduced-motion.

## How to use this catalog in practice

1. The user describes a UI section. Decide *what mood* it should set (calm, energetic, dramatic, technical).
2. Pick 1–3 patterns from above that match the mood.
3. Open the corresponding `assets/motion/*.html`, copy the technique, adapt the timing/colors to the brand.
4. Apply the `prefers-reduced-motion` and performance notes from this catalog before shipping.
5. If the result still feels generic, return to step 2 and reach for a more advanced pattern (3D, custom shader).
