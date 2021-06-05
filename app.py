from flask import Flask, render_template, request, redirect, url_for
from pytube import YouTube
from pytube import Playlist
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('base.html')

@app.route('/getSongs', methods = ["POST"])
def getSongs():
    songurl = request.form.get("Song URL")
    playurl = request.form.get("Song Playlist URL")
    SAVE_PATH = request.form.get("SavePath")
    inputtype = request.form.get("type")
    print(songurl)

    if inputtype == "A Song":
        yt = YouTube(songurl)

        audiofiles = yt.streams.filter(only_audio=True).first() 
        out_file =audiofiles.download(SAVE_PATH)
        base, ext = os.path.splitext(out_file)
        new_file = base + '.mp3'
        os.rename(out_file, new_file)
        print('Task Completed!')

    elif inputtype == "A Playlist":
        p = Playlist(playurl)
        for video in p.videos:
            # getting videos from the playlist and saving them as mp4 files
            audiofiles = video.streams.filter(only_audio=True).first()
            out_file = audiofiles.download(SAVE_PATH)
            
            # changing extensions from mp4 to mp3
            base, ext = os.path.splitext(out_file)
            new_file = base + '.mp3'
            os.rename(out_file, new_file)
            print(base, " Completed!")
    
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug = True)