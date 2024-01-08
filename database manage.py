import sqlite3

conn = sqlite3.connect('movie_database.db')
cursor = conn.cursor()

table_name = 'movies_table'
query = f'SELECT * FROM {table_name}'

try:
    cursor.execute(query)
    rows = cursor.fetchall()
    column_name = [description[0] for description in cursor.description]
    print("Columns: ", column_name)
    for row in rows:
        print(row)

except sqlite3.Error as e:
    print("Error: ",e)

conn.close()

# to delete column

# query_2 = 'ALTER TABLE movies_table DROP COLUMN video'
# cursor.execute(query_2)
# print("Columns deleted successfully.")
# conn.commit()
# conn.close()

# query_3 = 'ALTER TABLE movies_table DROP COLUMN adult'
# cursor.execute(query_3)
# print("Columns deleted successfully.")
# conn.commit()
# conn.close()


