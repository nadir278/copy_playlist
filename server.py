import spo_to_yt
from flask import Flask, request, render_template, redirect

app = Flask(__name__)

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
      return render_template('index.html')


@app.route('/spotify_to_youtube', methods=['POST'])
def spotify_to_youtube_post():
    playlist_link = request.form['playlist_link']
    return spo_to_yt.convert(playlist_link)



if __name__ == "__main__":
    app.run(debug=True)
