import streamlit as st
import pickle
import pandas as pd
import requests

movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))

movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

api = 'api.themoviedb.org/3/movies/<movie_id>?api_key=db2f5da27fac4304f002b9d7137a13c2&language=en-US'

def recommend(movie):
    index = movies[movies['title']==movie].index[0]
    distances = similarity[index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x:x[1])[1:6]
    
    def fetch_poster(movie_id):
        url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=db2f5da27fac4304f002b9d7137a13c2&language=en-US'
        response = requests.get(url)
        data = response.json()
        
        # Check for errors in the response
        if response.status_code == 200 and 'poster_path' in data:
            poster_path = data['poster_path']
            full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
            return full_path
        else:
            print(f"Error: {data.get('status_message', 'Unknown error occurred')}")
            return None

    recommend_movies = []
    recommend_movies_poster = []

    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id

        #fetch posters from API
        recommend_movies_poster.append(fetch_poster(movie_id))

        recommend_movies.append(movies.iloc[i[0]].title)
    
    return recommend_movies, recommend_movies_poster



st.title('Movie Recomender System')

movie = st.selectbox('Select or Search Movies', movies['title'].values)

if st.button('Show Recommendation'):
    recommended_movie_names,recommended_movie_posters = recommend(movie)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(recommended_movie_names[0])
        st.image(recommended_movie_posters[0])
    with col2:
        st.text(recommended_movie_names[1])
        st.image(recommended_movie_posters[1])

    with col3:
        st.text(recommended_movie_names[2])
        st.image(recommended_movie_posters[2])
    with col4:
        st.text(recommended_movie_names[3])
        st.image(recommended_movie_posters[3])
    with col5:
        st.text(recommended_movie_names[4])
        st.image(recommended_movie_posters[4])
