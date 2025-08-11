from flask import Flask, request, jsonify, Response, abort
from yt_dlp import YoutubeDL
import requests

app = Flask(__name__)

ydl_opts = {
    'quiet': True,
    'skip_download': True,
    'format': 'bestaudio/best',
    'noplaylist': True,
    'nocheckcertificate': True,
}

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

    # Pick best audio format URL and headers
    format_info = None
    for f in reversed(info.get('formats', [])):
        if f.get('acodec') != 'none' and f.get('url'):
            format_info = f
            break
    if not format_info:
        return jsonify({'error': 'No audio stream found'}), 404

    stream_url = format_info['url']
    http_headers = format_info.get('http_headers', {})

    return jsonify({
        'artist': artist,
        'title': title,
        'stream_proxy_url': f"/stream?url={stream_url}"
    })

@app.route('/stream')
def stream():
    url = request.args.get('url')
    if not url:
        return abort(400, "Missing url param")

    # Ideally, you'd want to whitelist URLs or sign these URLs to avoid abuse

    # For demo, proxy stream with minimal headers
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
        'Accept': '*/*',
        'Referer': 'https://www.youtube.com/',
    }

    r = requests.get(url, headers=headers, stream=True)
    if r.status_code != 200:
        return abort(r.status_code, "Failed to fetch stream")

    return Response(
        r.iter_content(chunk_size=1024),
        content_type=r.headers.get('content-type'),
        status=r.status_code,
        direct_passthrough=True,
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
