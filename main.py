from spotipy import SpotifyOAuth
from ytmusicapi import YTMusic
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os
import spotipy.util as util
from flask import Flask, request, render_template


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
print("playlist's name: " + playlist['name'])
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
    temp_song = ytmusic.search(f"{i['song']} {i['artist']}", filter='songs')
    temp_vid = ytmusic.search(f"{i['song']} {i['artist']}", filter='songs')
    
    compare_name = i['song'].lower()
    print(compare_name)
    #ffff

    print(temp_song[0]['title'])
    playlist_ytmusic_id.append(temp_song[0]['videoId'])

ytmusic_playlist = ytmusic.create_playlist(playlist['name'], playlist['description'], video_ids=playlist_ytmusic_id)
print('playlist copied successfully')
