import streamlit as st
import pandas as pd
import joblib
import requests
import base64

movies = joblib.load('movies.pkl')
similarity = joblib.load('similarity.pkl')
OMDB_API_KEY = '' # ← Replace with your actual key
API_KEY = ''  # ← Replace with your actual key
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




def fetch_movie_details_and_cast(movie_title):
    search_url = f"https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&query={movie_title}"
    search_response = requests.get(search_url).json()

    if search_response['results']:
        movie = search_response['results'][0]
        movie_id = movie['id']

        details_url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}"
        details_response = requests.get(details_url).json()

        cast_url = f"https://api.themoviedb.org/3/movie/{movie_id}/credits?api_key={API_KEY}"
        cast_response = requests.get(cast_url).json()
        cast = [member['name'] for member in cast_response.get('cast', [])[:3]]

        poster_path = details_response.get('poster_path', '')
        poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else "https://via.placeholder.com/200x300?text=No+Poster"

        omdb_url = f"http://www.omdbapi.com/?t={movie_title}&apikey={OMDB_API_KEY}&plot=full"
        omdb_response = requests.get(omdb_url).json()
        plot = omdb_response.get('Plot', 'No description available.') 

        return {
            "title": details_response.get('title', 'N/A'),
            "Plot": plot,
            "rating": details_response.get('vote_average', 'N/A'),
            "poster_url": poster_url,
            "cast": cast,
            "movie_url": f"https://www.themoviedb.org/movie/{movie_id}"
        }
    return None



def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = list(enumerate(similarity[index]))
    movies_list = sorted(distances, key=lambda x: x[1], reverse=True)[1:6]
    recommended_movies = [movies.iloc[i[0]].title for i in movies_list]
    return recommended_movies

st.set_page_config(page_title="Movie Recommender", page_icon="🎬", layout="centered")

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
    padding: 10px 12px;       
    font-size: 24px !important;     border: none;
    transition: background-color 0.3s ease;
    cursor: pointer;
}

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
    margin-left: -20px; 
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}


.poster-card:hover {
    transform: translateY(-16px) scale(1.08);  
    z-index: 99;  
    box-shadow: 0 16px 32px rgba(0, 0, 0, 0.4);  
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
    width: 500px !important; 
    }
div[data-baseweb="select"] {
    background-color: white !important;
    width: 900px !important;
    font-size: 18px !important;
    border-radius: 8px !important;
    padding: 10px !important;
    margin-top: -30px !important;  
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

div[data-baseweb="select"] * {
    color: black !important;
}
    .stForm button {
    width: 90% !important;
    min-width: 120px !important;
    white-space: nowrap !important;
    margin: 8px auto 0 auto !important;
    font-size: 18px !important;
    border-radius: 8px !important;
    display: block !important;
}
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="title">🎬 Movie Recommender</div>', unsafe_allow_html=True)

st.markdown("""
    <div style="color: white; font-size: 24px; font-weight: bold; margin-bottom: 10px;">
        🎥 Choose a movie you like:
    </div>
""", unsafe_allow_html=True)

selected_movie = st.selectbox(
    "",  # Empty label since we styled it manually
    movies['title'].values,
    key="movie_select"
)

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
    st.session_state.show_recommendations = True

if st.session_state.get("show_recommendations", False):
    recommendations = recommend(selected_movie)
    st.markdown('<h3 style="color: white; font-weight: bold;">📽️ Top 5 Recommendations</h3>', unsafe_allow_html=True)

    spaced_cols = st.columns([4, 4, 40, 4, 40, 4, 40, 0.4, 40, 0.4, 4])
    for movie in recommendations:
        details = fetch_movie_details_and_cast(movie)
        if details:
            st.markdown(f"""
                <div style="display: flex; align-items: flex-start; background: white; border-radius: 16px; box-shadow: 0 8px 20px rgba(0,0,0,0.12); margin: 0 auto 24px auto; max-width: 700px; min-height: 240px;">
                    <img src="{details['poster_url']}" alt="{details['title']} poster" style="border-radius: 12px; width: 160px; height: 240px; object-fit: cover; margin: 16px;">
                    <div style="padding: 16px 20px 16px 0; flex: 1;">
                        <div class="poster-title" style="font-size: 20px; font-weight: bold; color: #333;">{details['title']}</div>
                        <div style="font-size:15px; color:#666; margin: 8px 0 4px 0;">
                            <b>⭐ {round(details['rating'],1)}/10</b>
                            <div style="height:10px"></div>
                            <b>Cast:</b> {', '.join(details['cast'])}
                        </div>
                        <div style="font-size:14px; color:#444; margin-top: 10px;">
                            <b>Plot:</b> {details['Plot']}
                        </div>
                         <div style="margin-top: 12px;">
                <a href="{details['movie_url']}" target="_blank" style="color: #FF4B4B; font-weight: bold; text-decoration: none;">
                    🔗 More Details
                </a>
            </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)

