import streamlit as st
import pickle
import pandas as pd
import requests

def poster(movi_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=260da7fcb4a9fe7d55ffb2be36ec8400&language=en-US'.format(movi_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']


movies = pickle.load(open('DF.pkl', 'rb'))
movie_df = pd.DataFrame(movies)
similarities = pickle.load(open('similarity.pkl', 'rb'))
st.title("Movie Recommender System")

selected_movie = st.selectbox(
    'Write your movie name',
    movie_df['title'].values)


def recommend(movie):
    idx = movie_df[movie_df['title']==movie].index[0]
    distances = similarities[idx]
    movie_lst = sorted(list(enumerate(distances)), reverse = True, key = lambda x: x[1])[1:6]
    recommended = []
    posters = []
    for i in movie_lst:
        recommended.append(movie_df.iloc[i[0]].title)
        movi_id = movie_df.iloc[i[0]].movie_id
        posters.append(poster(movi_id))
    return recommended, posters


if st.button("Recommend"):
    recommendations, posters = recommend(selected_movie)
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.text(recommendations[0])
        st.image(posters[0])

    with col2:
        st.text(recommendations[1])
        st.image(posters[1])

    with col3:
        st.text(recommendations[2])
        st.image(posters[2])

    with col4:
        st.text(recommendations[3])
        st.image(posters[3])

    with col5:
        st.text(recommendations[4])
        st.image(posters[4])
