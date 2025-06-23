import streamlit as st
import pickle
import requests
import difflib
from streamlit_lottie import st_lottie

# ------------------------------- STYLING -------------------------------
st.set_page_config(page_title="🎬 Movie Recommender", layout="wide")
st.markdown("""
    <style>
    .stApp {
        background-image: url("https://images.unsplash.com/photo-1497032628192-86f99bcd76bc");
        background-size: cover;
        color: white;
    }
    .stButton>button {
        background-color: #FF4B4B;
        color: white;
        font-size: 18px;
        border-radius: 8px;
        padding: 0.5em 1em;
    }
    .stSelectbox>div>div {
        background-color: rgba(0,0,0,0.6);
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# ------------------------------- LOAD DATA -------------------------------
movies = pickle.load(open('movies.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

# ------------------------------- LOTTIE ANIMATION -------------------------------
def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

lottie_cinema = load_lottieurl("https://assets1.lottiefiles.com/packages/lf20_ydo1amjm.json")
st_lottie(lottie_cinema, height=200, key="cinema")

# ------------------------------- FETCH FUNCTIONS -------------------------------
@st.cache_data(show_spinner=False)
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        poster_path = data.get('poster_path')
        return f"https://image.tmdb.org/t/p/w500/{poster_path}" if poster_path else "https://via.placeholder.com/500x750?text=No+Image"
    except requests.exceptions.Timeout:
        st.warning("⏳ TMDb API timed out. Using placeholder image.")
        return "https://via.placeholder.com/500x750?text=No+Image"
    except requests.exceptions.RequestException as e:
        st.error(f"⚠️ Error fetching poster: {e}")
        return "https://via.placeholder.com/500x750?text=No+Image"

def fetch_movie_details(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8"
    try:
        response = requests.get(url)
        data = response.json()
        rating = data.get('vote_average', 'N/A')
        genres = ', '.join([genre['name'] for genre in data.get('genres', [])])
        return {"rating": rating, "genres": genres}
    except:
        return {"rating": "N/A", "genres": "Unknown"}

# ------------------------------- RECOMMENDATION LOGIC -------------------------------
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])
    recommended_movies = []
    for i in movie_list[1:6]:
        movie_data = movies.iloc[i[0]]
        movie_id = movie_data.movie_id
        details = fetch_movie_details(movie_id)
        recommended_movies.append({
            "title": movie_data.title,
            "poster": fetch_poster(movie_id),
            "rating": details['rating'],
            "genres": details['genres']
        })
    return recommended_movies

# ------------------------------- UI -------------------------------
st.title("🎥 Movie Recommender System")

user_input = st.text_input("🔍 Search a movie")

if user_input:
    closest_match = difflib.get_close_matches(user_input, movies['title'].values, n=1)
    if closest_match:
        selected_movie_name = closest_match[0]
        st.success(f"Found: {selected_movie_name}")
        if st.button("🎯 Show Recommendation"):
            with st.spinner("Fetching recommendations..."):
                recommendations = recommend(selected_movie_name)
                cols = st.columns(5)
                for idx, col in enumerate(cols):
                    movie = recommendations[idx]
                    with col:
                        st.markdown(f"""
                        <div style='background-color:#000000aa; padding:10px; border-radius:10px; text-align:center'>
                            <img src='{movie["poster"]}' width='150'><br>
                            <strong>{movie["title"]}</strong><br>
                            ⭐ {movie["rating"]} | 🎭 {movie["genres"]}
                        </div>
                        """, unsafe_allow_html=True)
    else:
        st.error("No close match found. Try again.")
