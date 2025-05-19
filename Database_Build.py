import sqlite3
import requests
import json
import base64

with open('API_KEYS.json', 'r') as file:
    keys = json.load(file)

rawg_key = keys['rawg']
spotify_client_id = keys['spotify_id']
spotify_client_secret = keys['spotify_secret']
spotify_key = ""

genres = ['Action', 'Indie', 'Adventure', 'RPG', 'Strategy', 'Shooter', 'Casual', 
          'Simulation', 'Puzzle', 'Arcade', 'Platformer', 'Massively_Multiplayer', 'Racing', 
          'Sports', 'Fighting', 'Family', 'Board_Games', 'Card', 'Educational']

conn = sqlite3.connect("games.db")
cursor = conn.cursor()


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



def search_album(game_title, limit=20):
    query = game_title + " soundtrack"
    headers = {
        'Authorization': f'Bearer {spotify_key}'
    }
    
    params = {
        'q': query,
        'type': 'album',
        'limit': limit
    }

    response = requests.get('https://api.spotify.com/v1/search', headers=headers, params=params)

    inc = 0
    album_list = []
    print("Game: " + game_title)
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
        album_data = {'name': album_list[int(user_input)]['name'], 'artist': ', '.join([artist['name'] for artist in album_list[int(user_input)]['artists']]), 'link':album_list[int(user_input)]['external_urls']['spotify']}
        return album_data

def get_genre_list(game):
    raw_genres = game['genres']
    clean_genres = []
    sql_genres = []

    for genre in raw_genres:
        clean_genres.append(genre['name'])

    for genre in genres:
        if genre in clean_genres:
            sql_genres.append(1)
        else:
            sql_genres.append(0)
    
    return sql_genres


def setup_tables(conn, cursor):
    conn.execute("PRAGMA foreign_keys = ON")

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS developer
        (   
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            developer_name TEXT UNIQUE
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS game (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            developer_id INTEGER,
            game_title TEXT UNIQUE, 
            release_date DATE,
            action INTEGER,
            indie INTEGER,
            adventure INTEGER,
            rpg INTEGER,
            strategy INTEGER,
            shooter INTEGER,
            casual INTEGER,
            simulation INTEGER,
            puzzle INTEGER,
            arcade INTEGER,
            platformer INTEGER,
            massively_multiplayer INTEGER,
            racing INTEGER,
            sports INTEGER,
            fighting INTEGER,
            family INTEGER,
            board_games INTEGER,
            card INTEGER,
            educational INTEGER,
            FOREIGN KEY(developer_id) REFERENCES developer(id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS artist (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            artist_name TEXT UNIQUE
            )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS album (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            album_title TEXT UNIQUE,
            artist_id INTEGER,
            game_id INTEGER,
            spotify_link TEXT,
            songs_processed INTEGER,
            FOREIGN KEY(artist_id) REFERENCES artist(id), 
            FOREIGN KEY(game_id) REFERENCES game(id)
            )
    
    """)


def get_developer_id(dev_name, conn, cursor):
    
    url = "https://api.rawg.io/api/developers"

    params = {
            "key":rawg_key,
            "search":dev_name,
            "page_size":1
        }

    response = requests.get(url, params=params)
    print(response)
    data = response.json()
    print(data)

    if data['results']:

        query = "SELECT id FROM developer WHERE developer_name = ?"
        cursor.execute(query, (dev_name,))
        result = cursor.fetchone()

        if result:
            print(f"{dev_name} already exists in database")
            return data['results'][0]['id']

        else:
            query = f"""
                INSERT INTO developer
                (
                    developer_name
                )
                VALUES
                (   
                    ?
                )
            """

            values = (dev_name,)
            cursor.execute(query, values)
            conn.commit()

            return data['results'][0]['id']
    
    else:
        print(f"Unable to find dev id for {dev_name}")
        return


def insert_artist(album_data, conn, cursor):
    artist_name = album_data['artist']

    query = "SELECT id FROM artist WHERE artist_name = ?"
    cursor.execute(query, (artist_name,))
    result = cursor.fetchone()

    if result:
        print(f"Artist {album_data['artist']} already exists in database")
        artist_id = result[0]
    
    else:
        query = """
            INSERT INTO artist(
                artist_name
            )

            VALUES(
                ?
            )
        """

        values = (album_data['artist'],)
        cursor.execute(query, values)
        conn.commit

        query = f""" SELECT id FROM artist WHERE artist_name = ?"""
        cursor.execute(query, (album_data['artist'],))
        artist_id = cursor.fetchone()[0]

    return artist_id


def insert_album(album_data, game_id, artist_id, conn, cursor):
    query = f"""SELECT id FROM album WHERE album_title = ?"""
    cursor.execute(query, (album_data['name'],))
    result = cursor.fetchone()

    if result:
        print(f"Album {album_data['name']} already exists in database")
        album_id = result[0]

    else:
        query = """
            INSERT INTO album(
                album_title, artist_id, game_id, spotify_link, songs_processed
                )

            VALUES(
                ?, ?, ?, ?, ?
                )
        """
        values = (album_data['name'], artist_id, game_id, album_data['link'], 0)
        cursor.execute(query, values)
        conn.commit()

        query = f"""SELECT id FROM album WHERE album_title = ?"""
        cursor.execute(query, (album_data['name'],))
        album_id = cursor.fetchone()[0]

    return album_id


def insert_game(game_title, release_date, genre_list, dev_id, conn, cursor):
    query = f"""
    SELECT id FROM game WHERE game_title = ?
    """
    cursor.execute(query, (game_title,))
    result = cursor.fetchone()

    if result:
        print(f"{game_title} already exists in database")
        game_id = result[0]

    else:

        query = f"""
        INSERT INTO game
        (   
            developer_id, game_title, release_date, {','.join(genres)}
        )
        VALUES
        (
            ?, ?, ?, {', '.join(['?'] * len(genres))}
        )
        """

        values = (dev_id, game_title, release_date, *genre_list)
        cursor.execute(query, values)
        conn.commit()

        query = f"""
        SELECT id FROM game WHERE game_title = ?
        """
        cursor.execute(query, (game_title,))
        game_id = cursor.fetchone()[0]

    return game_id


def get_game_data(dev_id, dev_name, conn, cursor, max_pages=1):

    url = "https://api.rawg.io/api/games"

    query = f"""
        SELECT Id FROM developer WHERE developer_name = ?
    """

    cursor.execute(query, (dev_name,))
    result = cursor.fetchone()

    if result:
        dev_sql_id = result[0]
    
    else:
        print(f"Unable to find {dev_name} in developers table")

    for page in range(1, max_pages + 1):
        params = {
                "key":rawg_key,
                "page":page,
                "developers":dev_id,
                "page_size": 30,
                "ordering":"-added"
        }

        response = requests.get(url, params=params)
        data = response.json()

        games = data['results']

        for game in games:
            game_title = game['name']
            release_date = game['released']
            genre_list = get_genre_list(game)
            album_data = search_album(game_title)

            if not album_data:
                print(f"Unable to find album data for {game_title}")
                continue

            game_id = insert_game(game_title, release_date, genre_list, dev_sql_id, conn, cursor)
            artist_id = insert_artist(album_data, conn, cursor)  
            album_id = insert_album(album_data, game_id, artist_id, conn, cursor)
            

spotify_key = get_access_token(spotify_client_id, spotify_client_secret)
dev_name = "Capcom"
setup_tables(conn, cursor)
dev_id = get_developer_id(dev_name, conn, cursor)
get_game_data(dev_id, dev_name, conn, cursor)

conn.close()

