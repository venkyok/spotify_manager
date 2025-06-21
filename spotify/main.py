from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from tekore import Spotify, scope, RefreshingCredentials
import os

# Setup
client_id = '9bf2f5538fe949228ab5cdccc03e7338'
client_secret = '5aaf3b9973b4449785e920b900a83b5e'
redirect_uri = 'http://127.0.0.1:8000/callback'

TOKEN_FILE = "refresh_token.txt"
rcred = RefreshingCredentials(client_id, client_secret, redirect_uri)


app = FastAPI()


def get_spotify():
    if not os.path.exists(TOKEN_FILE):
        raise Exception("Please login first at /login")
    
    with open(TOKEN_FILE, "r") as f:
        refresh_token = f.read().strip()
    
    token = rcred.refresh_user_token(refresh_token)
    return Spotify(token)

@app.get("/login")
def login():
    auth_url = rcred.user_authorisation_url(scope.every)
    return RedirectResponse(auth_url)



@app.get("/callback")
def callback(code: str):
    token = rcred.request_user_token(code)
    
    # Save refresh token
    with open(TOKEN_FILE, "w") as f:
        f.write(token.refresh_token)
    
    return {"message": "Login successful", "refresh_token": token.refresh_token}



@app.get("/profile")
def get_profile():
    try:
        spotify = get_spotify()
        user = spotify.current_user()
        return {"name": user.display_name, "email": user.email}
    except Exception as e:
        return {"error": str(e)}




@app.get("/playlists")
def get_playlists():
    result=[]
    try:
        spotify = get_spotify()
        user_id = spotify.current_user().id
        playlists = spotify.playlists(user_id)
        for p in playlists.items:
            if p is None:
                result.append({"name": "Unknown", "image": None})
            else:
                result.append({
                    "name": p.name,
                    "image": p.images[0].url if p.images else None,
                    'id':p.id

                })

        return result

    except Exception as e:
        return {"error": str(e)}



@app.get("/playlist/{id}")
def get_playlis(id:str):
    playlist_id = id
    spotify = get_spotify()
    playlist = spotify.playlist(playlist_id)
    tracks = playlist.tracks.items

    result = []
    for t in tracks:
        result.append({
            "track": t.track.name,
            "artist": t.track.artists[0].name,
            "album_image": t.track.album.images[0].url if t.track.album.images else None
        })

    return result



@app.get('/track')
def get_playlist():
    spotify = get_spotify()
    result=[]
    track = spotify.current_user_top_tracks(time_range='medium_term')
    for t in track.items:
         result.append({
            "track": t.name,
            "artist": t.artists[0].name,
            "album_image": t.album.images[0].url if t.album.images else None
        })
    return result
