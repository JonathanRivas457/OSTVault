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

Update the file (`API_KEYS.json`) with your own keys

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

### 📥 yt-dlp

[yt-dlp](https://github.com/yt-dlp/yt-dlp) is used to download audios for tracks located via the Spotify API. This is necessary because Spotify no longer provides detailed track audio features — instead, we analyze the downloaded tracks locally using Essentia.

To install run:
pip install yt-dlp

or refer to [https://github.com/yt-dlp/yt-dlp/wiki/Installation]

### Cookies

You will need to provide yt-dlp with YouTube cookies via a cookies file. Cookies can be obtained via edge, chrome, or firefox estension. Just replace the placeholder cookie file with your own, keeping the name the same

### 🎧 Essentia Models

This project uses pre-trained models from [Essentia](https://essentia.upf.edu/) to extract various musical features, including timbre, rhythm, pitch, and more.

These models are licensed under the [Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International License (CC BY-NC-ND 4.0)](https://creativecommons.org/licenses/by-nc-nd/4.0/).

✅ You are free to use the models for **non-commercial purposes**.  
🚫 Redistribution is permitted **only** as part of this project.  
🛠️ No modifications or derivative works are allowed.
For installation details, refer to [https://essentia.upf.edu/installing.html]

**Credits:**  
Essentia Development Team — [https://essentia.upf.edu/](https://essentia.upf.edu/)

## ▶️ Execution

There are two main scripts:
### 1. `Database_Build.py`

- Fetches all games for the specified developer from RAWG.
- Searches Spotify for potential albums.
- Prompts user to match games with albums (manual input required).
- Enter `-1` if no album match is found to skip the game.

> ⚠️ Edit the script to change the target developer.
### 2. `Populate_Songs.py`

- Downloads songs using `yt-dlp`.
- Extracts audio features using Essentia models.
- Populates the database with detailed song information.

> ⚠️ This step may use a lot of disk space temporarily — downloaded files can be deleted after processing.
