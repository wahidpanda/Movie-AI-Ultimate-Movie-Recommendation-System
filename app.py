import pickle
import streamlit as st
import requests
import random

# Function to fetch movie poster
def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

# Function to recommend movies
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        # fetch the movie poster
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names, recommended_movie_posters

# Load data and similarity matrices
movies = pickle.load(open('movie_list.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Sidebar Options
st.sidebar.title("Filter Options")

# Check if 'release_year' column exists in the DataFrame
if 'release_year' in movies.columns:
    # Slider for release year
    release_year_filter = st.sidebar.slider("Filter by Release Year", min_value=int(movies['release_year'].min()), max_value=int(movies['release_year'].max()), step=1)
else:
    st.sidebar.text("Release year information not available in this dataset.")
    release_year_filter = None

# Check if 'cast' column exists in the DataFrame
if 'cast' in movies.columns:
    # Randomly select an actor/actress from the movie dataset
    random_actor = random.choice(movies['cast'].str.split(',').explode().str.strip().unique())

    # Display random actor/actress and add a note about its randomness
    st.sidebar.text(f"Random Actor/Actress: {random_actor} (for demonstration purposes)")

    # Text input for choosing actor/actress
    actor_name = st.sidebar.text_input("Search by Actor/Actress Name")

    # Apply Filters
    filtered_movies = movies.copy()

    if release_year_filter is not None:
        filtered_movies = filtered_movies[filtered_movies['release_year'] == release_year_filter]

    if actor_name:
        filtered_movies = filtered_movies[filtered_movies['cast'].str.contains(actor_name, case=False)]
else:
    st.sidebar.text("Actor/Actress information not available in this dataset.")
    filtered_movies = movies.copy()

# Streamlit App
st.header('Movie Recommender System')

# Dropdown to select a movie
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    filtered_movies['title'].values
)

# Button to show recommendations
if st.button('Show Recommendation'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)

    # Display recommended movies and posters in columns
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(recommended_movie_names[0])
        st.image(recommended_movie_posters[0], width=150)
    with col2:
        st.text(recommended_movie_names[1])
        st.image(recommended_movie_posters[1], width=150)
    with col3:
        st.text(recommended_movie_names[2])
        st.image(recommended_movie_posters[2], width=150)
    with col4:
        st.text(recommended_movie_names[3])
        st.image(recommended_movie_posters[3], width=150)
    with col5:
        st.text(recommended_movie_names[4])
        st.image(recommended_movie_posters[4], width=150)
