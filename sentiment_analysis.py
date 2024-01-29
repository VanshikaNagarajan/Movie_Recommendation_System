from textblob import TextBlob
import sqlite3
import pandas as pd


movies_dataframe = pd.read_pickle('movies_dataframe.pkl')

# Connect to the SQLite database
conn = sqlite3.connect('movie_database.db')
cursor = conn.cursor()
table_name = 'movies_table'

# Fetch all rows from the 'movies_table'
query = f'SELECT * FROM {table_name}'
cursor.execute(query)
rows = cursor.fetchall()

# Get the column names
column_names = [description[0] for description in cursor.description]


# Perform sentiment analysis on the 'overview' column
def analyze_sentiment(overview):
    blob = TextBlob(overview)
    sentiment_score = blob.sentiment.polarity
    return sentiment_score

# Apply sentiment analysis to the 'overview' column and store the results in a new column
movies_dataframe['sentiment_score'] = movies_dataframe['overview'].apply(analyze_sentiment)

# Display the DataFrame information
print(movies_dataframe.info())
print(movies_dataframe[['title', 'overview', 'sentiment_score']].head())

# Close the database connection
conn.close()

movies_dataframe.to_pickle('movies_dataframe.pkl')
