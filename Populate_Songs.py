import requests
import base64
import json
import yt_dlp
import os
import re
import time
import sqlite3
import ffmpeg
from Audio_Features import get_audio_features


with open("API_KEYS.json", "r") as file:
    keys = json.load(file)

rawg_key = keys["rawg"]
spotify_client_id = keys["spotify_id"]
spotify_client_secret = keys["spotify_secret"]
spotify_key = keys["spotify"]


def create_song_table(conn, cursor):
    conn.execute("PRAGMA foreign_keys = ON")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS song
        (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            song_name TEXT,
            song_genre TEXT,
            approachability_score REAL,
            engagement_score REAL,
            danceability_score REAL,
            aggressiveness_score REAL,
            happiness_score REAL,
            party_score REAL,
            relaxed_score REAL,
            saddness_score REAL,
            electronic_score REAL,
            acoustic_score REAL,
            album_id INTEGER,
            game_id INTEGER,
            artist_id INTEGER,
            FOREIGN KEY(album_id) REFERENCES album(id),
            FOREIGN KEY(game_id) REFERENCES game(id),
            FOREIGN KEY(artist_id) REFERENCES artist(id)
        )
    """)


def sanitize_text(text):
    
    return re.sub(r'[^a-zA-Z0-9\s]', '', text)


def get_access_token(client_id, client_secret):
    auth_url = 'https://accounts.spotify.com/api/token'
    auth_header = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()

    headers = {
        'Authorization': f'Basic {auth_header}'
    }

    data = {
        'grant_type': 'client_credentials'
    }

    response = requests.post(auth_url, headers=headers, data=data)
    
    if response.status_code == 200:
        return response.json()['access_token']
    else:
        raise Exception(f"Failed to get token: {response.status_code}, {response.text}")



def search_album(query, access_token, limit=10):
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    
    params = {
        'q': query,
        'type': 'album',
        'limit': limit
    }

    response = requests.get('https://api.spotify.com/v1/search', headers=headers, params=params)

    inc = 0
    album_list = []
    if response.status_code == 200:
        for album in response.json()['albums']['items']:
            print(f"{inc}:{album['name']}")
            album_list.append(album)
            inc += 1
    else:
        print(f"Search failed: {response.status_code}")
        print(response.text)
    
    user_input = input("Enter number of album or -1 if correct album wasn't found (will be skipped): ")

    if user_input == "-1":
        return None

    else:
        album_data = {'name': album_list[int(user_input)]['name'], 'artists': ', '.join([artist['name'] for artist in album_list[int(user_input)]['artists']]), 'id': album_list[int(user_input)]['id']}
        return album_data
    

def get_popularity_score(track_url):
    match = re.search(r'track/([a-zA-Z0-9]+)', track_url)
    if not match:
        raise ValueError("Invalid Spotify track URL")
    track_id = match.group(1)

    # Build request
    url = f'https://api.spotify.com/v1/tracks/{track_id}'
    headers = {
        'Authorization': f'Bearer {spotify_key}'
        }
    
    # Make request
    response = requests.get(url, headers=headers)
    track_data = response.json()

    popularity = track_data['popularity']
    return popularity


def search_song(developer, game, track_list, conn, cursor, album_id, game_id, artist_id, max_results=1):

    for track in track_list:
        dl_result = 1
        track_name = track['name']
        track_popularity = get_popularity_score(track['external_urls']['spotify'])  
        
        sanitized_name = sanitize_text(track_name)

        search_query = f"ytsearch{max_results}:{game} OST {track_name}"

        print({f"Working on song {track_name}"})

        if os.path.exists(f"WAVFiles/{developer}/{game}/{sanitized_name}.wav"):
            print(f"Song {track_name} has already been downloaded")

        else:
            with yt_dlp.YoutubeDL({'quiet': True, 'no_warnings': True}) as ydl:
                results = ydl.extract_info(search_query, download=False)


            if not results['entries']:
                print(f"Unable to process song {track_name}")
                continue

            else:
                print(results['entries'][0]['original_url'])
                dl_result = download_song(results['entries'][0]['original_url'], developer, game, sanitized_name, search_query)

        db_query = f"SELECT id FROM song WHERE song_name = ? AND game_id = ? AND album_id = ?"
        cursor.execute(db_query, (sanitized_name, game_id, album_id))
        result = cursor.fetchone()

        if dl_result == 0:
            print(f"Song {track_name} is too large to process, skiping...")
            continue

        if result:
            print(f"Song {track_name} already exists in database")
            continue
        
        else:
            track_features = get_audio_features(f"WAVFiles/{developer}/{game}/{sanitized_name}.wav")

            if track_features == -1:
                print(f"Unable to process song {track_name}")
                continue

            db_query = f"""
            INSERT INTO song
            (
                song_name,
                song_genre,
                approachability_score,
                engagement_score,
                danceability_score,
                aggressiveness_score,
                happiness_score,
                party_score,
                relaxed_score,
                saddness_score,
                electronic_score,
                acoustic_score,
                album_id,
                game_id,
                artist_id,
                popularity_score
            )

            VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
        # Ensure track_features[1] to track_features[10] are floats rounded to 2 decimals
        cleaned_features = [track_features[0]] + [round(float(f), 2) for f in track_features[1:11]]

        # Build values tuple
        values = (
            sanitized_name,
            *cleaned_features,  # Unpack all 11 features (index 0 to 10)
            album_id,
            game_id,
            artist_id,
            track_popularity
        )

        # Execute and commit
        cursor.execute(db_query, values)
        conn.commit()

    db_query = f"""UPDATE album
                   SET songs_processed = ?
                   WHERE id = ?;"""
    values = (1, album_id)
    cursor.execute(db_query, values)
    conn.commit()

    return


