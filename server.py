import spo_to_yt
import yt_to_spo
from flask import Flask, request, render_template, redirect

app = Flask(__name__)

msg = ''

@app.route('/')
def choose():
    return render_template('choose.html')

#handle choosing platforms page
@app.route('/choose_input_output', methods=['POST'])
def choose_input_output():
    in_platform = request.form.get('copy_from')
    out_platform = request.form.get('copy_to')
    if in_platform == 'Spotify' and out_platform == 'YouTube_Music':
        return redirect('/spotify_to_youtube')
    elif in_platform == 'YouTube_Music' and out_platform == 'Spotify':
        return redirect('/youtube_to_spotify')

        
#handle convert from Spotify to YTmusic
@app.route('/spotify_to_youtube')
def spotify_to_youtube_get():
      return render_template('get_spotify_playlist.html')

@app.route('/spotify_to_youtube', methods=['POST'])
def spotify_to_youtube_post():
    global msg
    playlist_link = request.form['playlist_link']
    msg = spo_to_yt.convert(playlist_link)
    return redirect('/done')


#handle convert from YTmusic to Spotify
@app.route('/youtube_to_spotify')
def youtube_to_spotify_get():
      return render_template('get_youtube_playlist.html')

@app.route('/youtube_to_spotify', methods=['POST'])
def youtube_to_spotify_post():
    global msg
    playlist_link = request.form['playlist_link']
    msg = yt_to_spo.convert(playlist_link)
    return redirect('/done')

#handle when a convert is done
@app.route('/done')
def done():
    return render_template('done.html', string=msg)

@app.route('/done', methods=['POST'])
def show_msg():
    return redirect('/')


if __name__ == "__main__":
    app.run(debug=False)
