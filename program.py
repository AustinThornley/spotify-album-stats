"""
Spotify Album Listening Stats
------------------------------
Reads your Spotify extended streaming history (JSON files exported from
Spotify — see https://www.spotify.com/account/privacy/) and produces a
ranked list of your most-played albums, with play counts, total hours
listened, and top tracks per album.

Usage:
    1. Place your Spotify export .json files in a folder named
       "spotify-history" next to this script (or change DATA_FOLDER below).
    2. Run: python spotify_album_stats.py
    3. Results print to the console and are also saved to
       album_statistics.csv in the current directory.

NOTE: Some of these numbers may not be accurate. For example, if you play a single song from an album, that will count as an album play. Feel free to modify the code to suit your needs. This is just for fun and gives me a general idea of my listening habits and how they've changed over the years.
"""

import json
from pathlib import Path
from collections import defaultdict
import csv

# Folder containing your Spotify JSON files
DATA_FOLDER = Path("spotify-history")

# Minimum ms_played for a stream to count as a genuine listen (Spotify logs
# skips too; 30s is a common threshold for filtering those out). Set to 0
# to count every logged event, including skips.
# As is, this would never count a 20s song as played.
MIN_MS_PLAYED = 30_000

UNKNOWN_ARTIST = "Unknown Artist"

albums = defaultdict(lambda: {
    "plays": 0,
    "ms_played": 0,
    "artists": set(),
    "tracks": defaultdict(int)
})

files = sorted(DATA_FOLDER.glob("*.json"))

for file in files:
    try:
        with open(file, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (json.JSONDecodeError, OSError) as e:
        print(f"Skipping {file.name}: {e}")
        continue

    for entry in data:

        # Handle different Spotify export formats
        album = (
            entry.get("master_metadata_album_album_name")
            or entry.get("albumName")
        )

        track = (
            entry.get("master_metadata_track_name")
            or entry.get("trackName")
        )

        artist = (
            entry.get("master_metadata_album_artist_name")
            or entry.get("artistName")
            or UNKNOWN_ARTIST
        )

        ms = (
            entry.get("ms_played")
            or entry.get("msPlayed")
            or 0
        )

        # Skip podcasts/local files/etc.
        if not album or not track:
            continue

        # Skip near-instant skips so they don't inflate play counts
        if ms < MIN_MS_PLAYED:
            continue

        # Key by (album, artist) so same-named albums by different artists
        # (or self-titled albums) don't get merged together
        key = (album, artist)

        albums[key]["plays"] += 1
        albums[key]["ms_played"] += ms
        albums[key]["artists"].add(artist)
        albums[key]["tracks"][track] += 1

# Sort by play count
ranked = sorted(
    albums.items(),
    key=lambda x: x[1]["plays"],
    reverse=True
)

print("\nTop Albums\n")

for i, ((album, _artist), info) in enumerate(ranked[:100], start=1):

    hours = info["ms_played"] / 1000 / 60 / 60
    artist_display = ", ".join(sorted(info["artists"]))

    top_tracks = sorted(
        info["tracks"].items(),
        key=lambda x: x[1],
        reverse=True
    )[:5]

    print(f"{i}. {album}")
    print(f"   Artist: {artist_display}")
    print(f"   Plays: {info['plays']}")
    print(f"   Hours listened: {hours:.1f}")
    print("   Most played tracks:")
    for track, plays in top_tracks:
        print(f"      {track}: {plays}")
    print()

# Export CSV
with open("album_statistics.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)

    writer.writerow([
        "Rank",
        "Album",
        "Artist",
        "Play Count",
        "Hours Listened",
        "Top Track",
        "Top Track Plays"
    ])

    for rank, ((album, _artist), info) in enumerate(ranked, start=1):

        top_track, top_track_plays = max(
            info["tracks"].items(),
            key=lambda x: x[1]
        )

        writer.writerow([
            rank,
            album,
            ", ".join(sorted(info["artists"])),
            info["plays"],
            round(info["ms_played"] / 1000 / 60 / 60, 2),
            top_track,
            top_track_plays
        ])

print("Saved album_statistics.csv")