def download_song(url, developer, game, song, search_query):

    webm_directory = f"WEBMFiles/{developer}/{game}"
    wav_directory = f"WAVFiles/{developer}/{game}"

    if not os.path.exists(webm_directory):
        os.makedirs(webm_directory)

    if not os.path.exists(wav_directory):
        os.makedirs(wav_directory)

    try:
            ydl_opts = {
                'cookies': 'cookies.txt',
                'format': 'bestaudio[ext=webm]/bestaudio/best',
                'outtmpl': f'{webm_directory}/{song}.%(ext)s',
                'socket_timeout': 120,
                'download_sections': ['*00:00:00-00:05:00'],
                'retries': 5,
                'retry_sleep': 30,
                'quiet': True,
                'no_range': True,
                'postprocessor_args': ['-ac', '1', '-ar', '16000']
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
                info = ydl.extract_info(search_query, download=True)

        
            
            if 'entries' in info and info['entries']:
                ext = info['entries'][0]['ext']
            else:
                ext = info['ext']

    except yt_dlp.utils.DownloadError as e:
        print(f"Attempt failed: {e}")

    time.sleep(10)

    input_file = os.path.join(webm_directory, f"{song}.{ext}")
    output_file = os.path.join(wav_directory, f"{song}.wav")

    size_mb = os.path.getsize(input_file) / (1024 * 1024)

    if size_mb >= 31:
        print(f"File too large, skipping")
        return 0  # use as-is
    
    try:
        ffmpeg.input(input_file).output(output_file).run(capture_stdout=True, capture_stderr=True)
    
    except ffmpeg.Error as e:
        print("stdout:", e.stdout.decode())
        print("stderr:", e.stderr.decode())
        raise e

    return 1


def get_track_list(album_url, spotify_key):

    match = re.search(r'album/([a-zA-Z0-9]+)', album_url)
    album_id = match.group(1) if match else None

    headers = {
    "Authorization": f"Bearer {spotify_key}"
    }
    tracks = []
    limit = 50  # max allowed by Spotify
    offset = 0

    while True:
        url = f"https://api.spotify.com/v1/albums/{album_id}/tracks"
        params = {
            "limit": limit,
            "offset": offset
        }
        response = requests.get(url, headers=headers, params=params)
        data = response.json()

        tracks.extend(data["items"])

        if data["next"] is None:
            break

        offset += limit

    return tracks

conn = sqlite3.connect("games.db")
cursor = conn.cursor()

db_query = f""" SELECT album.id, album.artist_id, album.game_id, album.spotify_link, game.game_title, developer.developer_name
            FROM album
            JOIN game ON album.game_id = game.id
            JOIN developer ON game. developer_id= developer.id
            WHERE album.songs_processed = ?
            """
values = (0,)
cursor.execute(db_query, values)
result = cursor.fetchall()
print(result)

create_song_table(conn, cursor)

spotify_key = get_access_token(spotify_client_id, spotify_client_secret)

for album in result:
    track_list = get_track_list(album[3], spotify_key)
    search_song(album[5], album[4], track_list, conn, cursor, album[0], album[2], album[1])

# album_data = search_album(game, spotify_key)
# track_list = get_tracks(album_data["id"])
#def search_song(developer, game, track_list, conn, cursor, album_id, game_id, artist_id, max_results=1):
