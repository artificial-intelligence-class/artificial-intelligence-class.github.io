# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Jekyll static website for CIS 4210/5210 Artificial Intelligence at the University of Pennsylvania. It hosts course materials including syllabus, lecture slides, homework assignments, and robot programming assignments.

## Build Commands

```bash
# Install Ruby dependencies
bundle install

# Run local development server (auto-reloads on changes)
bundle exec jekyll serve

# Build static site to _site/ directory
bundle exec jekyll build
```

The local server runs at `http://localhost:4000`.

## Architecture

**Static Site Generator:** Jekyll 4.3 with Minima theme

**Key Directories:**
- `_data/` - YAML files driving dynamic content (modules.yaml, staff.yaml, lectures, recitations)
- `_layouts/` - HTML templates (Bootstrap 3.3.5, MathJax for math rendering)
- `homeworks/` - Assignment materials with Markdown files, Python starters, and Jupyter notebooks
- `r2d2_assignments/` - Sphero robot programming assignments by semester
- `slides/` - PowerPoint lecture slides
- `assets/` - CSS, images, PDF readings

**Content Pattern:**
- Pages use Markdown with YAML front matter (title, layout, due_date, release_date)
- Course structure defined in `_data/modules.yaml`
- Liquid templating for dynamic content (date-based alerts, staff listings)
- Homework directories contain `.md` description + Python/Jupyter starter files

**Deployment:** GitHub Pages auto-builds on push to master.
