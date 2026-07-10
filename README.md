# Spotify Album Listening Stats

Python script that reads Spotify extended streaming history JSON files
and outputs a ranked list of most-played albums.

Usage:
- Put your exported `.json` files in `spotify-history/` next to [program.py](program.py).
- Run: `python program.py`
- Output: `album_statistics.csv` with album ranks and top tracks.

Adjust the `DATA_FOLDER` and `MIN_MS_PLAYED` constants in [program.py](program.py)
to your liking if needed.
