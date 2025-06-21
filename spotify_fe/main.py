import streamlit as st
import requests


query = st.query_params
playlist_id = query.get('playlist_id', None)

response = requests.get(f"http://127.0.0.1:8000/playlist/{playlist_id}")


if playlist_id:
    if st.button('go back'):
        st.query_params.clear()
        st.rerun()




    response = requests.get(f"http://127.0.0.1:8000/playlist/{playlist_id}")
    if response.status_code != 200:
        st.error('Unable to fetch playlist')
    else:
        playlist = response.json()
        for song in playlist:
            col1, col2 = st.columns([2, 3])
            with col1:
                if song["album_image"]:
                    st.image(song["album_image"], width=120)
                else:
                    st.write("No Image")
            with col2:
                st.subheader(song['track'])
                st.write(song[ "artist"])



else:
    response = requests.get("http://127.0.0.1:8000/playlists")

    if response.status_code != 200:
        st.error("Failed to fetch playlists.")
    else:
        playlists = response.json()

        st.title("🎧 Your Spotify Playlists")

    # --- Loop through and show each playlist ---
        for playlist in playlists:
            col1, col2 = st.columns([2, 3])
            with col1:
                if playlist["image"]:
                    st.image(playlist["image"], width=120)
                else:
                    st.write("No Image")

            with col2:
                playlist_link = f"?playlist_id={playlist['id']}"
                st.markdown(
                f'<a href="{playlist_link}" style="text-decoration:none;">'
                f'<h4 style="color:#1DB954;">{playlist["name"]}</h4></a>',
                unsafe_allow_html=True
        )

            st.markdown("---")
