# Wei Yang Academic Homepage

Minimal academic personal website for Wei Yang, a mathematics Ph.D. student at
Peking University.

The site is built with Astro, MDX, and KaTeX. It is intended to be easy to edit
and suitable for mathematical notes written in Markdown or MDX.

## Requirements

- Node.js
- npm

## Run Locally

Install dependencies:

```bash
npm install
```

Start the development server:

```bash
npm run dev
```

Build the static site:

```bash
npm run build
```

Preview the production build:

```bash
npm run preview
```

## Editing Content

- Personal information is in `src/data/profile.ts`.
- Main pages are in `src/pages/`.
- Notes can be added as Markdown or MDX files under `src/pages/notes/`.
- Global styling is in `src/styles/global.css`.

## Mathematical Notes

MDX notes support LaTeX-style math through `remark-math`, `rehype-katex`, and
KaTeX. For example:

```mdx
Inline math: $E_2^{p,q}$

Displayed math:

$$
E_2^{p,q} \Rightarrow H^{p+q}(X)
$$
```

Each note can include a posted date in its frontmatter:

```mdx
---
layout: ../../layouts/NoteLayout.astro
title: Example Note
description: A short description of the note.
author: Wei Yang
date: 2026-06-17
---

The note begins here.
```

The `date` field is shown as the date the note was added on the note page and
in the Notes index. Add `updated: YYYY-MM-DD` if a note needs a separate
revision date.

## Deployment

The output of `npm run build` is written to `dist/`. That directory can be
deployed to a static hosting provider such as GitHub Pages.

This repository includes a GitHub Actions workflow at
`.github/workflows/deploy.yml` for GitHub Pages deployment. It uses the official
Astro GitHub Action to build and upload the site, then deploys it with GitHub
Pages.

For the `yangwei02miku-del.github.io` repository:

1. Push the project to the `main` branch.
2. In GitHub, open the repository settings.
3. Go to **Pages**.
4. Set **Source** to **GitHub Actions**.

After that, every push to `main` will build and deploy the site automatically at
`https://yangwei02miku-del.github.io`.
