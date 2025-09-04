import streamlit as st
import pickle
import pandas as pd
import requests
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
TMDB_API_KEY = os.getenv("TMDB_API_KEY")

if not TMDB_API_KEY:
    st.error("TMDB API key not found. Please check your .env file.")
    st.stop()


def fetch_poster(movie_id):
    """Fetch movie poster image URL using The Movie Database API."""
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={TMDB_API_KEY}&language=en-US"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        poster_path = data.get("poster_path")
        if poster_path:
            return f"https://image.tmdb.org/t/p/w500/{poster_path}", data["id"]
        else:
            # Fallback image if poster not found
            return "https://via.placeholder.com/500x750?text=No+Poster", data["id"]

    except requests.exceptions.RequestException as e:
        st.warning(f"Poster fetch failed: {e}")
        return "https://via.placeholder.com/500x750?text=Error", movie_id


def fetch_movie_wikipedia_link(movie_name):
    """Generate Wikipedia URL for the movie."""
    return f"https://en.wikipedia.org/wiki/{movie_name.replace(' ', '_')}"


def movie_recommend(movie):
    """Recommend similar movies based on the selected movie."""
    movie_index = movies[movies["title"] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:11]

    recommended_movies = []
    recommended_movies_posters = []
    movie_links = []

    for i in movies_list:
        movie_id = movies.iloc[i[0]].id
        title = movies.iloc[i[0]].title
        poster, _ = fetch_poster(movie_id)

        recommended_movies.append(title)
        recommended_movies_posters.append(poster)
        movie_links.append(fetch_movie_wikipedia_link(title))

    return recommended_movies, recommended_movies_posters, movie_links


# Load movie data and similarity matrix
with open("movies_dict.pkl", "rb") as file:
    movies_dict = pickle.load(file)
movies = pd.DataFrame(movies_dict)

with open("similarity.pkl", "rb") as file:
    similarity = pickle.load(file)

# Streamlit app UI
st.title("🎬 Cine Crave - Movie Recommender")

# Movie selection dropdown with filtering
selected_movie_name = st.selectbox("Select a movie", movies["title"].values)

if st.button("Recommend"):
    names, posters, links = movie_recommend(selected_movie_name)

    # Display 10 movie recommendations with posters in 2 rows of 5
    for i in range(0, 10, 5):
        row_names = names[i:i+5]
        row_posters = posters[i:i+5]
        row_links = links[i:i+5]

        cols = st.columns(5)
        for j, col in enumerate(cols):
            if j < len(row_names):
                with col:
                    st.markdown(f"[![{row_names[j]}]({row_posters[j]})]({row_links[j]})")
                    st.caption(row_names[j])
