#!/usr/bin/env python3
"""
Download album art using MusicBrainz + Cover Art Archive.
MusicBrainz rate limit: 1 req/sec (unauthenticated). We honour it with a delay.
"""

import json
import os
import ssl
import time
import urllib.request
import urllib.parse

SSL_CTX = ssl.create_default_context()
SSL_CTX.check_hostname = False
SSL_CTX.verify_mode = ssl.CERT_NONE

HEADERS = {"User-Agent": "VinylCollection/1.0 (personal vinyl catalogue)"}
IMG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "img")
MB_DELAY = 1.1  # seconds between MusicBrainz API calls

ALBUMS = [
    {"id":1,  "artist":"The Doors",                         "title":"L.A. Woman"},
    {"id":2,  "artist":"Jimi Hendrix Experience",           "title":"Are You Experienced"},
    {"id":3,  "artist":"Lawrence Welk",                     "title":"Moon River"},
    {"id":4,  "artist":"Bob Dylan",                         "title":"Waiting for the Sun"},
    {"id":5,  "artist":"The Doors",                         "title":"The Doors"},
    {"id":6,  "artist":"Various Artists",                   "title":"Rocky IV"},
    {"id":7,  "artist":"Neil Young",                        "title":"Harvest"},
    {"id":8,  "artist":"Pete Shelley",                      "title":"Homosapien"},
    {"id":9,  "artist":"Bruce Springsteen",                 "title":"Born in the USA"},
    {"id":10, "artist":"Bruce Springsteen",                 "title":"Darkness on the Edge of Town"},
    {"id":11, "artist":"Bruce Springsteen",                 "title":"Born to Run"},
    {"id":12, "artist":"Eric Clapton",                      "title":"From the Cradle"},
    {"id":13, "artist":"Pink Floyd",                        "title":"Wish You Were Here"},
    {"id":14, "artist":"Creedence Clearwater Revival",      "title":"Cosmo's Factory"},
    {"id":15, "artist":"Johnny Cash",                       "title":"At San Quentin"},
    {"id":16, "artist":"Bob Dylan",                         "title":"Highway 61 Revisited"},
    {"id":17, "artist":"Michael Jackson",                   "title":"Thriller"},
    {"id":18, "artist":"Various Artists",                   "title":"Inside Llewyn Davis"},
    {"id":19, "artist":"Willie Nelson",                     "title":"Always on My Mind"},
    {"id":20, "artist":"Aerosmith",                         "title":"Toys in the Attic"},
    {"id":21, "artist":"Grateful Dead",                     "title":"American Beauty"},
    {"id":22, "artist":"Seagulls",                          "title":"Great Pine"},
    {"id":23, "artist":"Nirvana",                           "title":"MTV Unplugged in New York"},
    {"id":24, "artist":"Led Zeppelin",                      "title":"Led Zeppelin I"},
    {"id":25, "artist":"Derek and the Dominos",             "title":"Layla and Other Assorted Love Songs"},
    {"id":26, "artist":"The Strokes",                       "title":"Future Present Past EP"},
    {"id":27, "artist":"B.B. King",                         "title":"B.B. King's Galaxy"},
    {"id":28, "artist":"Mumford and Sons",                  "title":"Babel"},
    {"id":29, "artist":"Boston",                            "title":"Don't Look Back"},
    {"id":30, "artist":"Stevie Ray Vaughan",                "title":"Live at Carnegie Hall"},
    {"id":31, "artist":"Toadies",                           "title":"Rubberneck"},
    {"id":32, "artist":"Frank Sinatra",                     "title":"Have Yourself a Merry Little Christmas"},
    {"id":33, "artist":"Johnny Cash",                       "title":"The Christmas Spirit"},
    {"id":34, "artist":"Various Artists",                   "title":"Joy to the World"},
    {"id":35, "artist":"Elvis Presley",                     "title":"Elvis Christmas Album"},
    {"id":36, "artist":"Ryan Bingham",                      "title":"Roadhouse Sun"},
    {"id":37, "artist":"Bob Marley",                        "title":"Legend"},
    {"id":38, "artist":"Beck",                              "title":"Morning Phase"},
    {"id":39, "artist":"Jimi Hendrix",                      "title":"Axis Bold as Love"},
    {"id":40, "artist":"Rush",                              "title":"Moving Pictures"},
    {"id":41, "artist":"Billy Idol",                        "title":"Rebel Yell"},
    {"id":42, "artist":"James Taylor",                      "title":"James Taylor"},
    {"id":43, "artist":"The Animals",                       "title":"The Best of the Animals"},
    {"id":44, "artist":"Survivor",                          "title":"Eye of the Tiger"},
    {"id":45, "artist":"Van Halen",                         "title":"Van Halen"},
    {"id":46, "artist":"Jason Isbell and the 400 Unit",     "title":"The Nashville Sound"},
    {"id":47, "artist":"Bob Marley and the Wailers",        "title":"Catch a Fire"},
    {"id":48, "artist":"Sturgill Simpson",                  "title":"The Ballad of Dood and Juanita"},
    {"id":49, "artist":"David Bowie",                       "title":"Labyrinth"},
    {"id":50, "artist":"Fiona Apple",                       "title":"Fetch the Bolt Cutters"},
    {"id":51, "artist":"Jason Isbell",                      "title":"Southeastern"},
    {"id":52, "artist":"Reverend Horton Heat",              "title":"The Full Custom Gospel Sounds"},
    {"id":53, "artist":"Tom Petty and the Heartbreakers",   "title":"The Best of Everything"},
    {"id":54, "artist":"Tom Petty",                         "title":"Wildflowers"},
    {"id":55, "artist":"Sturgill Simpson",                  "title":"A Sailor's Guide to Earth"},
    {"id":56, "artist":"Pearl Jam",                         "title":"Yield"},
    {"id":57, "artist":"Creedence Clearwater Revival",      "title":"Willy and the Poor Boys"},
    {"id":58, "artist":"The Beatles",                       "title":"Abbey Road"},
    {"id":59, "artist":"IDLES",                             "title":"Ultra Mono"},
    {"id":60, "artist":"George Harrison",                   "title":"All Things Must Pass"},
    {"id":61, "artist":"Willie Nelson",                     "title":"Red Headed Stranger"},
    {"id":62, "artist":"David Allan Coe",                   "title":"Greatest Hits"},
    {"id":63, "artist":"IDLES",                             "title":"Joy as an Act of Resistance"},
    {"id":64, "artist":"The Beatles",                       "title":"Revolver"},
    {"id":65, "artist":"Queen",                             "title":"A Night at the Opera"},
    {"id":66, "artist":"Queen",                             "title":"A Day at the Races"},
    {"id":67, "artist":"The Beatles",                       "title":"Rubber Soul"},
    {"id":68, "artist":"The Beatles",                       "title":"Sgt. Pepper's Lonely Hearts Club Band"},
    {"id":69, "artist":"Neil Young",                        "title":"Decade"},
    {"id":70, "artist":"The Strokes",                       "title":"By Blood"},
    {"id":71, "artist":"Willie Nelson",                     "title":"Long Story Short"},
    {"id":72, "artist":"Willie Nelson",                     "title":"Shotgun Willie"},
    {"id":73, "artist":"Chris Stapleton",                   "title":"Traveller"},
    {"id":74, "artist":"Taylor Swift",                      "title":"The Tortured Poets Department"},
    {"id":75, "artist":"Led Zeppelin",                      "title":"Physical Graffiti"},
    {"id":76, "artist":"Willie Nelson",                     "title":"Red Headed Stranger"},
    {"id":77, "artist":"The Strokes",                       "title":"Angles"},
    {"id":78, "artist":"Lana Del Rey",                      "title":"Born to Die"},
    {"id":79, "artist":"The Beatles",                       "title":"The Beatles"},
    {"id":80, "artist":"Sturgill Simpson",                  "title":"Metamodern Sounds in Country Music"},
    {"id":81, "artist":"Elton John",                        "title":"Tumbleweed Connection"},
    {"id":82, "artist":"Stevie Ray Vaughan",                "title":"Soul to Soul"},
    {"id":83, "artist":"Nirvana",                           "title":"Nevermind"},
    {"id":84, "artist":"Stevie Ray Vaughan",                "title":"Couldn't Stand the Weather"},
    {"id":85, "artist":"The Strokes",                       "title":"The New Abnormal"},
    {"id":86, "artist":"Cream",                             "title":"Disraeli Gears"},
    {"id":87, "artist":"Bob Dylan",                         "title":"Bringing It All Back Home"},
    {"id":88, "artist":"Nirvana",                           "title":"Bleach"},
    {"id":89, "artist":"Peter Frampton",                    "title":"Frampton Comes Alive"},
    {"id":90, "artist":"The Doors",                         "title":"The Doors"},
    {"id":91, "artist":"Bob Dylan",                         "title":"The Freewheelin' Bob Dylan"},
    {"id":92, "artist":"Grateful Dead",                     "title":"Workingman's Dead"},
    {"id":93, "artist":"Pink Floyd",                        "title":"The Dark Side of the Moon"},
    {"id":94, "artist":"Nirvana",                           "title":"In Utero"},
    {"id":95, "artist":"The Strokes",                       "title":"Is This It"},
    {"id":96, "artist":"Pearl Jam",                         "title":"Vitalogy"},
    {"id":97, "artist":"The Strokes",                       "title":"Room on Fire"},
    {"id":98, "artist":"The Strokes",                       "title":"First Impressions of Earth"},
    {"id":99, "artist":"Jeff Buckley",                      "title":"Grace"},
    {"id":100,"artist":"Amy Winehouse",                     "title":"Back to Black"},
    {"id":101,"artist":"The Beach Boys",                    "title":"Pet Sounds"},
    {"id":102,"artist":"Rod Stewart",                       "title":"Every Picture Tells a Story"},
    {"id":103,"artist":"Beck",                              "title":"Mutations"},
    {"id":104,"artist":"Arcade Fire",                       "title":"Reflektor"},
    {"id":105,"artist":"Johnny Cash",                       "title":"American IV: The Man Comes Around"},
    {"id":106,"artist":"Led Zeppelin",                      "title":"Led Zeppelin IV"},
    {"id":107,"artist":"Led Zeppelin",                      "title":"Led Zeppelin II"},
    {"id":108,"artist":"Led Zeppelin",                      "title":"Led Zeppelin III"},
    {"id":109,"artist":"Eric Clapton",                      "title":"Slowhand"},
    {"id":110,"artist":"Smashing Pumpkins",                 "title":"Siamese Dream"},
    {"id":111,"artist":"Johnny Cash",                       "title":"At Folsom Prison"},
    {"id":112,"artist":"Beastie Boys",                      "title":"Ill Communication"},
    {"id":113,"artist":"Johnny Cash",                       "title":"Orange Blossom Special"},
]


