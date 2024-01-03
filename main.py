import requests
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import sys
import sqlite3


# fetching movie api
url = "https://api.themoviedb.org/3/discover/movie?include_adult=false&include_video=false&language=en-US&page=1&sort_by=popularity.desc"

headers = {
    "accept": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIxZjQwMDYxYjJlOGFmY2YyMTUyZGQ0NWU5NWJlOTQyOCIsInN1YiI6IjY1OGU3NWEwNjRmNzE2MjIyNDNmN2QxNCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.RMgEWpaRJzN8DcNLWYr3x-F7ZgaQ1pBSo79TUMv8S3c"
}

response = requests.get(url, headers=headers)

print(response.text)



if response.status_code == 200:
    movie_data = response.json()
    if 'results' in movie_data:
        movies = movie_data['results']
        # creating a dataframe to store the fetched data from the api
        movies_df = pd.json_normalize(movies)
        print(movies_df)
    else:
        print('No movie data found in the response.')
else:
    print("Failed to retrieve data. Status code:", response.status_code)
# print(movies_df.dtypes)
# movies_df['genre_ids'] = movies_df['genre_ids'].astype(str)
# bool_columns = ['adult', 'video']
# movies_df[bool_columns] = movies_df[bool_columns].astype(int)
# conn = sqlite3.connect('movie_database.db')
# movies_df.to_sql('movies_table', conn, if_exists='replace', index=False)
# conn.commit()
# conn.close()

null_overviews = movies_df['overview'].isnull().sum()
print(null_overviews)


tfidf = TfidfVectorizer(stop_words = 'english')
tfidf_matrix_overview = tfidf.fit_transform(movies_df['overview'])
cosine_sim_overview = linear_kernel(tfidf_matrix_overview)

print('scuccessfully converted to numeric value')
def get_recommendations(title, cosine_sim = cosine_sim_overview, movies = movies_df):
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

# fetching weather api
response2 = requests.request("GET",
                            "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/india?unitGroup=us&key=PB8ALQT9SSB4S24S6USTQ2HAW&contentType=json")
if response2.status_code != 200:
    print('Unexpected Status code: ', response2.status_code)
    sys.exit()

# Parse the results as JSON
jsonData = response2.json()
print(jsonData)
print('successfully fetched data')


# extracting weather attributes
weather_data = []
for day in jsonData['days']:
    humidity = day['humidity']
    sunrise = day['sunrise']
    sunset = day['sunset']
    precipitation = day['precip']
    temperature = day['temp']
    weather_data.append({'humidity': humidity, 'sunrise': sunrise, 'sunset': sunset, 'precip': precipitation, 'temp': temperature})

#
weather_df = pd.DataFrame(weather_data)
print(weather_df)

conn1 = sqlite3.connect('weather_database.db')
weather_df.to_sql('weather_table', conn1, if_exists= 'replace', index = False)
conn1.commit()
conn1.close()

