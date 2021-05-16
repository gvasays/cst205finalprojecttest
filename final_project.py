from flask import Flask, render_template, redirect,request,
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, 
from wtforms.validators import DataRequired
from datetime import datetime
import requests,json
import speech_recognition as sr

app = Flask(__name__)
app.config['SECRET_KEY'] = 'csumb-otter'
bootstrap = Bootstrap(app)

class Playlist(FlaskForm):
    song_title = StringField('Song Title', validators=[DataRequired()])
    artist_name = StringField('Artist name', validators = [DataRequired()])
    

playlist = []

def store_song(my_song,my_artist):
    playlist.append(dict(
        song = my_song,
        artist = my_artist,
        date = datetime.today()
    ))

@app.route('/', methods=('GET', 'POST'))
def index():
    form = Playlist()
    if form.validate_on_submit():
        store_song(form.song_title.data,form.artist_name.data)
        print(playlist)
        return redirect('/view_playlist')
    return render_template('index.html', form=form)

@app.route('/view_playlist')
def vp():
    return render_template('vp.html', playlist=playlist)


@app.route('/artist_playlist')
def vip():
    return render_template('artist_playlist.html', playlist=playlist)


# voice assist for the playlist
@app.route("/voice", methods=["GET", "POST"])
def index1():
    transcript = ""
    if request.method == "POST":
        print("FORM DATA RECEIVED")

        if "file" not in request.files:
            return redirect(request.url)

        file = request.files["file"]
        if file.filename == "":
            return redirect(request.url)

        if file:
            recognizer = sr.Recognizer()
            audioFile = sr.AudioFile(file)
            with audioFile as source:
                data = recognizer.record(source)
            transcript = recognizer.recognize_google(data, key=None)

    return render_template('index1.html', transcript=transcript)

if __name__ == "__main__":
    app.run(debug=True, threaded=True)

# api information for the search bar

@app.route('/api_display', methods=['GET'])
def api():
    # response = requests.request("GET", url, headers=headers)
    req = requests.get('https://api.deezer.com/user/2529/playlists')
    data = json.loads(req.content)
    # print(response.text)
    return render_template('api_display.html', data=data['data'])





