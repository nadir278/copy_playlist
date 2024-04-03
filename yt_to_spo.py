import spotipy
from spotipy.oauth2 import SpotifyOAuth
from ytmusicapi import YTMusic

def convert(playlist_link):
    
    ytmusic = YTMusic("oauth.json")
    print('connected to youtube music')

    #cut the playlist id from the url
    playlist_id = playlist_link.split('list=')[-1]
    playlist = ytmusic.get_playlist(playlist_id)
    
    # token details
    SPOTIFY_CLIENT_ID = "39f42fa8c5bf4a69a270a038cafab9c4"
    SPOTIFY_SECRET = "74050c00f9534761a8bcfd53525d7227"
    redirect_uri = 'http://localhost:8888/callback'
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope="playlist-modify-private",
                                                   redirect_uri=redirect_uri,
                                                   client_id=SPOTIFY_CLIENT_ID,
                                                   client_secret=SPOTIFY_SECRET))
    print('connected to spotify')



    # create an array of the uri's of the song from the search result from spotify
    playlist_uris = []
    for i, item in enumerate(playlist['tracks']):
        result = sp.search(item['artists'][0]['name'] +" "+ item['title'], type='track', limit=1)
        playlist_uris.append(result['tracks']['items'][0]['uri'])
    



    #get the spotify user details
    user_details = sp.current_user()
    user_id = user_details['id']

    playlist_name = playlist['title']
    playlist_description = playlist['description']

    new = sp.user_playlist_create(user=f"{user_id}",
                                  name=playlist_name, 
                                  public=False, 
                                  description=playlist_description)
    playlist_id = new['id']

    spotipy_playlist = sp.user_playlist_add_tracks(user=f"{user_id}",
                                              playlist_id=playlist_id,
                                              tracks=playlist_uris)
    
    if spotipy_playlist:
        print('Playlist copied successfully')
        return "Playlist copied successfully"
    else:
        print('Failed to create YouTube Music playlist')
        return "Failed to create YouTube Music playlist"
    