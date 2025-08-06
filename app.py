import streamlit as st
import pandas as pd
import joblib
import requests

# Load data
movies = joblib.load('movies.pkl')
similarity = joblib.load('similarity.pkl')


API_KEY = '694b14c5d186529e5d415e1d73c56e16'  # ← Replace with your actual key
@st.cache_data
def fetch_poster(movie_title):
    url = f"https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&query={movie_title}"
    response = requests.get(url)
    data = response.json()
    
    if data['results']:
        poster_path = data['results'][0].get('poster_path')
        if poster_path:
            full_path = f"https://image.tmdb.org/t/p/w500{poster_path}"
            return full_path
    return "https://via.placeholder.com/200x300?text=No+Poster"

# Recommendation logic
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = list(enumerate(similarity[index]))
    movies_list = sorted(distances, key=lambda x: x[1], reverse=True)[1:6]
    recommended_movies = [movies.iloc[i[0]].title for i in movies_list]
    return recommended_movies

# Set page config
st.set_page_config(page_title="Movie Recommender", page_icon="🎬", layout="centered")

# Optional: Custom CSS for modern feel
st.markdown("""
    <style>
    .title {
        font-size: 36px;
        font-weight: bold;
        text-align: center;
        color: #FF4B4B;
        margin-bottom: 15px;
    }
    .recommendation-card {
        background-color: #f0f2f6;
        padding: 1rem;
        margin-bottom: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
   .stButton>button {
    background-color: #FF4B4B !important;
    color: white !important;
    font-weight: bold;
    border-radius: 12px;
    padding: 10px 12px;        /* ↑ Increased size */
    font-size: 24px !important;     border: none;
    transition: background-color 0.3s ease;
    cursor: pointer;
}

/* Hover state */
.stButton>button:hover {
    background-color: #e03e3e !important;
    color: white !important;
}

.recommendation-row {
    display: flex;
    flex-direction: row;
    gap: 20px;
    overflow-x: auto;
    padding: 20px 0;
    margin-bottom: 20px;
    width: 100%;
    box-sizing: border-box;
}

.poster-card {
    background-color: white;
    border-radius: 16px;
    padding: 12px;
    text-align: center;
    box-shadow: 0 8px 20px rgba(0, 0, 0, 0.2);
    border: 1px solid #e0e0e0;
    height: 330px;
    width: 180px;
    flex: 0 0 auto;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    position: relative;
    z-index: 1;
    margin-left: -20px; /* creates stacking overlap effect */
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}


.poster-card:hover {
    transform: translateY(-16px) scale(1.08);  /* more lift and zoom */
    z-index: 99;  /* bring it above all */
    box-shadow: 0 16px 32px rgba(0, 0, 0, 0.4);  /* strong shadow */
    border: 1px solid #aaa;
}


.poster-card img {
    border-radius: 8px;
    width: 100%;
    height: 240px;
    object-fit: cover;
}

.poster-title {
    font-weight: bold;
    font-size: 14px;
    color: #333;
    margin-top: 5px;
}div[data-baseweb="select"] {
    width: 500px !important;  /* You can adjust the width as needed */
}
div[data-baseweb="select"] {
    background-color: white !important;
    width: 900px !important;
    font-size: 18px !important;
    border-radius: 8px !important;
    padding: 10px !important;
    margin-top: -30px !important;  /* This line moves it up */
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

/* Text color inside dropdown */
div[data-baseweb="select"] * {
    color: black !important;
}
    </style>
""", unsafe_allow_html=True)

# App title
st.markdown('<div class="title">🎬 Movie Recommender</div>', unsafe_allow_html=True)

# Movie selection box
st.markdown("""
    <div style="color: white; font-size: 24px; font-weight: bold; margin-bottom: 10px;">
        🎥 Choose a movie you like:
    </div>
""", unsafe_allow_html=True)

selected_movie = st.selectbox(
    "",  # Empty label since we styled it manually
    movies['title'].values
)

import base64

def set_bg_from_local(image_path):
    with open(image_path, "rb") as img_file:
        encoded = base64.b64encode(img_file.read()).decode()
    st.markdown(f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpeg;base64,{encoded}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}
        </style>
    """, unsafe_allow_html=True)

set_bg_from_local("bg.jpg")

if st.button("🔍 Recommend Similar Movies"):
    recommendations = recommend(selected_movie)

    st.markdown('<h3 style="color: white; font-weight: bold;">📽️ Top 5 Recommendations</h3>', unsafe_allow_html=True)

    # Start horizontal scrollable row
    # Start collecting all cards as a single HTML string
    spaced_cols = st.columns([4, 4, 40, 4, 40, 4, 40, 0.4, 40, 0.4, 4])
 
    for i, movie in enumerate(recommendations):
        poster_url = fetch_poster(movie)
        with spaced_cols[i * 2+1]:  # 0, 2, 4, 6, 8 (skip spaces)
            st.markdown(f"""
                <div class="poster-card">
                    <img src="{poster_url}" alt="{movie} poster">
                    <div class="poster-title">{movie}</div>
                </div>
            """, unsafe_allow_html=True)
