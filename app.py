import streamlit as st
import pickle
import requests

def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    response = requests.get(url)
    if response.status_code != 200:
        return "https://via.placeholder.com/500x750?text=No+Image"
    data = response.json()
    poster_path = data.get('poster_path')
    if not poster_path:
        return "https://via.placeholder.com/500x750?text=No+Image"
    full_path = f"https://image.tmdb.org/t/p/w500/{poster_path}"
    return full_path

def recommend(movie):
    movie_index = movies[movies['title']==movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])
    recommended_movies = []
    recommended_movies_posters = []
    for i in movie_list[1:6]:

        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies_posters.append(fetch_poster(movie_id))
        recommended_movies.append(movies.iloc[i[0]].title)
    return recommended_movies , recommended_movies_posters

movies = pickle.load(open('movies.pkl','rb'))
similarity = pickle.load(open('similarity.pkl','rb'))
movies_list = movies['title'].values
st.title("Movie Recommender System")

selected_movie_name = st.selectbox(
'Pick your fav movie',movies_list)
if st.button('Show Recommendation'):
    cols = st.columns(5)
    with st.spinner('Fetching recommendations...'):
        recommended_movie_names, recommended_movie_posters = recommend(selected_movie_name)
        for i in range(5):
            with cols[i]:
                st.text(recommended_movie_names[i])
                st.image(recommended_movie_posters[i])