def mb_search(artist, title):
    """Search MusicBrainz for a release and return the best MBID."""
    # Try strict artist+release query first
    q = f'artist:"{artist}" AND release:"{title}"'
    url = (
        "https://musicbrainz.org/ws/2/release/?"
        + urllib.parse.urlencode({"query": q, "fmt": "json", "limit": 5})
    )
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=10, context=SSL_CTX) as r:
        data = json.loads(r.read())

    releases = data.get("releases", [])

    # Prefer releases with cover art
    for rel in releases:
        if rel.get("cover-art-archive", {}).get("front"):
            return rel["id"]

    # Fall back to first result
    if releases:
        return releases[0]["id"]
    return None


def fetch_cover(mbid):
    """Download cover art from the Cover Art Archive (500px thumbnail)."""
    url = f"https://coverartarchive.org/release/{mbid}/front-500"
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=15, context=SSL_CTX) as r:
        return r.read()


def process_album(album):
    album_id = album["id"]
    dest = os.path.join(IMG_DIR, f"{album_id}.jpg")

    if os.path.exists(dest) and os.path.getsize(dest) > 1000:
        return "skipped"

    time.sleep(MB_DELAY)  # respect MusicBrainz rate limit

    mbid = mb_search(album["artist"], album["title"])
    if not mbid:
        return "not_found"

    time.sleep(MB_DELAY)

    try:
        img_data = fetch_cover(mbid)
        with open(dest, "wb") as f:
            f.write(img_data)
        return "ok"
    except Exception as e:
        # Try release-group endpoint as fallback
        try:
            url = f"https://coverartarchive.org/release-group/{mbid}/front-500"
            req = urllib.request.Request(url, headers=HEADERS)
            with urllib.request.urlopen(req, timeout=15, context=SSL_CTX) as r:
                img_data = r.read()
            with open(dest, "wb") as f:
                f.write(img_data)
            return "ok"
        except Exception as e2:
            return f"error: {e2}"


def main():
    os.makedirs(IMG_DIR, exist_ok=True)
    total = len(ALBUMS)
    ok = skipped = not_found = errors = 0
    failed = []

    print(f"Fetching art for {total} albums via MusicBrainz + Cover Art Archive\n")

    for i, album in enumerate(ALBUMS, 1):
        label = f"[{i:>3}/{total}]"
        name = f"{album['artist']} – {album['title']}"

        result = process_album(album)

        if result == "ok":
            ok += 1
            print(f"  {label} ✓  {name}")
        elif result == "skipped":
            skipped += 1
            print(f"  {label} –  {name}  (already exists)")
        elif result == "not_found":
            not_found += 1
            print(f"  {label} ?  {name}  (not on MusicBrainz)")
            failed.append(album)
        else:
            errors += 1
            print(f"  {label} ✗  {name}  ({result})")
            failed.append(album)

    print(f"\nDone:  ✓ {ok} downloaded  – {skipped} skipped  ? {not_found} not found  ✗ {errors} errors")

    if failed:
        print(f"\nStill missing ({len(failed)}):")
        for a in failed:
            print(f"  [{a['id']}] {a['artist']} – {a['title']}")


if __name__ == "__main__":
    main()
