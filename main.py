from flask import Flask, request, jsonify
from yt_dlp import YoutubeDL

app = Flask(__name__)

ydl_opts = {
    'quiet': True,
    'skip_download': True,
    'format': 'bestaudio/best',
    'noplaylist': True,
}

@app.route('/search')
def search():
    query = request.args.get('q', '')
    if not query:
        return jsonify({'error': 'Missing query parameter q'}), 400

    with YoutubeDL(ydl_opts) as ydl:
        # Use ytsearch to get first result info
        info = ydl.extract_info(f"ytsearch1:{query}", download=False)['entries'][0]

    artist = info.get('artist') or info.get('uploader') or 'Unknown'
    title = info.get('title') or 'Unknown'
    url = info.get('url')

    # Full stream url can be in 'url' or 'formats' (depending on extraction)
    # Let's try to get the direct stream url from formats if available
    stream_url = None
    if 'formats' in info and len(info['formats']) > 0:
        stream_url = info['formats'][-1]['url']
    else:
        stream_url = url

    return jsonify({
        'artist': artist,
        'title': title,
        'stream_url': stream_url
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
