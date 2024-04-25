import sqlite3
import pandas as pd

# Load movie data from file
movies_df = pd.read_pickle('movies_dataframe.pkl')

# Connect to SQLite database
conn = sqlite3.connect('movie_database.db')

# Define weather-genre mapping
weather_genre_mapping = {
    'Sunny': ['Adventure', 'Comedy', 'Family', 'Science Fiction'],
    'Cloudy': ['Drama', 'Romance', 'Documentary'],
    'Rainy': ['Mystery', 'Thriller', 'Crime'],
    'Pleasant Day': ['Animation', 'Fantasy', 'Music'],
    'Stormy': ['Action', 'Horror', 'War'],
    'Foggy': ['Mystery', 'Western']
}

# Get user input for weather condition
user_weather_input = input('Enter the current weather condition (Sunny, Cloudy, Rainy, etc.): ')

# Map user's weather input to corresponding movie genres
user_weather_genres = weather_genre_mapping.get(user_weather_input, [])

# Filter movies based on weather-genre mapping
filtered_movies_df = movies_df[movies_df['genre_names'].apply(lambda genres: any(genre in user_weather_genres for genre in genres.split(',')))]

# Generate recommendations (for demonstration, select the top 5 most popular movies)
recommendations = filtered_movies_df.nlargest(5, 'popularity')[['title', 'genre_names']]

# Display recommendations to the user
print(f"Recommended Movies for {user_weather_input}:")
print(recommendations)
