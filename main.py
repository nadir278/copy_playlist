import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from ytmusicapi import YTMusic
import os
from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():

    def is_english(s):
        return all(ord(c) < 128 for c in s)


    # spotify user id
    username = '110cxnzqiawttmjdidq0y2drm?si=9940ed5e69fd475c'

    # token details
    redirect_uri = 'http://localhost:8888/callback'
    scope = "user-library-read"
    os.environ["SPOTIPY_CLIENT_ID"] = '39f42fa8c5bf4a69a270a038cafab9c4'
    os.environ["SPOTIPY_CLIENT_SECRET"] = '74050c00f9534761a8bcfd53525d7227'

    auth_manager = SpotifyClientCredentials()
    sp = spotipy.Spotify(auth_manager=auth_manager)

    playlist_link = input("please enter a playlist's url: ")
    playlist = sp.playlist(playlist_link)
    tracks = sp.playlist_items(playlist_link)

    #create a list of the songs and their artist's
    artist_and_song = []
    for i, item in enumerate(tracks['items']):
        current_track = item['track']
        print(current_track['name'])
        artist_and_song.append({'artist': current_track['artists'][0]['name'], 'song': current_track['name']})

    ytmusic = YTMusic("oauth.json")

    #create a list of the youtube music id's
    playlist_ytmusic_id = []
    for i in artist_and_song:
        temp_song = ytmusic.search(f"{i['song']} {i['artist']}", filter='songs', limit=5)
        temp_vid = ytmusic.search(f"{i['song']} {i['artist']}", filter='songs', limit=5)
        
        #if the song is insn't in english add the first result
        if is_english(i['song']):
            #check which song from the top 5 results is the right song by
            #checking if the first substring to the space of the rsult is in the name of the wanted song
            compare_str = i['song'].lower()
            for j in range(5):
                song_compare_substr = temp_song[j]['title'].split()[0].lower()
                vid_compare_substr = temp_vid[j]['title'].split()[0].lower()
                # because of some tracks only having a video version and some only have a song version
                # add the song or video with priority to the song version 
                if song_compare_substr in compare_str:
                    playlist_ytmusic_id.append(temp_song[j]['videoId'])
                    break
                elif vid_compare_substr in compare_str: 
                    playlist_ytmusic_id.append(temp_vid[j]['videoId'])
                    break
                if j==5:
                    print('couldnt find song "' + i['song'] + '" by "' + i['artist'] + '"')
        else:
            playlist_ytmusic_id.append(temp_song[0]['videoId'])

    ytmusic_playlist = ytmusic.create_playlist(playlist['name'], playlist['description'], video_ids=playlist_ytmusic_id)
    print('playlist copied successfully')

if __name__ == "__main__":
    app.run(debug=True)
