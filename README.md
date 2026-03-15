# Ryan's Vinyl Collection

A personal vinyl record collection catalog, viewable at [vinyl.ryanrscott.com](https://vinyl.ryanrscott.com).

## Features

- **Card & list views** — browse by album art grid or compact rows
- **Sort** by artist, title, genre, or year
- **Group** by artist, genre, or year
- **Search** — real-time filtering across artist, title, genre, and year
- **Dark/light mode** toggle

## Stack

Single-file HTML/CSS/JS app with no build step or dependencies. Album art is stored locally in `/img/` and served as static files via GitHub Pages.

## Adding Albums

1. Add an entry to the `ALBUMS` array in `index.html`
2. Add the album art as `/img/{id}.jpg`
3. Add the ID to the `HAS_ART` set in `index.html`
4. Update the record count in the header and footer

Album art can be bulk-downloaded using `download_art.py`, which pulls from MusicBrainz + Cover Art Archive.
