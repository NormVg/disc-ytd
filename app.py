from flask import Flask,send_file,request,jsonify

from pytube import YouTube
from moviepy.editor import *
import tempfile
import eyed3
import requests

from io import BytesIO
from PIL import Image



def get_audio_thumbnail(file):

    audio_file = eyed3.load(file)
    
    # Check if the audio file has an attached image
    if audio_file.tag and audio_file.tag.images:
        # Get the first image (thumbnail)
        image_data = audio_file.tag.images[0].image_data
        
        # Convert image data to PIL Image
        image = Image.open(BytesIO(image_data))
        art = tempfile.NamedTemporaryFile(suffix='.png', delete=False) 
        # Save the image (optional)
        image.save(art.name)
        
        return art.name
    
    else:
        print("No thumbnail found in the audio file.")
        return None

def download_mp3(url):
    mp4 =  tempfile.NamedTemporaryFile(suffix='.mp4', delete=False) 
    yt  = YouTube(url)
    file = yt.streams.get_lowest_resolution().download(filename=mp4.name)
    mp3 =  tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) 
    AudioFileClip(file).write_audiofile(mp3.name)
    audiofile = eyed3.load(mp3.name)
    audiofile.initTag(version=(2, 3, 0))
    imagedata = requests.get(yt.thumbnail_url).content
    audiofile.tag.images.set(3, imagedata, "image/jpeg", u"cover")
    audiofile.tag.save()
    return mp3.name

app = Flask(__name__)

@app.get("/")
def inedx():
    url = request.args.get("url")
    if url:
        file = download_mp3(url)
        return send_file(file)
    else : 
        return jsonify({"type":"url not found"})

@app.post("/img")
def get():
    file = tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) 
    a = request.files['file']
    a.save(file.name)
    img = get_audio_thumbnail(file.name)
    return send_file(img)
if __name__=="__main__":
    app.run(debug=True)
