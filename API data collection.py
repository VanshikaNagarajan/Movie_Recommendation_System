import requests
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import sys
import sqlite3
from sqlalchemy import create_engine
import ast


# fetching movie api
url = "https://api.themoviedb.org/3/discover/movie?include_adult=false&include_video=false&language=en-US&page=1&sort_by=popularity.desc"

headers = {
     "accept": "application/json",
     "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIxZjQwMDYxYjJlOGFmY2YyMTUyZGQ0NWU5NWJlOTQyOCIsInN1YiI6IjY1OGU3NWEwNjRmNzE2MjIyNDNmN2QxNCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.RMgEWpaRJzN8DcNLWYr3x-F7ZgaQ1pBSo79TUMv8S3c"
}

response = requests.get(url, headers=headers)

# print(response.text)


# checking the url access and converting the json data into a dataframe
if response.status_code == 200:
    movie_data = response.json()
    if 'results' in movie_data:
        movies = movie_data['results']
        # creating a dataframe to store the fetched data from the api
        movies_df = pd.json_normalize(movies)
        # print(movies_df)
    else:
        print('No movie data found in the response.')
else:
    print("Failed to retrieve data. Status code:", response.status_code)
# print(movies_df.dtypes)


# fetching genre names from api

url = "https://api.themoviedb.org/3/genre/movie/list?language=en"

headers = {
    "accept": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIxZjQwMDYxYjJlOGFmY2YyMTUyZGQ0NWU5NWJlOTQyOCIsInN1YiI6IjY1OGU3NWEwNjRmNzE2MjIyNDNmN2QxNCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.RMgEWpaRJzN8DcNLWYr3x-F7ZgaQ1pBSo79TUMv8S3c"
}

response = requests.get(url, headers=headers)
# print(response.text)

# getting genre names mapped to genre ids
genre_mapping = {
    28: "Action",
    12: "Adventure",
    16: "Animation",
    35: "Comedy",
    80: "Crime",
    99: "Documentry",
    18: "Drama",
    10751: "Family",
    14: "Fantasy",
    36: "History",
    27: "Horror",
    10402: "Music",
    9648: "Mystery",
    10749: "Romance",
    878: "Science Fiction",
    10770: "TV Movie",
    53: "thriller",
    10752: "War",
    37: "Western"
}
movies_df['genre_ids'] = movies_df['genre_ids'].apply(lambda ids: [int(id) for id in ids if int(id) in genre_mapping])
movies_df['genre_names'] = movies_df['genre_ids'].apply(lambda ids: [genre_mapping[id] for id in ids])
# print(movies_df[['genre_ids', 'genre_names']])
# print(movies_df)


# to integrate weather with genre
weather_genre_mapping = {
    'Sunny': ['Adventure', 'Comedy', 'Family', 'Science Fiction'],
    'Cloudy': ['Drama', 'Romance', 'Documentary'],
    'Rainy': ['Mystery', 'Thriller', 'Crime'],
    'Pleasant Day': ['Animation', 'Fantasy', 'Music'],
    'Stormy': ['Action', 'Horror', 'War'],
    'Foggy': ['Mystery', 'Western']
 }
#
# Function to map genres to weather conditions
def map_to_weather_genre(genres):
    result = []
    for weather, genre_list in weather_genre_mapping.items():
        if any(genre in genre_list for genre in genres):
            result.append(weather)
    return result

# Apply the mapping function to the 'genre_names' column
movies_df['weather_genre'] = movies_df['genre_names'].apply(map_to_weather_genre)
# print(movies_df[['genre_names', 'weather_genre']])

# converting list to string
movies_df['genre_ids'] = movies_df['genre_ids'].apply(lambda x: ','.join(map(str, x)))
movies_df['genre_names'] = movies_df['genre_names'].apply(lambda x: ','.join(map(str, x)))
movies_df['weather_genre'] = movies_df['weather_genre'].apply(lambda x: ','.join(map(str, x)))
bool_columns = ['adult', 'video']
movies_df[bool_columns] = movies_df[bool_columns].astype(int)



# creating database
'''
conn = sqlite3.connect('movie_database.db')
movies_df.to_sql('movies_table', conn, if_exists='replace', index=False)
conn.commit()
conn.close()
'''
'''
# creating csv file
engine = create_engine('sqlite:///movie_database.db')
df = pd.read_sql_table('movies_table', con=engine)
df.to_csv('movie.csv', index=False)
'''

'''
# checking null values
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
'''

# fetching weather api
response2 = requests.request("GET",
                            "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/india?unitGroup=us&key=PB8ALQT9SSB4S24S6USTQ2HAW&contentType=json")
if response2.status_code != 200:
    print('Unexpected Status code: ', response2.status_code)
    sys.exit()

# Parse the results as JSON
jsonData = response2.json()
# print(jsonData)
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


weather_df = pd.DataFrame(weather_data)
# print(weather_df)

'''
conn1 = sqlite3.connect('weather_database.db')
weather_df.to_sql('weather_table', conn1, if_exists= 'replace', index = False)
conn1.commit()
conn1.close()

engine = create_engine('sqlite:///weather_database.db')
df = pd.read_sql_table('weather_table', con=engine)
df.to_csv('weather.csv', index=False)
'''


print(movies_df)
print(weather_df)