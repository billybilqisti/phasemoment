# Phasemoment® Website

Studio portfolio: a full-screen project showcase (home) plus per-project case-study pages.
Built with [Vite](https://vitejs.dev) and vanilla HTML/CSS/JS (ES modules), no framework.

## Getting started

```bash
npm install
npm run dev       # http://localhost:3000
npm run build     # production build → dist/
npm run preview   # serve the production build
```

> No Node yet? The source also runs unbundled from any static server at the project root,
> e.g. `python3 -m http.server 3000`. Paths are root-absolute (`/src/...`), so serve from the root.

## Structure

```
.
├── index.html                  # Home: showcase (Figma 123:120 "Home - Scrolled")
├── work/
│   └── kura.html               # Case study: KURA (Figma 97:182)
├── src/
│   ├── assets/
│   │   ├── icons/              # favicon / emblem
│   │   └── images/
│   │       ├── home/           # showcase slide backgrounds (bg_<project>.png)
│   │       └── work/<project>/ # case-study imagery
│   ├── scripts/
│   │   ├── data/projects.js    # project registry: order, names, case-study links
│   │   ├── modules/            # reusable behaviour (clock, showcase, dock-modal, emblem)
│   │   └── pages/              # one entry per page (home.js, work.js)
│   └── styles/
│       ├── base/               # tokens, reset, shared responsive rules
│       ├── components/         # header, project-nav, footer-bar, dock, modal
│       ├── pages/              # page-specific layout (home-*, work-detail)
│       ├── home.css            # entry stylesheet for index.html
│       └── work.css            # entry stylesheet for work/*.html
├── design-reference/           # Figma exports & raw node JSON (not part of the build)
├── vite.config.js
└── package.json
```

## Adding a new case study

1. Add images to `src/assets/images/work/<project>/`.
2. Copy `work/kura.html` to `work/<project>.html` and replace the content/image paths.
3. Set `href: '/work/<project>.html'` for the project in `src/scripts/data/projects.js`.
4. Add `data-href="/work/<project>.html"` to that project's `.slide` in `index.html`.
5. Register the page in `vite.config.js` → `build.rollupOptions.input`.
