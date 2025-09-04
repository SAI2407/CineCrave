import streamlit as st
import pandas as pd
import requests
import numpy as np
import pickle
import logging
from dotenv import load_dotenv
import os   
st.title("Top 50 Movies")
load_dotenv()
TMDB_API_KEY = os.getenv("TMDB_API_KEY")

# Configure logging
logging.basicConfig(level=logging.INFO)

def fetch_poster(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={TMDB_API_KEY}&language=en-US"
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad responses

        data = response.json()

        # Check if 'poster_path' exists in the data and is not None
        if 'poster_path' in data and data['poster_path']:
            return "https://image.tmdb.org/t/p/w500/" + data["poster_path"], data["id"]
        else:
            logging.warning(f"No poster path found for movie ID {movie_id}")
            return None, None

    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching poster for movie ID {movie_id}: {e}")
        return None, None
    except Exception as e:
        logging.error(f"Unexpected error fetching poster for movie ID {movie_id}: {e}")
        return None, None

def top_50_movies():
    movie_index = q_movies.index[0]
    movies_list = q_movies["title"][:50]  # Get the top 50 movies
    
    top_movies = [] 
    top_movies_posters = []   
    movie_ids = [] 
    for title in movies_list:
        movie_id = q_movies[q_movies['title'] == title].iloc[0, 3]  # Ensure correct column index for movie_id
        poster, movie_id = fetch_poster(movie_id)
        top_movies.append(title)
        top_movies_posters.append(poster)
        movie_ids.append(movie_id)
  
    return top_movies, top_movies_posters, movie_ids

with open("q_movies_dict.pkl", "rb") as file:
    q_movies_dict = pickle.load(file)

    q_movies = pd.DataFrame(q_movies_dict)

names, posters, movie_ids = top_50_movies()

# Create rows of 5 movies per row (10 rows total)
for i in range(0, len(names), 5):
    row_names = names[i:i+5]
    row_posters = posters[i:i+5]
    row_ids = movie_ids[i:i+5]
    
    # Create a row with 5 columns
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        if row_posters[0]:
            st.markdown(f"[![{row_names[0]}]({row_posters[0]})](https://en.wikipedia.org/wiki/{row_names[0].replace(' ', '_')})")
    
    with col2:
        if row_posters[1]:
            st.markdown(f"[![{row_names[1]}]({row_posters[1]})](https://en.wikipedia.org/wiki/{row_names[1].replace(' ', '_')})")
    
    with col3:
        if row_posters[2]:
            st.markdown(f"[![{row_names[2]}]({row_posters[2]})](https://en.wikipedia.org/wiki/{row_names[2].replace(' ', '_')})")
    
    with col4:
        if row_posters[3]:
            st.markdown(f"[![{row_names[3]}]({row_posters[3]})](https://en.wikipedia.org/wiki/{row_names[3].replace(' ', '_')})")
    
    with col5:
        if row_posters[4]:
            st.markdown(f"[![{row_names[4]}]({row_posters[4]})](https://en.wikipedia.org/wiki/{row_names[4].replace(' ', '_')})")
