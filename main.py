from flask import Flask, request, jsonify, Response, abort
from yt_dlp import YoutubeDL
import requests
import uuid

app = Flask(__name__)

ydl_opts = {
    'quiet': True,
    'skip_download': True,
    'format': 'bestaudio',
    'noplaylist': True,
    'nocheckcertificate': True,
}

stream_cache = {}

@app.route('/search')
def search():
    query = request.args.get('q')
    if not query:
        return jsonify({'error': 'Missing query parameter q'}), 400

    with YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(f"ytsearch1:{query}", download=False)['entries'][0]
        except Exception as e:
            return jsonify({'error': 'Failed to fetch info', 'details': str(e)}), 500

    artist = info.get('artist') or info.get('uploader') or 'Unknown'
    title = info.get('title') or 'Unknown'

    # Pick best audio-only format
    audio_formats = [f for f in info.get('formats', []) if f.get('vcodec') == 'none' and f.get('acodec') != 'none' and f.get('url')]
    if not audio_formats:
        return jsonify({'error': 'No audio stream found'}), 404

    # Sort by abr (audio bitrate) descending to get best quality
    audio_formats.sort(key=lambda x: x.get('abr', 0), reverse=True)
    best_audio = audio_formats[0]

    stream_url = best_audio['url']
    http_headers = best_audio.get('http_headers', {})

    stream_id = str(uuid.uuid4())
    stream_cache[stream_id] = (stream_url, http_headers)

    return jsonify({
        'artist': artist,
        'title': title,
        'stream_proxy_url': f"/stream/{stream_id}"
    })

@app.route('/stream/<stream_id>')
def stream(stream_id):
    if stream_id not in stream_cache:
        return abort(404, "Stream ID not found")

    url, headers = stream_cache[stream_id]

    req_headers = {
        'User-Agent': headers.get('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'),
        'Referer': headers.get('Referer', 'https://www.youtube.com/'),
        'Cookie': headers.get('Cookie', ''),
        'Accept': '*/*',
    }

    r = requests.get(url, headers=req_headers, stream=True)
    if r.status_code != 200:
        return abort(r.status_code, "Failed to fetch stream")

    return Response(
        r.iter_content(chunk_size=1024),
        content_type=r.headers.get('content-type'),
        status=r.status_code,
        headers={'Content-Disposition': 'inline'},  # force playback in browser
        direct_passthrough=True,
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
