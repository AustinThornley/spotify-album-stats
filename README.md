# Spotify Album Listening Stats

Python script that reads Spotify extended streaming history JSON files
and outputs a ranked list of most-played albums.

To download your extended history from Spotify, see https://www.spotify.com/account/privacy/.
It told me it could take up to 30 days but I got it within a few hours.

Usage:
- Put your exported `.json` files in `spotify-history/` next to [program.py](program.py).
- Run: `python program.py`
- Output: `album_statistics.csv` with album ranks and top tracks.

Adjust the `DATA_FOLDER` and `MIN_MS_PLAYED` constants in [program.py](program.py)
to your liking if needed.
