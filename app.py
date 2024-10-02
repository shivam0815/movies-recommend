import streamlit as st
import pickle
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import time
import streamlit.components.v1 as components

def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=c7ec19ffdd3279641fb606d19ceb9bb1&language=en-US"

    # Create a session with retry and backoff
    session = requests.Session()
    retry = Retry(total=5, backoff_factor=0.3, status_forcelist=[500, 502, 503, 504])
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('https://', adapter)
    
    try:
        response = session.get(url, timeout=10)  # Increased timeout to 10 seconds
        response.raise_for_status()  # Raise HTTPError for bad responses
        data = response.json()
        poster_path = data['poster_path']
        full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
        return full_path
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching poster: {e}")
        return "https://via.placeholder.com/500"  # Fallback image


# Load movie data
movies = pickle.load(open("movies_list.pkl", "rb"))
similarity = pickle.load(open("similarity.pkl", "rb"))
movies_list = movies['title'].values

# Header
st.header("Movie Recommender System")

# Declare custom component for image carousel
imageCarouselComponent = components.declare_component("image-carousel-component", path="frontend/frontend/public")

# Fetch image URLs for the carousel
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

# Display carousel
imageCarouselComponent(imageUrls=imageUrls, height=200)

# Dropdown for movie selection
selectvalue = st.selectbox("Select movies from dropdown", movies_list)

# Recommendation logic
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distance = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda vector: vector[1])
    recommend_movie = []
    recommend_poster = []

    for i in distance[1:11]:
        movies_id = movies.iloc[i[0]].id
        recommend_movie.append(movies.iloc[i[0]].title)
        recommend_poster.append(fetch_poster(movies_id))

    return recommend_movie, recommend_poster


# Display recommendations when button is clicked
if st.button("Show Recommend"):
    movie_name, movie_poster = recommend(selectvalue)
    col1, col2, col3, col4, col5 ,col6,col7,col8,col9,col10= st.columns(10)

    with col1:
        st.text(movie_name[0])
        st.image(movie_poster[0])
    with col2:
        st.text(movie_name[1])
        st.image(movie_poster[1])
    with col3:
        st.text(movie_name[2])
        st.image(movie_poster[2])
    with col4:
        st.text(movie_name[3])
        st.image(movie_poster[3])
    with col5:
        st.text(movie_name[4])
        st.image(movie_poster[4])
    with col6:
        st.text(movie_name[5])
        st.image(movie_poster[5])
    with col7:
        st.text(movie_name[6])
        st.image(movie_poster[6])
    with col8:
        st.text(movie_name[7])
        st.image(movie_poster[7])
    with col9:
        st.text(movie_name[8])
        st.image(movie_poster[8])
    with col10:
        st.text(movie_name[9])
        st.image(movie_poster[9])
    # with col11:
    #     st.text(movie_name[10])
    #     st.image(movie_poster[10])
        

        

# User rating for the movie
rating = st.slider('Rate this movie', 1, 5)
st.text(f'You rated this movie {rating}/5')

# Genre selection
genres = ['Action', 'Comedy', 'Drama', 'Sci-Fi', 'Horror']
selected_genres = st.multiselect('Choose Genres', genres)

# Dictionary mapping genres to YouTube trailer URLs
genre_trailers = {
    'Action': 'https://www.youtube.com/watch?v=6ZfuNTqbHE8',  # Example trailer for Action
    'Comedy': 'https://www.youtube.com/watch?v=t433PEQGErc',  # Example trailer for Comedy
    'Drama': 'https://www.youtube.com/watch?v=0pdqf4P9MB8',   # Example trailer for Drama
    'Sci-Fi': 'https://www.youtube.com/watch?v=8ugaeA-nMTc',  # Example trailer for Sci-Fi
    'Horror': 'https://www.youtube.com/watch?v=abEekH9BhgA'   # Example trailer for Horror
}

# Display the trailer after selecting the genre
if st.button("Show Trailer for Selected Genres"):
    if selected_genres:
        # Only show the trailer of the first selected genre (you can extend this to support multiple genres)
        genre = selected_genres[0]
        trailer_url = genre_trailers.get(genre)
        if trailer_url:
            st.video(trailer_url)
        else:
            st.error("No trailer available for this genre.")
    else:
        st.warning("Please select at least one genre to display the trailer.")


# Custom CSS for hover effect and styling
st.markdown("""
    <style>
    .image-container img:hover {
        transform: scale(1.1);
        transition: 0.3s;
    }
    .image-container {
        display: flex;
        justify-content: space-around;
    }
    .movie-title {
        text-align: center;
        color: #fff;
    }
    </style>
    """, unsafe_allow_html=True)
