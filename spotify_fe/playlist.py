import streamlit as st
import requests


















# --- Call your FastAPI server ---
response = requests.get("http://127.0.0.1:8000/playlist")

if response.status_code != 200:
    st.error("Failed to fetch playlists.")
else:
    playlist = response.json()

    st.title("🎧 Your Spotify Playlists")

    # --- Loop through and show each playlist ---
    for song in playlist:
        col1, col2 = st.columns([2, 3])
        with col1:
            if song["album_image"]:
                st.image(song["album_image"], width=120)
            else:
                st.write("No Image")

        with col2:
            st.subheader(song["track"])
            st.subheader(song["artist"])
        st.markdown("---")
