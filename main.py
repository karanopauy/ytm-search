from flask import Flask, jsonify, request
import requests as rq
import json as js
from bs4 import BeautifulSoup as bs
import lxml
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


def spaceAdjuster(name: str) -> str:
    """
    Replaces spaces in a string with '%20' for URL encoding.
    This is useful for constructing URLs with parameters.
    """
    return name.replace(' ', '%20')

HEADERS = {
    "authority": "dab.yeet.su",
    "method": "GET",
    "accept": "*/*",
    "accept-encoding": "gzip, deflate, br, zstd",
    "accept-language": "en-US,en;q=0.9",
    "cookie": "visitor_id=f0381566-6198-42f6-91b6-000746aad507",
    "priority": "u=1, i",
    "referer": "https://dab.yeet.su/",
    "sec-ch-ua": '"Microsoft Edge";v="137", "Chromium";v="137", "Not/A)Brand";v="24"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36 Edg/137.0.0.0",
}

SEARCH_BASE_URL = "https://dab.yeet.su/api/search?q="
SEARCH_EXTRA_QUERY = "&offset=0&type=track"
LYRICS_BASE_URL = 'https://dab.yeet.su/api/lyrics?artist='
STREAM_BASE_URL = 'https://dab.yeet.su/api/stream?trackId='

def get_json_response(url: str) -> dict:
    """
    Makes a synchronous GET request to the given URL with predefined headers
    and returns the JSON response. Raises an exception for bad status codes.
    """
    response = rq.get(url, headers=HEADERS, timeout=10)
    response.raise_for_status()
    return response.json()

def get_track_info_from_dab(song_name: str) -> dict | None:
    """
    Searches for a track on dab.yeet.su and returns the first track's info.
    Returns None if no track is found or an error occurs.
    This is for internal use by getTopSongs to get track IDs and audio quality.
    """
    encoded_name = spaceAdjuster(song_name)
    search_url = f"{SEARCH_BASE_URL}{encoded_name}{SEARCH_EXTRA_QUERY}"
    try:
        data = get_json_response(search_url)
        # Return the first track or None if 'tracks' is empty
        return data['tracks'][0] if data and 'tracks' in data and len(data['tracks']) > 0 else None
    except (rq.exceptions.RequestException, KeyError, IndexError, js.JSONDecodeError) as e:
        print(f"ERROR: Could not get track info from dab.yeet.su for '{song_name}': {e}")
        return None

# --- End of functions from dab-yeet-su-scraper-clean ---


# This is your getTopSongs function, now ready for the server.
def getTopSongs():
    """
    Fetches the top 10 songs from Billboard Hot 100.
    For each song, it also attempts to find its trackId and audioQuality from dab.yeet.su.
    Returns a list of dictionaries, each containing 'title', 'artist', 'id', and 'audioQuality'.
    Handles errors gracefully.
    """
    top_songs_data = []
    billboard_url = 'https://www.billboard.com/charts/hot-100/'

    try:
        response = rq.get(billboard_url, headers=HEADERS, timeout=10)
        response.raise_for_status()
    except rq.exceptions.RequestException as e:
        print(f"ERROR: Failed to fetch Billboard data. Network probably died or Billboard hates us: {e}")
        return []

    soups = bs(response.text, 'lxml')

    chart_list_container = soups.find('div', class_='chart-results-list')
    if not chart_list_container:
        print("ERROR: Could not find the main chart container. Billboard HTML structure changed.")
        return []

    song_containers = chart_list_container.find_all('div', class_='o-chart-results-list-row-container')[:10]
    if not song_containers:
        print("ERROR: No song containers found. Billboard HTML structure changed or page is empty.")
        return []

    for song_soup in song_containers:
        title = None
        artist = None
        track_id = None
        audio_quality = None # Initialize audio_quality
        albumCover = None

        try:
            title_element = song_soup.find('h3', id='title-of-a-story', class_='c-title')
            if title_element:
                title = title_element.get_text(strip=True)

            artist_link = song_soup.find('a', class_='c-label', href=lambda href: href and '/artist/' in href)
            if artist_link:
                artist = artist_link.get_text(strip=True)
            else:
                potential_artist_elements = song_soup.find_all(['span', 'a'], class_='c-label')
                for element in potential_artist_elements:
                    text = element.get_text(strip=True)
                    if text and \
                       text != title and \
                       not text.isdigit() and \
                       'Week' not in text and \
                       'Last Week' not in text and \
                       'Peak' not in text and \
                       'NEW' not in text and \
                       'RE-ENTRY' not in text:
                        artist = text
                        break
            
            albumCover_link = song_soup.find('img', class_='c-lazy-image__img lrv-u-background-color-grey-lightest lrv-u-width-100p lrv-u-display-block lrv-u-height-auto')
            if albumCover_link:
                albumCover = (albumCover_link.get('src')).replace('180x180', '240x240')
            else:
                albumCover = 'https://placehold.co/600x400'

            
            if title and artist:
                search_query = f"{title} {artist}"
                dab_track_info = get_track_info_from_dab(search_query)
                if dab_track_info:
                    track_id = dab_track_info.get('id')
                    audio_quality = dab_track_info.get('audioQuality')
                else:
                    print(f"WARNING: Could not find dab.yeet.su ID or audio quality for '{title}' by '{artist}'.")

        except Exception as e:
            print(f"WARNING: Could not parse title, artist, or dab.yeet.su ID/audio quality for a song. Skipping. Error: {e}")
            title = title if title else "UNKNOWN TITLE"
            artist = artist if artist else "UNKNOWN ARTIST"

        if title and artist:
            top_songs_data.append({
                'title': title,
                'artist': artist,
                'id': track_id,
                'audioQuality': audio_quality,
                'albumCover': albumCover,
            })
        else:
            print(f"WARNING: Skipping a song due to missing title or artist after parsing attempts. Title: {title}, Artist: {artist}")

    return top_songs_data

