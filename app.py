import streamlit as st
import pickle
import requests

# 🔄 Optional caching to reduce API hits and improve speed
@st.cache_data(show_spinner=False)
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    try:
        response = requests.get(url, timeout=5)  # Add timeout
        response.raise_for_status()
        data = response.json()
        poster_path = data.get('poster_path')
        if not poster_path:
            return "https://via.placeholder.com/500x750?text=No+Image"
        return f"https://image.tmdb.org/t/p/w500/{poster_path}"
    except requests.exceptions.Timeout:
        st.warning("⏳ TMDb API timed out. Using placeholder image.")
        return "https://via.placeholder.com/500x750?text=No+Image"
    except requests.exceptions.RequestException as e:
        st.error(f"⚠️ Error fetching poster: {e}")
        return "https://via.placeholder.com/500x750?text=No+Image"

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])
    recommended_movies = []
    recommended_movies_posters = []
    for i in movie_list[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_posters

# 🔄 Load data
movies = pickle.load(open('movies.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

# 🎬 UI
st.set_page_config(page_title="Movie Recommender", layout="wide")
st.title("🎥 Movie Recommender System")

selected_movie_name = st.selectbox("Pick your favorite movie", movies['title'].values)

if st.button('🎯 Show Recommendation'):
    with st.spinner('Fetching recommendations...'):
        names, posters = recommend(selected_movie_name)
        cols = st.columns(5)
        for i in range(5):
            with cols[i]:
                st.image(posters[i])
                st.caption(names[i])
