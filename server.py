import spo_to_yt
import time
from flask import Flask, request, render_template, redirect

app = Flask(__name__)

msg = ''

@app.route('/')
def choose():
    return render_template('choose.html')

@app.route('/choose_input_output', methods=['POST'])
def choose_input_output():
    in_platform = request.form.get('copy_from')
    out_platform = request.form.get('copy_to')
    if in_platform == 'Spotify':
        return redirect('/spotify_to_youtube')
        


@app.route('/spotify_to_youtube')
def spotify_to_youtube_get():
      return render_template('get_spotify_playlist.html')


@app.route('/spotify_to_youtube', methods=['POST'])
def spotify_to_youtube_post():
    global msg
    playlist_link = request.form['playlist_link']
    msg = spo_to_yt.convert(playlist_link)
    return redirect('/done')

@app.route('/done')
def done():
    return render_template('done.html', string=msg)

@app.route('/done', methods=['POST'])
def show_msg():
    return redirect('/')


if __name__ == "__main__":
    app.run(debug=True)
