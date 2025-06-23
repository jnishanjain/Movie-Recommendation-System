import streamlit as st
import pickle
import requests

# ------------------------ Caching API requests ------------------------

@st.cache_data(show_spinner=False)
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        poster_path = data.get('poster_path')
        if not poster_path:
            return "https://via.placeholder.com/500x750?text=No+Image"
        return f"https://image.tmdb.org/t/p/w500/{poster_path}"
    except:
        return "https://via.placeholder.com/500x750?text=No+Image"

# ------------------------ Recommendation Logic ------------------------

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])
    recommended_movies = []
    recommended_posters = []
    for i in movie_list[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_posters

# ------------------------ Load data ------------------------

movies = pickle.load(open('movies.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

# ------------------------ Streamlit UI ------------------------

st.set_page_config(page_title="Movie Recommender", layout="wide")

# Inject custom CSS
st.markdown("""
    <style>
    body {
        background: linear-gradient(to right, #0f2027, #203a43, #2c5364);
        color: white;
    }
    .big-title {
        font-size: 50px;
        text-align: center;
        color: #FF4B4B;
        font-weight: bold;
        margin-bottom: 20px;
    }
    .poster-container img {
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.6);
        transition: transform 0.2s ease;
    }
    .poster-container img:hover {
        transform: scale(1.05);
    }
    </style>
""", unsafe_allow_html=True)

# Title
st.markdown("<div class='big-title'>🎬 Movie Recommender System</div>", unsafe_allow_html=True)

selected_movie = st.selectbox("Choose a movie you like:", movies['title'].values)

if st.button("🚀 Get My Movie Recommendations"):
    with st.spinner("🔍 Finding best matches..."):
        names, posters = recommend(selected_movie)
        cols = st.columns(5)
        for i in range(5):
            with cols[i]:
                st.markdown("<div class='poster-container'>", unsafe_allow_html=True)
                st.image(posters[i], use_container_width=True)
                st.markdown(f"**{names[i]}**")
                st.markdown("</div>", unsafe_allow_html=True)

# Footer
st.markdown("<hr style='border:1px solid #f63366'>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Built with ❤️ using Streamlit</p>", unsafe_allow_html=True)
