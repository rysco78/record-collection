# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Running the site

```bash
python3 server.py        # serves on http://localhost:3010
```

To re-download or refresh album art:
```bash
python3 download_art.py  # fetches from MusicBrainz + Cover Art Archive
```

## Architecture

This is a single-page, zero-dependency vinyl collection website. Everything lives in one HTML file with embedded CSS and JS.

**`index.html`** — the entire app: markup, styles, and logic in one file.
**`server.py`** — a minimal Python static file server (no proxy, no API calls at runtime).
**`img/`** — local album art as `{id}.jpg` (e.g. `img/58.jpg` for album id 58).
**`download_art.py`** — one-time utility to bulk-download cover art via MusicBrainz/CAA.

## Key conventions

### Album data
Albums are defined in the `ALBUMS` array inside `index.html`. Each entry:
```js
{"id": 58, "artist": "The Beatles", "title": "Abbey Road", "genre": "Classic Rock", "year": 1969, "img_url": ""}
```
`img_url` is vestigial (always `""`); images are served from `/img/{id}.jpg`.

### Cover art
The `HAS_ART` Set in `index.html` controls which albums show real cover art vs. the vinyl placeholder SVG. **Always update this set when adding/removing albums or images.** IDs not in the set render a styled vinyl record placeholder.

### Adding an album
1. Add entry to `ALBUMS` array with the next sequential ID.
2. Download art via MusicBrainz (see `download_art.py` for the pattern).
3. Add the ID to `HAS_ART`.
4. Update the record count in two places: `#total-label` and `#footer-count`.

### Removing an album
1. Delete the entry from `ALBUMS`.
2. Remove the ID from `HAS_ART`.
3. Delete `img/{id}.jpg`.
4. Update the record counts.

## Art sourcing

Primary source: **MusicBrainz + Cover Art Archive** (open, no auth, CORS-friendly from server side).
- Search: `https://musicbrainz.org/ws/2/release/?query=...&fmt=json`
- Image: `https://coverartarchive.org/release/{mbid}/front-500`
- Rate limit: 1 req/sec unauthenticated — `download_art.py` respects this.

Fallback: `sips` (macOS) to convert user-supplied images: `sips -s format jpeg input.png --out img/{id}.jpg -Z 600`

iTunes API cannot be used directly from the browser (CORS blocked). Python-side fetches work with SSL cert verification disabled (`ssl.CERT_NONE`) due to macOS Python cert bundle issues.
