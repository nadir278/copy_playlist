import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from ytmusicapi import YTMusic
import os

def is_english(s):
        return all(ord(c) < 128 for c in s)

def convert(playlist_link):
    os.environ["SPOTIPY_CLIENT_ID"] = '39f42fa8c5bf4a69a270a038cafab9c4'
    os.environ["SPOTIPY_CLIENT_SECRET"] = '74050c00f9534761a8bcfd53525d7227'

    auth_manager = SpotifyClientCredentials()
    sp = spotipy.Spotify(auth_manager=auth_manager)
    print('connected to spotify')


    playlist = sp.playlist(playlist_link)
    tracks = sp.playlist_items(playlist_link)
    print('got playlist and songs from spotify')

    #create a list of the songs and their artist's
    artist_and_song = []
    for i, item in enumerate(tracks['items']):
        current_track = item['track']
        artist_and_song.append({'artist': current_track['artists'][0]['name'], 'song': current_track['name']})

    ytmusic = YTMusic("oauth.json")
    print('connected to youtube music')

    #create a list of the youtube music id's
    playlist_ytmusic_id = []
    for i in artist_and_song:
        # *error with limit returning 20 results when asked for 5*
        temp_song = ytmusic.search(f"{i['song']} {i['artist']}", filter='songs', limit=5)
        temp_vid = ytmusic.search(f"{i['song']} {i['artist']}", filter='videos', limit=5)
        
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

    ytmusic_playlist = ytmusic.create_playlist(playlist['name'],
                                               playlist['description'],
                                               video_ids=playlist_ytmusic_id)
    
    if ytmusic_playlist:
        print('Playlist copied successfully')
        return "Playlist copied successfully"
    else:
        print('Failed to create YouTube Music playlist')
        return "Failed to create YouTube Music playlist"
