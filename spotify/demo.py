from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from tekore import Spotify,RefreshingCredentials,Scope
import os

app=FastAPI()
client_id = '9bf2f5538fe949228ab5cdccc03e7338'
client_secret = '5aaf3b9973b4449785e920b900a83b5e'
redirect_uri = 'http://127.0.0.1:8000/callback'


rcred = RefreshingCredentials(client_id,client_secret,redirect_uri)
def get_spotify():
    if not os.path.exists('refresh_token.txt'):
        raise Exception ('please login first')
    else:
        with open('refresh_token.txt','r') as f:
            refresh_token=f.read().strip()
    token = rcred.refresh_user_token(refresh_token)
    return Spotify(token)

@app.get('/login')
def auth():
    url=rcred.user_authorisation_url(Scope.every)
    return RedirectResponse(url)

@app.get('callback')
def handle(code:str):
    token=rcred.request_user_token(code)
     
    with open('refresh_token.txt','w') as f:
        f.write(token.refresh_token)




    return {"message": "Login successful", "refresh_token": token.refresh_token}

@app.get('/playlists')
def get_playlit():
    spotify = get_spotify()
    result=[]
    playlist = spotify.current_user_top_tracks(time_range='medium_term')
    for p in playlist:
        return p


