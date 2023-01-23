
from flask import Flask, jsonify, render_template
import requests
import secrets

def jsongen(url):
    import requests
    import json
    headers = {"X-Signature-Version": "web2","X-Signature": secrets.token_hex(32)}
    res = requests.get(url, headers=headers)
    y = json.loads(res.text)
    return y


def gettrending(time,page):
    jsondata  = []
    page = page
    trending_url = "https://hanime.tv/api/v8/browse-trending?time={time}&page={page}".format(time=time,page=str(page))
    url = trending_url
    urldata = jsongen(url)
    for x in urldata["hentai_videos"]:
        json_data = {'id': x['id'] , 'name' : x['name'], 'cover_url': x['cover_url'], 'views' : x['views'], 'link': '/api/video/{id}'.format(id=str(x['id']))}
        jsondata.append(json_data)
    return jsondata

def getvideo(id):
    jsondata = []
    video_api_url = "https://hanime.tv/api/v8/video?id="
    video_data_url = video_api_url + str(id)
    video_data = jsongen(video_data_url)
    streams = []
    for s in video_data['videos_manifest']['servers'][0]['streams']:
        stream_data = {'width' : s['width'],'height' : s['height'],'size_mbs' : s['filesize_mbs'],'url' : s['url']}
        streams.append(stream_data)
    json_data = {'id': video_data["hentai_video"]['id'] , 'name' : video_data["hentai_video"]['name'],'description': video_data["hentai_video"]['description'], 'poster_url': video_data["hentai_video"]['poster_url'],'cover_url': video_data["hentai_video"]['cover_url'], 'views' : video_data["hentai_video"]['views'], 'streams': streams}
    jsondata.append(json_data)
    return jsondata

app = Flask(__name__)
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/trending/<time>/<page>', methods = ["GET"])
def trending_page(time,page):
    videos = gettrending(time,page)
    next_page = '/trending/{time}/{page}'.format(time=time,page=str(int(page)+1))
    return render_template('trending.html',videos=videos, next_page = next_page, time=time)

@app.route('/video/<id>', methods = ["GET"])
def video_page(id):
    video = getvideo(id)[0]
    return render_template('video.html',video=video)

@app.route('/api/video/<id>', methods = ["GET"])
def video_api(id):
    jsondata = getvideo(id)
    return jsonify({'results': jsondata}),200

@app.route('/api/trending/<time>/<page>', methods=["GET"])
def trending_api(time, page):
    jsondata = gettrending(time,page)
    return jsonify({'results': jsondata, 'next_page': '/api/trending/{time}/{page}'.format(time=time,page=str(int(page)+1))}),200