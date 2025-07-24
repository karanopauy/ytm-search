import yt_dlp
from flask_cors import CORS
from flask import Flask, request, jsonify
import os
proxy_url = '160.251.142.232:80'
os.environ["http_proxy"] = proxy_url
os.environ["https_proxy"] = proxy_url
os.environ["HTTP_PROXY"] = proxy_url  # uppercase variants sometimes needed
os.environ["HTTPS_PROXY"] = proxy_url

app = Flask(__name__)
CORS(app)

def get_stream_url(song_name):
    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'simulate': True,
        'force_generic_extractor': True,
        'noplaylist': True,
        'skip_download': True,
        'extract_audio': True,
        'audio_format': 'best',
        'audio_quality': 0,
        'default_search': 'ytsearch',
        # 'cookiefile' : 'D:\\Projects\\CppAndPython\\music playing\\ytcookie.txt',
    }

    try:
        info_dict = None
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(f"ytsearch1:{song_name}", download=False)

        if not info_dict or 'entries' not in info_dict or not info_dict['entries']:
            return jsonify({"error":"Song not found", "code" : 404}), 404
        
        first_entry_info = info_dict['entries'][0]

        is_music = 'Music' in first_entry_info.get('categories', []) or \
                   (first_entry_info.get('category') == 'Music')
        
        if not is_music:
            return jsonify({"error" : "Result yeilds no music", "code": 503}), 503
        
        title = first_entry_info['title']

        if not title:
            title = "Couldn't fetch title :("

        thumb = first_entry_info['thumbnail']

        if not thumb:
            thumb = "Couldn't fetch album cover :("
        
        stream_url = first_entry_info.get('url')

        if not stream_url:
            return jsonify({"error": "no link to stream", "code" : 401}), 401
        
        return jsonify({"stream url": stream_url, "code" : 200, "title": title, "cover" : thumb}), 200
    
    except Exception as e:
        return jsonify({"error" : "Failed to fetch from youtube", "code" : 403}), 403

@app.route('/search', methods=['GET'])
def search():
    song_name = request.args.get('q')

    if not song_name:
        return jsonify({"error": "Missing 'q' parameter (song name) in query.", "code" : 400}), 400

    return get_stream_url(song_name)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)
