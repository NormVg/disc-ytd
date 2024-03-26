from flask import Flask, request, render_template, send_file
from pytube import YouTube
from pydub import AudioSegment
import tempfile
import os

app = Flask(__name__)

@app.route('/')
def index():
    files = os.listdir(tempfile.gettempdir())
    mp3_files = [f for f in files if f.endswith('.mp3')]
    return render_template('index.html', mp3_files=mp3_files)

@app.route('/download', methods=['POST'])
def download():
    url = request.form['url']
    
    yt = YouTube(url)
    video = yt.streams.filter(only_audio=True).first()
    
    if video:
        audio_stream = video.download(output_path=tempfile.gettempdir())
        
        # Convert to MP3 using pydub
        audio_path = audio_stream[:-4] + '.mp3'
        AudioSegment.from_file(audio_stream).export(audio_path, format='mp3')
        
        os.remove(audio_stream)  # Remove original audio file
        
        return audio_path.split('/')[-1]
    
    return 'Error downloading the video'

@app.route('/play/<path:file_name>')
def play(file_name):
    return send_file(os.path.join(tempfile.gettempdir(), file_name), as_attachment=True, mimetype='audio/mp3')

if __name__ == '__main__':
    app.run(debug=True)
