# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project overview

This is a static personal portfolio site hosted on GitHub Pages. It is a single-page site (`index.html`) with vanilla CSS (`styles.css`) and a small amount of vanilla JavaScript (`script.js`). There is no build system, package manager, or framework.

## Common commands

### Local preview

Because this is a static site, any static-file server works. For example:

```bash
# Python 3
python -m http.server 8000

# Node.js (if installed)
npx serve .

# VS Code
# Use the "Live Server" extension and open index.html
```

Then open `http://localhost:8000` in a browser.

### Compile the CV

`cv.tex` is a Chinese résumé that requires XeLaTeX and the `ctex` package:

```bash
xelatex cv.tex
```

On Windows with MiKTeX/TeX Live installed, this should resolve the `ctex` dependency automatically. The file uses `fontset=windows`, so compilation on non-Windows systems may need adjustment or a different fontset.

### Validate markup

There is no project-level test or lint script. To sanity-check changes:

- Open the page locally and review each section at desktop, tablet, and mobile widths.
- Use a browser devtools accessibility audit to check contrast and focus order.
- Run an HTML validator (e.g., the W3C validator) against `index.html`.

### Tests

A `test-results/.last-run.json` file exists from a prior Playwright run, but no Playwright configuration or test files are currently committed. To add tests, create a `playwright.config.js` and tests in the conventional locations, then run:

```bash
npx playwright test
```

## Architecture

### Single-page structure

- `index.html` contains all page content and is the only production HTML file.
- `styles.css` is hand-written; no preprocessor is used.
- `script.js` is hand-written and currently a placeholder for future interactions.
- `assets/hongwei-qin.jpg` is the portrait used in the sidebar and as the favicon.
- `design/` holds concept/mockup images; nothing in that folder is referenced by the live site.

### Content order

The page is a single scrolling document with no top navigation:

1. Sidebar profile (avatar, name, affiliation, contact)
2. About
3. Research & Education
4. Selected Projects
5. Technical Skills
6. Selected Coursework
7. Footer

### Styling conventions

- Design tokens live in `:root` at the top of `styles.css` (`--bg`, `--text`, `--accent`, `--border`, etc.).
- The site uses a very light, understated theme (`#ffffff` background) with a muted blue for links (`#0366d6`).
- Layout uses CSS Grid and Flexbox.
- The desktop layout is a two-column sidebar + main content grid; it collapses to a single column on smaller screens.
- Section titles are uppercase with a subtle bottom border.
- Content is presented as plain text and simple lists with minimal decoration.
- There are no cards, shadows, gradients, icons, or large decorative numbers.
- The layout is responsive at breakpoints `800px` and `480px`.
- Reduced-motion preferences are honored via `@media (prefers-reduced-motion: reduce)`.

### Navigation behavior

- There is **no top navigation bar**. The page is meant to be read by scrolling.
- Smooth scroll is enabled in CSS via `scroll-behavior: smooth`.
- Contact links live in the sidebar and footer.

### CV

- `cv.tex` is maintained separately from the web page and is written in Chinese.
- It uses the `ctex` package with `fontset=windows` and is compiled with XeLaTeX.
- Keep content dates and project metrics in sync with `index.html` when either file changes.

## Deployment

The site is published with GitHub Pages from the default branch (`main`). Pushing changes to `index.html`, `styles.css`, `script.js`, or `assets/` updates the live site once the Pages build completes.
