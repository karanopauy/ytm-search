import requests as rq
import time
import datetime
import yt_dlp
from flask_cors import CORS
from flask import Flask, request, jsonify

app = Flask(__name__)
CORS(app)


def search_result(query):
    ydl_opts = {
        "format": "bestaudio/best",
        "extract_flat": True,
        "quiet": True,
        "noplaylist": True,
        "skip_download": True,
        "extract_audio": True,
        "audio_format": "best",
        "audio_quality": 0,
        "dump_single_json": True,
        "logger": None,
    }
    cookie = {
        "__Secure-1PAPISID": "ur",
        "__Secure-1PSID": "ur",
        "__Secure-1PSIDCC": "ur",
        "__Secure-1PSIDTS": "ur",
        "__Secure-3PAPISID": "ur",
        "__Secure-3PSID": "ur",
        "__Secure-3PSIDCC": "ur",
        "__Secure-3PSIDTS": "ur",
        "__Secure-ROLLOUT_TOKEN": "ur",
        "APISID": "ur",
        "HSID": "ur",
        "LOGIN_INFO": "ur",
        "NID": "ur",
        "PREF": "ure",
        "s_gl": "TR",
        "SAPISID": "ur",
        "SID": "ur",
        "SIDCC": "ur",
        "SOCS": "ur",
        "SSID": "ur",
        "VISITOR_INFO1_LIVE": "ur",
        "VISITOR_PRIVACY_METADATA": "ur",
    }
    cookie_header_value = "; ".join([f"{key}={value}" for key, value in cookie.items()])
    now_utc = datetime.datetime.now(datetime.timezone.utc)
    client_version_date_str = now_utc.strftime("%Y%m%d")
    dynamic_client_version = f"1.{client_version_date_str}.03.00"
    unix_timestamp_sec_float = time.time()
    dynamic_creation_time_usec = str(int(unix_timestamp_sec_float * 1_000_000))
    dynamic_dt_msec = str(int(unix_timestamp_sec_float * 1_000))
    payload = {
        "context": {
            "client": {
                "hl": "en-GB",
                "gl": "TR",
                "remoteHost": "uuurrr",
                "deviceMake": "",
                "deviceModel": "",
                "visitorData": "ur",
                "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:140.0) Gecko/20100101 Firefox/140.0,gzip(gfe)",
                "clientName": "WEB_REMIX",
                "clientVersion": dynamic_client_version,
                "osName": "Windows",
                "osVersion": "10.0",
                "originalUrl": "https://music.youtube.com/",
                "screenPixelDensity": 1,
                "platform": "DESKTOP",
                "clientFormFactor": "UNKNOWN_FORM_FACTOR",
                "configInfo": {
                    "appInstallData": "ur",
                    "coldConfigData": "ur",
                    "coldHashData": "ur",
                    "hotHashData": "ur",
                },
                "screenDensityFloat": 1.25,
                "userInterfaceTheme": "USER_INTERFACE_THEME_DARK",
                "timeZone": "Europe/Bucharest",  # Note: This is a fixed string. You could make this dynamic too if needed, based on host system's timezone.
                "browserName": "Firefox",
                "browserVersion": "140.0",
                "acceptHeader": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "deviceExperimentId": "ur",
                "rolloutToken": "ur",
                "screenWidthPoints": 1536,
                "screenHeightPoints": 257,
                "utcOffsetMinutes": 180,  # Note: This is fixed. Could be dynamic based on timezone.
                "musicAppInfo": {
                    "pwaInstallabilityStatus": "PWA_INSTALLABILITY_STATUS_UNKNOWN",
                    "webDisplayMode": "WEB_DISPLAY_MODE_BROWSER",
                    "storeDigitalGoodsApiSupportStatus": {
                        "playStoreDigitalGoodsApiSupportStatus": "DIGITAL_GOODS_API_SUPPORT_STATUS_UNSUPPORTED"
                    },
                },
            },
            "user": {"lockedSafetyMode": False},
            "request": {
                "useSsl": True,
                "internalExperimentFlags": [],
                "consistencyTokenJars": [],
                "innertubeTokenJar": {
                    "appTokens": [
                        {
                            "type": 2,
                            "value": "ur=",
                            "maxAgeSeconds": 86400,
                            # DYNAMIC creationTimeUsec
                            "creationTimeUsec": dynamic_creation_time_usec,
                        }
                    ]
                },
            },
            "adSignalsInfo": {
                "params": [
                    # DYNAMIC dt
                    {"key": "dt", "value": dynamic_dt_msec},
                    {"key": "flash", "value": "0"},
                    {"key": "frm", "value": "0"},
                    {"key": "u_tz", "value": "180"},
                    {"key": "u_his", "value": "2"},
                    {"key": "u_h", "value": "864"},
                    {"key": "u_w", "value": "1536"},
                    {"key": "u_ah", "value": "816"},
                    {"key": "u_aw", "value": "1536"},
                    {"key": "u_cd", "value": "24"},
                    {"key": "bc", "value": "31"},
                    {"key": "bih", "value": "257"},
                    {"key": "biw", "value": "1536"},
                    {"key": "brdim", "value": "-7,-7,-7,-7,1536,0,1550,830,1536,257"},
                    {"key": "vis", "value": "1"},
                    {"key": "wgl", "value": "true"},
                    {"key": "ca_type", "value": "image"},
                ]
            },
            "activePlayers": [{"playerContextParams": "Q0FFU0FnZ0I="}],
        },
        "query": query,
        "suggestStats": {
            "validationStatus": "VALID",
            "parameterValidationStatus": "VALID_PARAMETERS",
            "clientName": "youtube-music",
            "searchMethod": "ENTER_KEY",
            "inputMethods": ["KEYBOARD"],
            "originalQuery": query,
            "availableSuggestions": [
                {"index": 0, "type": 0},
                {"index": 1, "type": 0},
                {"index": 2, "type": 0},
                {"index": 3, "type": 0},
                {"index": 4, "type": 0},
                {"index": 5, "type": 0},
                {"index": 6, "type": 0},
                {"index": 7, "type": 0},
                {"index": 8, "type": 0},
            ],
            "zeroPrefixEnabled": True,
            "firstEditTimeMsec": 51258,
            "lastEditTimeMsec": 55640,
        },
    }
    headers = {
        "POST": "/youtubei/v1/search?prettyPrint=false HTTP/2",
        "Host": "music.youtube.com",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:140.0) Gecko/20100101 Firefox/140.0",
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Content-Type": "application/json",
        "Content-Length": "3713",
        "Referer": "https://music.youtube.com/",
        "X-Goog-Visitor-Id": "ur",
        "X-Youtube-Bootstrap-Logged-In": "true",
        "X-Youtube-Client-Name": "67",
        "X-Youtube-Client-Version": "1.20250716.03.00",
        "X-Goog-AuthUser": "1",
        "X-Origin": "https://music.youtube.com",
        "Origin": "https://music.youtube.com",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "same-origin",
        "Sec-Fetch-Site": "same-origin",
        "Authorization": "ur",
        "Connection": "keep-alive",
        "Cookie": cookie_header_value,  # This is where the variable cookie value is used
        "Priority": "u=0",
        "TE": "trailers",
    }
    url = "https://music.youtube.com/youtubei/v1/search?prettyPrint=false"
    try:
        try:
            response = rq.post(
                url, headers=headers, json=payload, cookies=cookie
            ).json()
        except:
            return jsonify({"Error": "Youtube is mad", "code": 404}), 404
        response = response["contents"]["tabbedSearchResultsRenderer"]["tabs"][0][
            "tabRenderer"
        ]["content"]["sectionListRenderer"]["contents"][1]["musicCardShelfRenderer"]
        type = response["subtitle"]["runs"][0]["text"]
        try:
            thumbnail = (
                response["thumbnail"]["musicThumbnailRenderer"]["thumbnail"][
                    "thumbnails"
                ][1]["url"]
            ).replace("120", "720")
        except:
            thumbnail = (
                response["thumbnail"]["musicThumbnailRenderer"]["thumbnail"][
                    "thumbnails"
                ][0]["url"]
            ).replace("120", "720")
        title = response["title"]["runs"][0]["text"]
        videoUrl = (
            "https://music.youtube.com/watch?v="
            + response["title"]["runs"][0]["navigationEndpoint"]["watchEndpoint"][
                "videoId"
            ]
        )
        artist = response["subtitle"]["runs"][2]["text"]
        runtime = response["subtitle"]["runs"][4]["text"]
        try:
            isExplicit = response["subtitleBadges"][0]["musicInlineBadgeRenderer"][
                "icon"
            ]
            isExplicit = True
        except:
            isExplicit = False

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(videoUrl, download=False)

        return (
            jsonify(
                {
                    "Title": title,
                    "Artist": artist,
                    "Content-Type": type,
                    "Runtime": runtime,
                    "Cover Art": thumbnail,
                    "isExplicit": isExplicit,
                    "stream": info_dict["url"],
                }
            ),
            200,
        )

    except:
        return jsonify({"error": "Failed to fetch from youtube", "code": 403}), 403


@app.route("/search", methods=["GET"])
def search():
    query = request.args.get("q")
    query = query.replace("%20", " ")
    if not query:
        return (
            jsonify(
                {"error": "Missing 'q' parameter (song name) in query.", "code": 400}
            ),
            400,
        )

    return search_result(query)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=80)
