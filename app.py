import streamlit as st
import pandas as pd

from recommendations import (
    config,
    ae_embeddings_np,
    siam_embeddings_np,
    id_to_pos,
    pos_to_id,
    user_recommendation,
    track_recommendation
)

# --------------------
# PAGE CONFIG
# --------------------
st.set_page_config(
    page_title="Music App",
    page_icon="🎵",
    layout="centered"
)

st.markdown("""
<style>
div.block-container {
    padding-top: 1rem;
    padding-bottom: 6rem;
}

div[data-testid="stVerticalBlock"] {
    gap: 0.25rem;
}

header[data-testid="stHeader"] {
    background: rgba(0,0,0,0);
}

footer {
    visibility: hidden;
}

.rec-btn button {
    height: 120px;
    font-size: 28px;
    font-weight: 800;
    border-radius: 18px;
}
</style>
""", unsafe_allow_html=True)

# --------------------
# LOAD DATA
# --------------------
df = pd.read_csv("data_for_recommendations/tracks.csv")

# --------------------
# CLEAN DATA (ВАЖНО)
# --------------------
def is_bad_track(row):
    title = str(row["track_title"]).lower()
    artist = str(row["artist_name"]).lower()

    if "track" in title and "area" in artist:
        return True
    if "area c" in title:
        return True
    if title.startswith("track ") and title.split(" ")[1].isdigit():
        return True
    if len(title) < 2 or len(artist) < 2:
        return True

    return False

df = df[~df.apply(is_bad_track, axis=1)].reset_index(drop=True)

# --------------------
# SESSION STATE
# --------------------
if "favorites" not in st.session_state:
    st.session_state.favorites = []

if "page" not in st.session_state:
    st.session_state.page = "home"

if "selected_track" not in st.session_state:
    st.session_state.selected_track = None

if "visible_count" not in st.session_state:
    st.session_state.visible_count = 50

# --------------------
# SEARCH (по всей базе)
# --------------------
def search_tracks(query):
    if not query:
        return df

    q = query.lower()
    return df[
        df["track_title"].str.lower().str.contains(q) |
        df["artist_name"].str.lower().str.contains(q)
    ]

# --------------------
# TRACK CARD
# --------------------
def track_card(track):

    col1, col2 = st.columns([10, 1])

    with col1:
        if st.button(
            f"🎵 {track['track_title']} — {track['artist_name']}",
            key=f"t_{track['track_id']}",
            use_container_width=True
        ):
            st.session_state.selected_track = track["track_id"]
            st.session_state.page = "similar"
            st.rerun()

    with col2:
        is_fav = track["track_id"] in st.session_state.favorites
        heart = "❤️" if is_fav else "🤍"

        if st.button(heart, key=f"f_{track['track_id']}"):
            if is_fav:
                st.session_state.favorites.remove(track["track_id"])
            else:
                st.session_state.favorites.append(track["track_id"])
            st.rerun()

# --------------------
# HOME
# --------------------
def home_page():

    st.title("🎵 Музыка")

    query = st.text_input("", placeholder="Поиск треков")

    filtered = search_tracks(query)

    visible = st.session_state.visible_count
    display_df = filtered.head(visible)

    # кнопка рекомендаций
    if len(st.session_state.favorites) > 0:

        st.markdown("###")

        if st.button("🎧 Музыка для вас", use_container_width=True):
            st.session_state.page = "recommendations"
            st.rerun()

    st.markdown("## Треки")

    for _, track in display_df.iterrows():
        track_card(track)

    # LOAD MORE
    if visible < len(filtered):
        if st.button("⬇ Загрузить ещё 25", use_container_width=True):
            st.session_state.visible_count += 25
            st.rerun()

# --------------------
# FAVORITES
# --------------------
def favorites_page():

    st.title("❤️ Избранное")

    fav_df = df[df["track_id"].isin(st.session_state.favorites)]

    if len(fav_df) == 0:
        st.info("Нет сохранённых треков")

    for _, track in fav_df.iterrows():
        track_card(track)

# --------------------
# RECOMMENDATIONS
# --------------------
def recommendations_page():

    st.title("🎧 Рекомендации")

    if st.button("⬅ Назад"):
        st.session_state.page = "home"
        st.rerun()

    rec_ids = user_recommendation(
        st.session_state.favorites,
        config,
        ae_embeddings_np,
        id_to_pos,
        pos_to_id
    )

    rec_df = df[df["track_id"].isin(rec_ids)]

    if len(rec_df) == 0:
        st.info("Добавь лайки ❤️ для рекомендаций")

    for _, track in rec_df.iterrows():
        track_card(track)

# --------------------
# SIMILAR TRACKS
# --------------------
def similar_page():

    track_id = st.session_state.selected_track

    st.title("🎵 Похожие треки")

    if st.button("⬅ Назад"):
        st.session_state.page = "home"
        st.rerun()

    rec_ids = track_recommendation(
        track_id,
        config,
        siam_embeddings_np,
        id_to_pos,
        pos_to_id
    )

    rec_df = df[df["track_id"].isin(rec_ids)]

    selected = df[df["track_id"] == track_id]
    if not selected.empty:
        st.info(
            f"Выбран трек: {selected.iloc[0]['track_title']} — {selected.iloc[0]['artist_name']}"
        )

    for _, track in rec_df.iterrows():
        track_card(track)

# --------------------
# ROUTER
# --------------------
if st.session_state.page == "home":
    home_page()
elif st.session_state.page == "favorites":
    favorites_page()
elif st.session_state.page == "recommendations":
    recommendations_page()
elif st.session_state.page == "similar":
    similar_page()

# --------------------
# BOTTOM NAV
# --------------------
st.markdown("---")

c1, c2 = st.columns(2)

with c1:
    if st.button("🏠", use_container_width=True):
        st.session_state.page = "home"
        st.rerun()

with c2:
    if st.button("❤️", use_container_width=True):
        st.session_state.page = "favorites"
        st.rerun()