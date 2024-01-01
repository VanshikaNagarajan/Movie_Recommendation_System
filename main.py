import requests
import pandas as pd


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
        df = pd.json_normalize(movies)
    # Process the retrieved movie data as needed
        print(df)
    else:
        print('No movie data found in the response.')
else:
    print("Failed to retrieve data. Status code:", response.status_code)

