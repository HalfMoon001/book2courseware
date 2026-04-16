# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

`book2courseware` is a **Claude Code skill**, not a runnable app. It converts a lesson plan (教案 / 课本章节) into a single-file interactive HTML courseware by string-substituting placeholders in fixed, pre-tested templates.

Install = copy into the user's skills directory:

```bash
cp -R book2courseware ~/.claude/skills/
```

There is no build system, no package manager, no test runner. The repo is templates + docs. "Running" the skill happens inside Claude Code when the user asks to 生成课件 — the skill's workflow is triggered automatically via `SKILL.md`'s frontmatter description.

To **try** the skill end-to-end, open any file under `examples/*/` in a browser (e.g. `examples/04-化学-氯及其化合物/chlorine_courseware.html`). `examples/04-化学-氯及其化合物/_build_chlorine.py` is a reference Python assembler showing how `shell/` + `components/` get concatenated — useful as a concrete template for writing new assemblers.

## Entry point and reading order

**Always read `SKILL.md` first.** It is the authoritative spec for the skill: workflow, hard rules, bug-fix history baked into `shell/`, and the checklist. The frontmatter there is what Claude Code reads to auto-trigger the skill.

Supporting docs (read when needed):
- `MANIFEST.md` — component decision table (content type → which component to use) and per-page capacity limits
- `web-search-workflow.md` — when & how to fill `components/web-source-card.html`
- `components/media-workflow.md` — how to fetch images/videos for `components/media-embed.html`, including the base64-inline rule and 百度百科 CDN vs. Wikimedia Commons routing
- `README.md` — user-facing install + demo index

## Architecture: how a courseware file is built

A finished courseware is **one HTML file**, assembled in this fixed order:

```
shell/head.html                # <!DOCTYPE>, CSS design tokens, fonts, shared SVG markers, <body>
  [slides from components/]    # cover → section-divider → content pages → quizzes → mini-game → summary
shell/nav.html                 # bottom nav dots + page counter
shell/scripts.js               # paging, fill-blank reveal, MCQ feedback, gamePick()
shell/editor.html              # ~55KB in-browser editor (CSS + UI DOM + JS IIFE, self-contained)
</body></html>
```

Key invariants to preserve when editing templates or writing an assembler:

1. **The four `shell/` files are load-bearing and must appear in the order above.** `shell/editor.html` must be the last thing before `</body>`. Missing it = no ✏️ 编辑模式 button = user can't edit/download the modified file.

2. **Do not use `str.replace('</body>', ...)` as an insertion anchor.** Append to the string tail manually or use `rfind('</body>')`. Historical regressions happened when the literal `</body>` appeared in comments inside `shell/nav.html` / `shell/editor.html` and `replace` hit the wrong one, silently burying patches inside an HTML comment. Final output must contain exactly one `</body>`.

3. **Do not hand-patch `shell/editor.html`, `shell/scripts.js`, or `shell/nav.html`.** Six concrete runtime bugs are fixed at the skill level (scripts.js closure over stale `slides/current/total`; edit-mode flex reflow drift; `globalAddText` percent-transform drag jump; `moveHtmlElement` robustness against `translate(..%..)`; undo/redo clamping instead of `goTo(0)`; `editorSave` actually persisting to `localStorage['book2ppt:' + pathname]`). See `SKILL.md` → "Editor bug fixes baked in". Re-editing these files means new courseware loses the fixes.

4. **Placeholders are `{{SNAKE_CASE}}`.** Assembly = literal string replace. Final output must contain zero `{{...}}`.

## Non-negotiable design constraints (from user feedback)

These are not style preferences — violating them has repeatedly caused regressions. Full list in `SKILL.md`; the ones most likely to bite:

- **Font sizes are frozen** (body 22px / title 36px / cover 64px). Keep `--font-body: 'Nunito', 'Ma Shan Zheng', ...` with Nunito first — without it, Latin/digit glyphs fall back to a Chinese font and become unreadable.
- **`.slide` uses `min-height: 100vh`, never `height: 100vh`.** Never add `overflow: hidden` to `html`, `body`, `.slide`, or `.slide-col` — long pages must scroll. `head.html` already sets this correctly; preserve it.
- **Arrows use shared SVG markers** (`arr-red/blue/green/gold/purple/dark/orange`), never `<polygon>` triangles. Triangle coordinates on rotated lines drift visually. Tangent arrows on an ellipse: a 10px horizontal line at `(cx, cy+ry)` with `marker-end`.
- **Mandatory interactive mini-game.** Every courseware needs ≥1 `components/mini-game.html` slide (≥2 for >15 pages). A courseware without a game is considered failing.
- **No click-to-flip cards.** Use fill-blank or MCQ — flip cards break print review.
- **Web assets are default, not optional.** Every courseware needs 2–3 real-world web items (images/videos/text cards). All web fetching goes through the `web-access` skill (handles防盗链 / referer / login). All `<img>` tags must be `data:` URIs — hotlinked remote URLs are banned except for `iframe` video embeds.
- **Chinese courseware images come from 百度百科 CDN** (`bkimg.cdn.bcebos.com`, hotlink-allowed), never from `image.baidu.com` search results (防盗链 → red X). International topics use Wikimedia Commons.
- **After downloading an image, always `Read` it visually before writing the caption** — 百科 alt/caption text is often wrong (documented incident: a 百度百科 "氯气" entry captioned a generic yellow-green flame as "钠在氯气中燃烧").
- **Print friendliness** is implemented in `head.html`'s `@media print` (fill-blank answers shown, nav hidden). Don't break it.

## Skill dependencies

`SKILL.md`'s workflow actively invokes other skills by name — don't reimplement them:

| Situation | Invoke |
|---|---|
| `.pdf` lesson plan (incl. scanned PDFs → render pages as PNG, Read visually) | `pdf` |
| `.docx` lesson plan | `docx` |
| **Any** web fetch / search / login / dynamic page | `web-access` |

In particular, literal `WebSearch(...)` / `WebFetch(...)` calls in the docs are shorthand — in a real session they all route through `web-access`.

## When adding a new component

1. Add `components/<name>.html` with `{{SNAKE_CASE}}` placeholders and a leading HTML comment documenting them (follow `components/cover-slide.html` as the pattern).
2. Add a row in `MANIFEST.md`'s decision table mapping content type → component.
3. If the component has a per-page capacity limit, add it to `MANIFEST.md`'s capacity table.
4. If new CSS is needed, add it to `shell/head.html` (not the component file) so it's shared across the bundle.
5. If new JS is needed (quiz feedback, game logic), add it to `shell/scripts.js` — do not inline `<script>` in the component, or the editor's serialization round-trip may drop it.

## When fixing a bug in `shell/`

Any fix to `shell/editor.html`, `shell/scripts.js`, or `shell/nav.html` must also be documented under `SKILL.md` → "Editor bug fixes baked in". That list is how future instances know not to accidentally revert the fix when "cleaning up" the shell files.
