import pickle
import streamlit as st
import requests
import streamlit.components.v1 as components

def fetch_poster(movie_id):
    url = ("https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
           .format(movie_id))

    try:
        data = requests.get(url).json()
        # Check if 'poster_path' is present in the API response
        if 'poster_path' in data:
            poster_path = data['poster_path']
            full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
            return full_path
        else:
            # Handle the case where 'poster_path' is not available
            return "No Poster Available"
    except Exception as e:
        # Handle potential API request errors
        print(f"Error fetching poster for movie ID {movie_id}: {e}")
        return "Error Fetching Poster"
    


def recommend(movie):
    index = movies[movies['Series_Title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda vector: vector[1])
    movie_names = []
    movie_posters = []

    for i in distances[1:6]:
        # Use the index as a proxy for movie ID
        movie_id = movies.iloc[i[0]].name
        poster_url = fetch_poster(movie_id)
        
        # Append movie details or error message to the lists
        if "Error" in poster_url:
            movie_posters.append("https://via.placeholder.com/500x750.png?text=Error+Fetching+Poster")
            movie_names.append("Error Fetching Poster")
        elif "No Poster" in poster_url:
            movie_posters.append("https://via.placeholder.com/500x750.png?text=No+Poster+Available")
            movie_names.append(movies.iloc[i[0]]['Series_Title'])
        else:
            movie_posters.append(poster_url)
            movie_names.append(movies.iloc[i[0]]['Series_Title'])

    return movie_names, movie_posters

# Load movie data and similarity matrix
movies = pickle.load(open('movies_list.pk1', 'rb'))
similarity = pickle.load(open('similarity.pk1', 'rb'))

# Streamlit App
st.header('NETFLIX RECOMMENDATION ENGINE')

imageCarouselComponent = components.declare_component("image-carousel-component", path="frontend/public")

imageUrls = [
    fetch_poster(1632),
    fetch_poster(299536),
    fetch_poster(17455),
    fetch_poster(2830),
    fetch_poster(429422),
    fetch_poster(9722),
    fetch_poster(13972),
    fetch_poster(240),
    fetch_poster(155),
    fetch_poster(598),
    fetch_poster(914),
    fetch_poster(255709),
    fetch_poster(572154)

]

imageCarouselComponent(imageUrls=imageUrls, height=200)
movie_list = movies['Series_Title'].values
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)

if st.button('Show Recommendation'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)
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