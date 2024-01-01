import requests
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel


url = "https://api.themoviedb.org/3/discover/movie?include_adult=false&include_video=false&language=en-US&page=1&sort_by=popularity.desc"
print(url)
headers = {
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIxZjQwMDYxYjJlOGFmY2YyMTUyZGQ0NWU5NWJlOTQyOCIsInN1YiI6IjY1OGU3NWEwNjRmNzE2MjIyNDNmN2QxNCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.RMgEWpaRJzN8DcNLWYr3x-F7ZgaQ1pBSo79TUMv8S3c"
}

response = requests.get(url, headers=headers)
print(response)

if response.status_code == 200:
    movie_data = response.json()
    if 'results' in movie_data:
        movies = movie_data['results']
        movie_df = pd.json_normalize(movies)
        print(movie_df)
    else:
        print('No movie data found in the response.')
else:
    print("Failed to retrieve data. Status code:", response.status_code)


null_overviews = movie_df['overview'].isnull().sum()
print(null_overviews)

tfidf = TfidfVectorizer(stop_words = 'english')
tfidf_matrix_overview = tfidf.fit_transform(movie_df['overview'])
cosine_sim_overview = linear_kernel(tfidf_matrix_overview)

print('scuccessfully converted to numeric value')
def get_recommendations(title, cosine_sim = cosine_sim_overview, movies = movie_df):
    indx = movies[movies['title'] == title].index[0]
    sim_scores = list(enumerate(cosine_sim[indx]))
    sim_scores = sorted(sim_scores, key = lambda x : x[1], reverse = True)
    sim_scores = sim_scores[1:6]
    movies_indices = (i[0] for i in sim_scores)
    return movies[['title', 'genre_ids', 'poster_path']].iloc[movies_indices]

print('getting recommended movies')

movie_title = input('Enter a movie title: ')
recommended_movies = get_recommendations(movie_title)
print("Recommended Movies for '{}':".format(movie_title))
print(recommended_movies)


