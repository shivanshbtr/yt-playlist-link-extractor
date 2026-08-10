# YT Playlist Link Extractor

A small Tkinter GUI that extracts all video links from a YouTube playlist, showing serial number, title, and link — with export to `.txt` and a one-click Windows build.

## Project Structure

```
.
├── yt_playlist_extractor.py   # Main GUI application
├── app_icon.ico               # App icon (used by the build and shortcut)
├── build.bat                  # Windows build script (exe + desktop shortcut)
├── .gitignore                 # Ignores build artifacts and local cache
├── LICENSE                    # MIT License
└── README.md
```

## Requirements

- Python 3.8+
- [yt-dlp](https://github.com/yt-dlp/yt-dlp)

## Run from source

```bash
pip install yt-dlp
python yt_playlist_extractor.py
```

Paste a playlist URL, click **Fetch**. Results appear in a table (# / Title / Link).

- Double-click a row, or select it and click **Copy Selected Link** (or right-click → **Copy Link**), to copy that video's link to clipboard.
- Click **Save to .txt** to export all links as:

```
1. Title - https://www.youtube.com/watch?v=xxxx
2. Title - https://www.youtube.com/watch?v=xxxx
```

## Build a standalone .exe (Windows)

Requires Python installed on the Windows machine.

1. Put `yt_playlist_extractor.py`, `app_icon.ico`, and `build.bat` in the same folder.
2. Double-click `build.bat`.

This will:
- Install `yt-dlp` and `pyinstaller`
- Build `dist\YT Playlist Extractor.exe` with the custom icon
- Create a desktop shortcut pointing to the exe

After that, double-click the desktop shortcut to launch the app — no console window.

## Notes

- Works with public/unlisted playlists. Private playlists are not supported.
- No videos are downloaded; only metadata (title, video ID) is fetched.
- If a large playlist fetches only ~100 videos, your `yt-dlp` is outdated. Fix with:
  ```bash
  pip install -U yt-dlp
  ```

## License

MIT License © 2026 Shivansh Batra — see [LICENSE](LICENSE).
