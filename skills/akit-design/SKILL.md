---
name: akit-design
description: Use when designing web or mobile UI/UX, establishing or updating a DESIGN.md design system, choosing typography/color tokens, or auditing interfaces against generic AI visual clichés and accessibility flaws.
---
# AKit Design — DESIGN.md Systems & UI/UX Pro Max Intelligence

## Overview
`akit-design` synthesizes the **Markdown Design System (`DESIGN.md`)** specification from `VoltAgent/awesome-design-md`, the **UI/UX Intelligence** taxonomy (style pairings, typography, color contrast, responsive ergonomics) from `nextlevelbuilder/ui-ux-pro-max-skill`, and the **Intentional Frontend Design** philosophy from `anthropics/skills`.

**Core principle:** Every interface must commit to an intentional aesthetic direction backed by reusable tokens in `DESIGN.md` and complete interactive states — never ship generic AI purple-gradient templates or screenshot-only happy paths.

---

## Anti-AI-Slop & Aesthetic Direction Gate
Before writing CSS, Tailwind config, or UI components, lock in a deliberate aesthetic persona (`references/ui-ux-intelligence.md`):
- **Editorial / Swiss Grid:** High-contrast serif + grotesk pairing, exposed hairlines (`1px`), generous negative space, crisp data hierarchy.
- **Industrial / Technical Precision:** Monospace numeric alignment (`tabular-nums`), dense slate/zinc surfaces, subtle semantic status badges, keyboard-first ergonomics.
- **Warm Craft / Organic Studio:** Paper/stone neutral backgrounds, warm clay/terracotta accents, tactile card elevation, calm motion.
- **Forbidden Clichés:** Unmotivated purple-to-cyan neon gradients, 3 identical centered feature cards with generic spark icons, inconsistent border radii, or low-contrast gray text on gray surfaces.

---

## Antigravity Native Tool Mapping
1. **Inspect Existing Design Tokens (`read_file`):** Check `DESIGN.md`, `tailwind.config.*`, `globals.css`, or Figma token exports before defining new variables.
2. **Generate `DESIGN.md` Specification (`write_file`):** Create or update `DESIGN.md` using `references/DESIGN.template.md` so all subsequent agents (`akit-react`, `akit-browser-qa`) share one source of truth.
3. **Visual & Accessibility Verification:** Pair with `akit-browser-qa` (or `image-generator` subagent when visual assets are requested) to validate responsive viewports (`375px`, `768px`, `1440px`) and WCAG contrast.

---

## Step-by-Step UI/UX Design Workflow

### Step 1: Domain & User Task Discovery
1. Identify primary user personas, top 3 high-frequency workflows, device targets (mobile-first vs. desktop-dense), and brand constraints.
2. Inspect existing `DESIGN.md` or CSS variables; never overwrite an established design system without explicit user approval.

### Step 2: Author or Update `DESIGN.md` (`references/DESIGN.template.md`)
Define explicit, token-driven rules for:
1. **Color Palette & Semantic Surfaces:**
   - Background layers (`bg-canvas`, `bg-surface`, `bg-elevated`, `bg-overlay`).
   - Text hierarchy (`text-primary` >= 7:1 contrast, `text-secondary` >= 4.5:1 contrast, `text-muted`).
   - Semantic intent tokens (`accent-primary`, `status-success`, `status-warning`, `status-danger`).
2. **Typography Scale & Pairing:**
   - Display/Heading font + Body font + Monospace font (`font-variant-numeric: tabular-nums` for all tables, prices, and metrics).
   - Modular scale (`xs: 12px` through `4xl: 36px`) with explicit line-heights and `max-w-prose` (`60ch–70ch`) reading widths.
3. **Spacing, Radius & Elevation Grid:**
   - Strict `4px` / `8px` spatial rhythm; consistent border radius tokens (`sm`, `md`, `lg`); restrained shadows/borders.

### Step 3: Map Complete UX State Matrix (`references/ui-ux-intelligence.md`)
Every screen and interactive component MUST specify 6 states before implementation:
1. **Loading / Skeleton:** Layout-stable placeholders (`CLS = 0`).
2. **Empty / Zero-Data:** Helpful explanation + primary call-to-action to create the first item.
3. **Populated (Ideal & Extreme):** Single-line vs. 3-line wrapped titles, `0` vs. `999,999,999` numbers, missing avatars.
4. **Validation & Field Error:** Inline field-level guidance (`aria-invalid`, `aria-describedby`), preserving user input.
5. **Network / Partial Failure:** Retryable banner or fallback without crashing the whole page.
6. **Keyboard Focus & Disabled:** Visible `:focus-visible` ring (`2px` offset) and accessible touch targets (`>= 44x44px` on mobile).

---

## Red Flags & Rationalization Counter-Table

| Common Excuse / Rationalization | Engineering Reality & Mandatory Action |
| :--- | :--- |
| *"I'll hardcode hex colors (`#6366f1`) directly inside 15 component files."* | Hardcoded hex values cause visual drift and break dark/light theming. Define semantic tokens in `DESIGN.md` and CSS variables first. |
| *"The happy-path screenshot looks great, so the UI is done."* | A page without empty states, loading skeletons, error handling, and mobile responsiveness fails in real usage. Complete the 6-state matrix. |
| *"Light gray text (`#9ca3af` on `#f3f4f6`) looks sleek and minimal."* | Fails WCAG AA contrast (< 4.5:1) and is unreadable on non-Retina screens. Verify contrast ratios (`references/ui-ux-intelligence.md`). |
| *"I'll use `Inter` + purple gradients for every single project."* | Generic AI template fatigue. Choose an intentional industry-aligned palette and typography pairing from `references/ui-ux-intelligence.md`. |

---

## Safety & Exit Gates
- Never copy proprietary brand logos, licensed commercial fonts, or copyrighted illustrations without authorization.
- Require `DESIGN.md` token alignment and WCAG AA contrast checks before handing off to `akit-react` or `akit-browser-qa`.

## Reference Materials & Attribution
- Complete `DESIGN.md` specification template: `references/DESIGN.template.md`
- UI/UX Pro Max intelligence matrix (palettes, typography, UX state checklist): `references/ui-ux-intelligence.md`
- Inspired by `VoltAgent/awesome-design-md`, `nextlevelbuilder/ui-ux-pro-max-skill`, and `anthropics/skills` (`frontend-design`). Original AKit instructions.
