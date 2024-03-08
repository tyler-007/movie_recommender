import pickle
import streamlit as st
import requests
import os
#yeaah
def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

def recommend(movie):
    index = new_df[new_df['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        movie_id = new_df.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(new_df.iloc[i[0]].title)

    return recommended_movie_names,recommended_movie_posters

def display_recommendations(movie_names, movie_posters, num_columns=5):
    num_recommendations = len(movie_names)
    cols = [st.columns(num_columns) for _ in range(num_recommendations)]

    for i, (col, (name, poster)) in enumerate(zip(cols, zip(movie_names, movie_posters))):
        with col[i % num_columns]:
            st.text(name)
            st.image(poster, caption=None, width=None, use_column_width=None, clamp=False, channels="RGB", output_format="auto")


st.header('Hollywood Movie Recommendation')


import os
import pandas as pd

# Assuming pickle files are in the 'movie-recommender' directory
pickle_directory = 'movie-recommender'

# Print current working directory
print("Current working directory:", os.getcwd())

try:
    with open(os.path.join(pickle_directory, 'movie_list.pkl'), 'rb') as file:
        new_df = pd.read_pickle(file)
except Exception as e:
    print(f"Error loading pickle file: {e}")

#print("new_df:", new_df)

try:
    with open(os.path.join(pickle_directory, 'similarity.pkl'), 'rb') as filex:
        similarity = pd.read_pickle(filex)
except Exception as e:
    print(f"Error loading pickle file: {e}")

#print(new_df)
#print("similarity:", similarity)



movie_list = new_df['title'].values
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)



if st.button('Show Recommendation'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)
    display_recommendations(recommended_movie_names, recommended_movie_posters)


