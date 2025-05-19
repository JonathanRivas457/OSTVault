# 🎮 Video Game Music Database Extractor
## 📖 Overview

This project extracts and compiles video game music metadata into a local SQLite database, combining developer, game, album, artist, and song information. It emphasizes rich audio features and popularity data for each song.

Tools used:
- [RAWG API](https://rawg.io/apidocs) for game metadata  
- [Spotify API](https://developer.spotify.com/) for album and track discovery  
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) for downloading audio  
- [Essentia](https://essentia.upf.edu/) for local audio feature extraction  

> **Note:** This project was developed and tested on Ubuntu/Linux systems.
## ⚙️ Setup
### 🔑 API Keys

This extractor requires two APIs:  
- RAWG.io (for game metadata)  
- Spotify (for album and track search)

Create a file called `API_KEYS.json` and structure it like so:

```json
{
  "rawg": "your-key",
  "spotify_id": "your-id",
  "spotify_secret": "your-secret"
}

---

### `### 🗃️ Database File`

```md
### 🗃️ Database File

The project uses a local SQLite database.

A **starter database** is included, pre-populated with entries from the following developers:
- Arc System Works  
- Capcom  
- id Software  
- Namco  
- Nintendo  
- PlatinumGames  
- SEGA  
- Square Enix  
- Treyarch  

If downloaded, this file (`starter_db.sqlite`) will be updated with additional extractions. Otherwise, a new file will be created in the root directory during execution.
