<div align="center">

# 🎵 Ryan's Vinyl Collection

**A personal vinyl record collection catalog**

[![Live Site](https://img.shields.io/badge/Live-vinyl.ryanrscott.com-blue)](https://vinyl.ryanrscott.com)

</div>

## Features

- **Grid & List Views** — Browse your collection as album art cards or compact rows
- **Smart Sorting** — Organize by artist, title, genre, or year
- **Dynamic Grouping** — Group albums by artist, genre, or year for easy browsing
- **Real-Time Search** — Instant filtering across artist, title, genre, and year
- **Dark/Light Mode** — Toggle theme preference with persistent storage

## Tech Stack

| Category | Technology |
|----------|------------|
| Frontend | HTML5, CSS3, Vanilla JavaScript |
| Backend | Python static server |
| Assets | SVG, Local JPEG images |
| Hosting | GitHub Pages |

## Getting Started

### Prerequisites

- Python 3.x (for local development)
- Modern web browser

### Running Locally

```bash
# Start the development server
python3 server.py

# Server runs at http://localhost:3010
```

To refresh album artwork from MusicBrainz + Cover Art Archive:

```bash
python3 download_art.py
```

## Album Management

### Adding an Album

1. Add a new entry to the `ALBUMS` array in `index.html`:
   ```js
   {"id": 59, "artist": "Artist Name", "title": "Album Title", "genre": "Genre", "year": 2024, "img_url": ""}
   ```

2. Add album art as `/img/{id}.jpg` (600×600px recommended)

3. Add the ID to the `HAS_ART` set in `index.html` to display cover art instead of the vinyl placeholder

4. Update record counts in two places:
   - `#total-label` in the header
   - `#footer-count` in the footer

### Removing an Album

1. Delete the entry from the `ALBUMS` array
2. Remove the ID from the `HAS_ART` set
3. Delete the corresponding `img/{id}.jpg` file
4. Update the record counts

### Downloading Album Art

Use the included utility to bulk-download artwork:

```bash
python3 download_art.py
```

This script queries **MusicBrainz + Cover Art Archive** (no authentication required). For missing artwork, manually source images and convert with:

```bash
sips -s format jpeg input.png --out img/{id}.jpg -Z 600
```

## Project Structure

```
record-collection/
├── index.html         # Single-page app (markup, styles, logic)
├── server.py          # Python development server
├── download_art.py    # Album art batch downloader
├── img/               # Album artwork ({id}.jpg)
└── README.md
```

## License

This project is provided as-is for personal use.
