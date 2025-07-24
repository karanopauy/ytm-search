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
        "__Secure-1PAPISID": "6B4klqdk-uAkBeW5/AbjywAOSVB9zr4eY6",
        "__Secure-1PSID": "g.a000zQiPvnZ_AkfsufuNR0DOSpdeSkdvQq8E4sEQK5OAp0KASd4iGxVwO3DorpY8PtlHLBBK2AACgYKAXESARMSFQHGX2Mijt_orkZiPPs6-IjyA2qAChoVAUF8yKrH7oZRdzaoP9ALvHLn77VF0076",
        "__Secure-1PSIDCC": "AKEyXzU3SmwPxgmJi7LhDTeBafNmQ2j_n7Cc7_jwyUzRe-c3RqisVFhGqHDAQQgxdtyyvs24WA",
        "__Secure-1PSIDTS": "sidts-CjEB5H03P3s2Po2S-Ji-pQ6H9jBQVbdgrgSPPS7jO6IEg4cBDtu_2xs8yp1pHtUjKcmDEAA",
        "__Secure-3PAPISID": "6B4klqdk-uAkBeW5/AbjywAOSVB9zr4eY6",
        "__Secure-3PSID": "g.a000zQiPvnZ_AkfsufuNR0DOSpdeSkdvQq8E4sEQK5OAp0KASd4i4cQ_xhzG8rO3LlhAcMD6xQACgYKAS0SARMSFQHGX2MiW2UHi_PmcO5FilnZ8vUBQBoVAUF8yKoAS5qxUFvTX46V5fMzat3I0076",
        "__Secure-3PSIDCC": "AKEyXzWAvSEYw88O4WNEGxYgSXOnghBS0GK2jl54c_qXIim7Ufdf9CxnggQgh_A5fwrEjNiJDNI",
        "__Secure-3PSIDTS": "sidts-CjEB5H03P3s2Po2S-Ji-pQ6H9jBQVbdgrgSPPS7jO6IEg4cBDtu_2xs8yp1pHtUjKcmDEAA",
        "__Secure-ROLLOUT_TOKEN": "CNKN3vDUpKqXVRCa_byn-fCNAxiH5YCvztWOAw==",
        "APISID": "UutZ0NwEZ5IaBNiL/AqYnp9bst2d_W0cih",
        "HSID": "AZBT_xbUtY2otWrBi",
        "LOGIN_INFO": "AFmmF2swRQIhANMiljR-f47-jso4dG4NfXpADTv_vOo7zydiKdIlvFtJAiAJ6F3yzpsg5WR5jqXggZEXxz4kANEg4Vl7OQM_bG4daA:QUQ3MjNmeTIyNWt4QUdQWHZTM2JWQ1dnREZKUUtqWFRSVVhYNklwT3hETGNHQTlCRm9zWFdjbGNWRUZIdlM1YnJaZEhhR2lOQk5VN0Q5MHNpbW9ndmpXRVM2YkYzWU8xSGxvSmRzQUM0OHFUa2Vaek5vanZxXzNhZG9tVEhrcnlWUlQzQXFKUDk1U3JSWTdpaEc0X2JJSE1EaFRPSzBWQ3RB",
        "NID": "525=WUnsJ27owu7RtD19Fxn-62YMvguyQPrg2FZk5k6vtjYbSF_SE9YReFlzVaqVZYC4-LwevJeVteI_f9OkgPEGsv0Mp4AXQyMTLf2eNiL3U-qqfupWsvS-pfCf_Co6PMTEBleBsiF48nuct72JaTu16bVFt_Y8K079OGTgJgixgo_gEiuO6Pj_1v2hIsqAs_cbVDFdXPj2Sg2S2cFlktDWS869ELbhnIuendDePu5Q",
        "PREF": "repeat=NONE&f6=40000400&tz=Europe.Bucharest&f7=100&f5=20000&f4=4000000&autoplay=true",
        "s_gl": "NL",
        "SAPISID": "6B4klqdk-uAkBeW5/AbjywAOSVB9zr4eY6",
        "SID": "g.a000zQiPvnZ_AkfsufuNR0DOSpdeSkdvQq8E4sEQK5OAp0KASd4ijOIk-_vc2FX_ysBVHpnKdgACgYKAZwSARMSFQHGX2Miiu5guCT729BH7sJRAH-ENBoVAUF8yKocwMN5amDiM_TFN-Y3R-4Q0076",
        "SIDCC": "AKEyXzWybQxpsVJ7C4twRnbNCvb-bQlB7T50Scj6kBBcqB9XKK_oIzalSHFRvpCFKLLzTUJgIHM",
        "SOCS": "CAISNQgREitib3FfaWRlbnRpdHlmcm9udGVuZHVpc2VydmVyXzIwMjUwNjA5LjA1X3AwGgJlbiACGgYIgPeywgY",
        "SSID": "AuO9xq9hhEfpPFGuG",
        "VISITOR_INFO1_LIVE": "8_xMAfxKsco",
        "VISITOR_PRIVACY_METADATA": "CgJDWRIhEh0SGwsMDg8QERITFBUWFxgZGhscHR4fICEiIyQlJiAj",
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
                "gl": "NL",
                "remoteHost": "",
                "deviceMake": "",
                "deviceModel": "",
                "visitorData": "Cgs4X3hNQWZ4S3NjbyjS9YjEBjInCgJDWRIhEh0SGwsMDg8QERITFBUWFxgZGhscHR4fICEiIyQlJiAj",
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
                    "appInstallData": "CNL1iMQGELnZzhwQpcvPHBDyxM8cEL22rgUQu9nOHBCfoc8cELjkzhwQibDOHBDivs8cEOq7zxwQvoqwBRCQvM8cEPXEzxwQ0-GvBRDw4s4cEMn3rwUQiOOvBRCLgoATEJrKzxwQzN-uBRDYnM8cEJi5zxwQzMDPHBDGy88cEL2ZsAUQt-r-EhCHrM4cEJmNsQUQ9svPHBDOrM8cEIqXgBMQiIewBRDmyc8cEOGCgBMQ_LLOHBDFw88cEParsAUQr4bPHBCZmLEFEOHLzxwQ4crPHBCe0LAFEIHNzhwQlP6wBRDevM4cEJe1zxwQ8J3PHBDa984cEIKzzhwQ4riwBRCThs8cEO_EzxwQ9rrPHBCAl88cEJOszxwQ0qbPHCokQ0FNU0ZSVVdvTDJ3RE5Ia0J1SGRoUXJMM0E2dmlBWWRCdz09",
                    "coldConfigData": "CNL1iMQGGjJBT2pGb3gxN1pzYUxPelUyOGlVZEJsSWI5aVBVWVhVdzJwVGlVSmhhMm4yWnpYTVB4ZyIyQU9qRm94M0ptOG51VmZ2VFdWVzZHUmtHRlVNMFhwZkh2RmpJcTh2OEZvZzRxZDdvUkE%3D",
                    "coldHashData": "CNL1iMQGEhM4MzcyMjg4Nzg1MDY2MDg0NzkyGNL1iMQGMjJBT2pGb3gxN1pzYUxPelUyOGlVZEJsSWI5aVBVWVhVdzJwVGlVSmhhMm4yWnpYTVB4ZzoyQU9qRm94M0ptOG51VmZ2VFdWVzZHUmtHRlVNMFhwZkh2RmpJcTh2OEZvZzRxZDdvUkE%3D",
                    "hotHashData": "CNL1iMQGEhIzMDc5MDYxMzU2NTI0MTg3NjgY0vWIxAYyMkFPakZveDE3WnNhTE96VTI4aVVkQmxJYjlpUFVZWFV3MnBUaVVKaGEybjJaelhNUHhnOjJBT2pGb3gzSm04bnVWZnZUV1ZXNkdHUwWHBmSHZGaklxOHY4Rm9nNHFkN29SQQ%3D%3D",
                },
                "screenDensityFloat": 1.25,
                "userInterfaceTheme": "USER_INTERFACE_THEME_DARK",
                "timeZone": "Europe/Amsterdam",  # Note: This is a fixed string. You could make this dynamic too if needed, based on host system's timezone.
                "browserName": "Firefox",
                "browserVersion": "140.0",
                "acceptHeader": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "deviceExperimentId": "ChxOelV6TURZME5qSXdNVFExTkRZeE1qRTBNQT09ENL1iMQGGNL1iMQG",
                "rolloutToken": "CNKN3vDUpKqXVRCa_byn-fCNAxiH5YCvztWOAw%3D%3D",
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
                            "value": "EicKI1FQVi0zYWVvQWJwSU1DWkg1U1pad2Y0cldvT29pWGlfM3pUEAA=",
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
        "X-Goog-Visitor-Id": "Cgs4X3hNQWZ4S3NjbyjS9YjEBjInCgJDWRIhEh0SGwsMDg8QERITFBUWFxgZGhscHR4fICEiIyQlJiAj",
        "X-Youtube-Bootstrap-Logged-In": "true",
        "X-Youtube-Client-Name": "67",
        "X-Youtube-Client-Version": "1.20250716.03.00",
        "X-Goog-AuthUser": "1",
        "X-Origin": "https://music.youtube.com",
        "Origin": "https://music.youtube.com",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "same-origin",
        "Sec-Fetch-Site": "same-origin",
        "Authorization": "SAPISIDHASH 1753365257_656f0ab55014f3fc5a850c32f31c7d5c1b68746a_u SAPISID1PHASH 1753365257_656f0ab55014f3fc5a850c32f31c7d5c1b68746a_u SAPISID3PHASH 1753365257_656f0ab55014f3fc5a850c32f31c7d5c1b68746a_u",
        "Connection": "keep-alive",
        "Cookie": cookie_header_value,  # This is where the variable cookie value is used
        "Priority": "u=0",
        "TE": "trailers",
    }
    url = "https://music.youtube.com/youtubei/v1/search?prettyPrint=false"
    try:
        try:
            response = rq.post(url, headers=headers, json=payload, cookies=cookie).json()
        except:
            return jsonify({"Error" : "No Internet Access", "Code" : response.status_code}) , 404
        response = response["contents"]["tabbedSearchResultsRenderer"]["tabs"][0][
            "tabRenderer"
        ]["content"]["sectionListRenderer"]["contents"][1]["musicCardShelfRenderer"]
        if response["subtitle"]["runs"][0]["text"] != "Song":
            return jsonify({"Error": "Result yeilds no music", "code": 403}), 403
        thumbnail = (
            response["thumbnail"]["musicThumbnailRenderer"]["thumbnail"]["thumbnails"][
                1
            ]["url"]
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
                    "Runtime": runtime,
                    "Cover Art": thumbnail,
                    'isExplicit' : isExplicit,
                    "stream": info_dict["url"],
                }
            ),
            200,
        )

    except:
        return jsonify({"error": "Failed to fetch from youtube", "code": 403}), 403

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('q')
    if not query:
        return jsonify({"error": "Missing 'q' parameter (song name) in query.", "code" : 400}), 400
    
    return search_result(query)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=80)
