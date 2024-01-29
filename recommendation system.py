import sqlite3
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

movies_dataframe = pd.read_pickle('movies_dataframe.pkl')

# Connect to the SQLite database
conn = sqlite3.connect('movie_database.db')
cursor = conn.cursor()
table_name = 'movies_table'

tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix_overview = tfidf.fit_transform(movies_dataframe['overview'])
cosine_sim_overview = linear_kernel(tfidf_matrix_overview)

# Hybrid-based = content-based integrated with the sentiment scores
def get_hybrid_based_recommendation(title, cosine_sim=cosine_sim_overview, movies=movies_dataframe):
    try:
        indx = movies[movies['title'] == title].index[0]
    except IndexError:
        print(f"Movie '{title}' not found in the database.")
        return

    sim_scores = list(enumerate(cosine_sim[indx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:6]
    movies_indices = (i[0] for i in sim_scores)
    hybrid_scores = 0.7 * cosine_sim[indx] + 0.3 * (movies['sentiment_score'] + 1) / 2
    recommended_movies = movies.iloc[movies_indices].sort_values(by=['sentiment_score'], ascending=False)
    # return movies[['title', 'genre_ids', 'poster_path']].iloc[movies_indices]
    return recommended_movies[['title', 'genre_ids', 'poster_path']]

# Get user input for the movie title
movie_title = input('Enter a movie title: ')

# Get hybrid-based recommendations
recommended_movies = get_hybrid_based_recommendation(movie_title)

if recommended_movies is not None:
    print(f"Recommended Movies for '{movie_title}':")
    print(recommended_movies)


