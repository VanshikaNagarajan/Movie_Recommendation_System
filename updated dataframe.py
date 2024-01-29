import sqlite3
import pandas as pd

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

# Create an empty dictionary to store data
data = {col_name: [] for col_name in column_names}

# Fill the dictionary with data from the database
for row in rows:
    for col_index, col_name in enumerate(column_names):
        data[col_name].append(row[col_index])

# Create a DataFrame from the data
updated_movie_df = pd.DataFrame(data)

# Display the DataFrame information
print(updated_movie_df.info())
print(updated_movie_df.head())

# Close the database connection
conn.close()
