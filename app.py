import streamlit as st
import pickle
import requests

# Function to fetch movie poster
def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=c7ec19ffdd3279641fb606d19ceb9bb1&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

# Function to fetch movie details
def fetch_movie_details(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=c7ec19ffdd3279641fb606d19ceb9bb1&language=en-US"
    response = requests.get(url)
    movie_data = response.json()
    return movie_data

# Function to fetch top cast
def fetch_top_cast(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}/credits?api_key=c7ec19ffdd3279641fb606d19ceb9bb1&language=en-US"
    response = requests.get(url)
    cast_data = response.json()['cast']
    top_cast = [cast['name'] for cast in cast_data[:5]]  # Fetch only the top 5 cast members
    return top_cast

# Load movie data and similarity matrix
movies = pickle.load(open("movies_list.pkl", 'rb'))
similarity = pickle.load(open("similarity.pkl", 'rb'))
movies_list = movies['title'].values

# Set page title and header
st.set_page_config(page_title="Movie Recommendation System", layout="wide")
st.title("Movies Recommendation System")

# Sidebar with movie selection
selected_movie = st.sidebar.selectbox("Select a Movie:", movies_list)

# Function to recommend similar movies
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distance = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda vector: vector[1])
    recommended_movies = []
    for i in distance[1:6]:
        movie_id = movies.iloc[i[0]].id
        movie_name = movies.iloc[i[0]].title
        movie_poster = fetch_poster(movie_id)
        release_date = fetch_movie_details(movie_id)['release_date']
        top_cast = fetch_top_cast(movie_id)
        recommended_movies.append((movie_name, movie_poster, release_date, top_cast))
    return recommended_movies

# Show recommendations button
if st.sidebar.button('Show Recommendations'):
    st.sidebar.subheader("Recommended Movies")
    recommended_movies = recommend(selected_movie)
    cols = st.columns(5)
    for col, (movie_name, movie_poster, release_date, top_cast) in zip(cols, recommended_movies):
        col.image(movie_poster, caption=movie_name, width=150)
        col.write(f"**Release Date:** {release_date}")
        col.write("**Top Cast:**")
        col.write(', '.join(top_cast))
