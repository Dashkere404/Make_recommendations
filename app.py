import streamlit as st
import pandas as pd

# --------------------
# Настройки страницы
# --------------------
st.set_page_config(
    page_title="Music App",
    page_icon="🎵",
    layout="centered"
)

st.markdown(
    """
    <style>
    div.block-container {
        padding-top: 1rem;
        padding-bottom: 0rem;
    }

    div[data-testid="stVerticalBlock"] {
        gap: 0.25rem;
    }

    div[data-baseweb="input"] {
        position: relative;
    }

    div[data-baseweb="input"]::after {
        content: "🔍";
        position: absolute;
        right: 12px;
        top: 50%;
        transform: translateY(-50%);
        pointer-events: none;
    }

    header[data-testid="stHeader"] {
        background: rgba(0,0,0,0);
    }

    html, body {
        height: 100%;
    }

    div[data-testid="stAppViewContainer"] {
        min-height: 100vh;
        padding-bottom: 6rem;
    }

    footer {
        visibility: hidden;
    }
    </style>
    """,
    unsafe_allow_html=True
)
# --------------------
# Фейковые треки
# --------------------
fake_tracks = [
    {
        "track_id": 1,
        "title": "Midnight City",
        "artist": "M83"
    },
    {
        "track_id": 2,
        "title": "Blinding Lights",
        "artist": "The Weeknd"
    },
    {
        "track_id": 3,
        "title": "After Dark",
        "artist": "Mr.Kitty"
    },
    {
        "track_id": 4,
        "title": "Sweater Weather",
        "artist": "The Neighbourhood"
    },
    {
        "track_id": 5,
        "title": "505",
        "artist": "Arctic Monkeys"
    },
    {
        "track_id": 6,
        "title": "Little Dark Age",
        "artist": "MGMT"
    },
    {
        "track_id": 7,
        "title": "Starboy",
        "artist": "The Weeknd"
    },
    {
        "track_id": 8,
        "title": "Borderline",
        "artist": "Tame Impala"
    }
]

df = pd.DataFrame(fake_tracks)

# --------------------
# Session State
# --------------------
if "favorites" not in st.session_state:
    st.session_state.favorites = []

if "page" not in st.session_state:
    st.session_state.page = "home"

if "selected_track" not in st.session_state:
    st.session_state.selected_track = None

if "previous_page" not in st.session_state:
    st.session_state.previous_page = "home"

# --------------------
# Поиск
# --------------------
def search_tracks(query, data):

    if not query:
        return data

    query = query.lower()

    return data[
        data["title"].str.lower().str.contains(query) |
        data["artist"].str.lower().str.contains(query)
    ]

# --------------------
# Карточка трека
# --------------------
def track_card(track):

    st.markdown(
        """
        <style>
        /* убираем лишние отступы сверху/снизу страницы */
        div.block-container {
            padding-top: 1rem;
            padding-bottom: 0rem;
        }

        /* уменьшаем расстояние между карточками */
        div[data-testid="stVerticalBlock"] {
            gap: 0.25rem;
        }

        /* 🔍 иконка справа в поиске */
        div[data-baseweb="input"] {
            position: relative;
        }

        div[data-baseweb="input"]::after {
            content: "🔍";
            position: absolute;
            right: 12px;
            top: 50%;
            transform: translateY(-50%);
            pointer-events: none;
        }
        
        header[data-testid="stHeader"] {
            background: rgba(0,0,0,0);
        }

        </style>
        """,
        unsafe_allow_html=True
    )

    with st.container():

        col1, col2 = st.columns([10, 1])

        with col1:
            st.markdown('<div class="track-btn">', unsafe_allow_html=True)

            if st.button(
                f"🎵 {track['title']}  —  {track['artist']}",
                key=f"track_{track['track_id']}",
                use_container_width=True
            ):
                st.session_state.previous_page = st.session_state.page
                st.session_state.selected_track = track
                st.session_state.page = "similar"
                st.rerun()

            st.markdown('</div>', unsafe_allow_html=True)

        with col2:
            st.markdown('<div class="fav-btn">', unsafe_allow_html=True)

            is_favorite = track["track_id"] in st.session_state.favorites
            heart = "❤️" if is_favorite else "🤍"

            if st.button(
                heart,
                key=f"fav_{track['track_id']}",
                use_container_width=True
            ):
                if is_favorite:
                    st.session_state.favorites.remove(track["track_id"])
                else:
                    st.session_state.favorites.append(track["track_id"])

                st.rerun()

            st.markdown('</div>', unsafe_allow_html=True)

# --------------------
# Главная
# --------------------
def home_page():

    st.title("🎵 Музыка")

    query = st.text_input(
        "",
        placeholder="Поиск треков"
    )

    filtered = search_tracks(query, df)

    # Рекомендации
    if len(st.session_state.favorites) > 0:

        st.markdown("###")

        st.markdown(
            """
            <style>
            .rec-btn button {
                height: 120px;          /* 👈 делаем выше */
                font-size: 28px;        /* 👈 крупный текст */
                font-weight: 700;       /* жирный */
                border-radius: 18px;    /* более "карточный" вид */
            }
            </style>
            """,
            unsafe_allow_html=True
        )

        with st.container():
            st.markdown('<div class="rec-btn">', unsafe_allow_html=True)

            if st.button(
                "🎧 Музыка для вас",
                use_container_width=True,
                key="recommend_btn"
            ):
                st.session_state.page = "recommendations"
                st.rerun()

            st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("## Треки")

    for _, track in filtered.iterrows():
        track_card(track)
# --------------------
# Избранное
# --------------------
def favorites_page():

    st.title("❤️ Избранное")

    query = st.text_input(
        "",
        placeholder="🔍 Поиск"
    )

    fav_df = df[
        df["track_id"].isin(
            st.session_state.favorites
        )
    ]

    filtered = search_tracks(query, fav_df)

    if len(filtered) == 0:
        st.info("Нет сохранённых треков")

    for _, track in filtered.iterrows():
        track_card(track)

# --------------------
# Рекомендации
# --------------------
def recommendations_page():

    st.title("🎧 Рекомендации")

    if st.button("⬅ Назад"):

        st.session_state.page = "home"
        st.rerun()

    st.write("На основе ваших предпочтений")

    # Временно случайные треки
    recs = df.sample(
        min(5, len(df))
    )

    for _, track in recs.iterrows():
        track_card(track)

# --------------------
# Похожие треки
# --------------------
def similar_page():

    track = st.session_state.selected_track

    st.title("🎵 Похожие треки")

    col1, col2 = st.columns([5,1])

    with col1:

        if st.button("⬅ Назад"):

            st.session_state.page = (
                st.session_state.previous_page
            )

            st.rerun()

    st.markdown("###")

    st.info(
        f"Похожие на:\n\n"
        f"{track['title']} — {track['artist']}"
    )

    # Временно случайные треки
    similar_tracks = df.sample(
        min(5, len(df))
    )

    for _, t in similar_tracks.iterrows():
        track_card(t)

# --------------------
# Роутинг
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
# Нижняя навигация
# --------------------
st.markdown("---")

nav1, nav2 = st.columns(2)

with nav1:

    if st.button(
        "🏠",
        use_container_width=True
    ):

        st.session_state.page = "home"
        st.rerun()

with nav2:

    if st.button(
        "❤️",
        use_container_width=True
    ):

        st.session_state.page = "favorites"
        st.rerun()