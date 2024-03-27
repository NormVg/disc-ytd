from flask import Flask,send_file,request,jsonify

from pytube import YouTube
from moviepy.editor import *
import tempfile

def download_mp3(url):
    mp4 =  tempfile.NamedTemporaryFile(suffix='.mp4', delete=False) 
    yt  = YouTube(url)
    print("downloading")
    file = yt.streams.get_audio_only().download(filename=mp4.name)
    print("downloaded")
    mp3 =  tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) 
    AudioFileClip(file).write_audiofile(mp3.name)
    return mp3.name

app = Flask(__name__)

@app.get("/")
def inedx():
    url = request.args.get("url")
    if url:
        file = download_mp3(url)
        return send_file(file)
    else : 
        return jsonify("type":"url not found")

if __name__=="__main__":
    app.run(debug=True)