@app.route('/top-songs', methods=['GET'])
def top_songs_endpoint():
    songs = getTopSongs()
    return jsonify(songs)


@app.route('/search-tracks', methods=['GET'])
def search_tracks_endpoint():
    song_name = request.args.get('q')

    if not song_name:
        return jsonify({"error": "Missing 'q' parameter (song name) in query."}), 400

    encoded_name = spaceAdjuster(song_name)
    search_url = f"{SEARCH_BASE_URL}{encoded_name}{SEARCH_EXTRA_QUERY}"

    try:
        data = get_json_response(search_url)
        tracks = data.get('tracks', [])
        return jsonify(tracks)
    except (rq.exceptions.RequestException, KeyError, js.JSONDecodeError) as e:
        print(f"ERROR: Could not search for tracks for '{song_name}': {e}")
        return jsonify({"error": f"Failed to search for tracks: {e}"}), 500


@app.route('/get-stream-url', methods=['GET'])
def get_stream_url_endpoint():
    track_id = request.args.get('trackId')

    if not track_id:
        return jsonify({"error": "Missing 'trackId' parameter in query."}), 400

    try:
        track_id = int(track_id)
    except ValueError:
        return jsonify({"error": "Invalid 'trackId' parameter. Must be an integer."}), 400

    stream_url = f"{STREAM_BASE_URL}{track_id}"
    try:
        data = get_json_response(stream_url)
        return jsonify({"url": data['url']})
    except (rq.exceptions.RequestException, KeyError, js.JSONDecodeError) as e:
        print(f"ERROR: Could not get stream URL for track ID {track_id}: {e}")
        return jsonify({"error": f"Failed to get stream URL: {e}"}), 500


@app.route('/get-lyrics', methods=['GET'])
def get_lyrics_endpoint():
    artist_name = request.args.get('artist')
    title = request.args.get('title')

    if not artist_name or not title:
        return jsonify({"error": "Missing 'artist' or 'title' parameters in query."}), 400

    encoded_artist = spaceAdjuster(artist_name)
    encoded_title = spaceAdjuster(title).split('(')[0]
    lyrics_url = f"{LYRICS_BASE_URL}{encoded_artist}&title={encoded_title}"

    try:
        data = get_json_response(lyrics_url)
        lyrics_text = data.get('lyrics', 'No Lyrics Found')
        return jsonify({"lyrics": lyrics_text})
    except (rq.exceptions.RequestException, js.JSONDecodeError) as e:
        print(f"ERROR: Could not get lyrics for '{title}' by '{artist_name}': {e}")
        return jsonify({"lyrics": "No Lyrics Found (Error during fetch)"}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)
