import requests
import json
from cluster_users import cluster_users_and_recommend, ratings_df
from other_scores import euclidean_score, pearson_score, get_recommendations
from rich.console import Console

api_key = '69a9aef3'
console = Console()
with open('ratings.json', 'r', encoding='utf-8') as file:
    ratings_data = json.load(file)


def get_movie_details(title):
    """
        Sprawdza, czy film istnieje w bazie OMDb i zwraca jego szczegóły.

        Args:
            title (str): Tytuł filmu do wyszukania.

        Returns:
            dict: Zawiera klucze:
                - "exists" (bool): Czy film istnieje w bazie OMDb.
                - "title" (str): Tytuł filmu (jeśli istnieje).
                - "description" (str): Opis filmu (jeśli istnieje).
        """

    url = f"http://www.omdbapi.com/?t={title}&apikey={api_key}"
    response = requests.get(url)
    data = response.json()

    if data.get('Response') == 'True':
        return {
            "exists": True,
            "title": data.get('Title', 'Brak tytułu'),
            "description": data.get('Plot', 'Brak opisu')
        }
    else:
        return {"exists": False}


def add_movie_descriptions(movies):
    """
        Dodaje opisy do listy filmów.

        Args:
            movies (list): Lista tytułów filmów.

        Returns:
            list: Lista słowników zawierających:
                - "title" (str): Tytuł filmu.
                - "description" (str): Opis filmu (lub informację o braku filmu w OMDb).
        """

    movie_details = []
    for movie in movies:
        details = get_movie_details(movie)
        if details['exists']:
            movie_details.append({
                "title": details['title'],
                "description": details['description']
            })
        else:
            movie_details.append({
                "title": movie,
                "description": "Film nie istnieje w OMDb"
            })
    return movie_details


user_name = "Mateusz Wisniewski"
top_movies, anti_movies = cluster_users_and_recommend(user_name, ratings_df)

console.rule("[purple]Klasteryzacja[/purple]")
print(f"Top 5 rekomendacji dla użytkownika {user_name}:")
for movie in add_movie_descriptions(top_movies):
    console.print(f"- [green]{movie['title']}[/green]: {movie['description']}")
print(f"\nTop 5 antyrekomendacji dla użytkownika {user_name}:")
for movie in add_movie_descriptions(anti_movies):
    console.print(f"- [red]{movie['title']}[/red]: {movie['description']}")

console.rule("[purple]Euclidean[/purple]")
recommendations_euclidean, anti_recommendations_euclidean = get_recommendations(ratings_data, user_name,
                                                                                euclidean_score)
print(f"Top 5 rekomendacji dla użytkownika {user_name}:")
for movie in add_movie_descriptions(recommendations_euclidean):
    console.print(f"- [green]{movie['title']}[/green]: {movie['description']}")
print(f"\nTop 5 antyrekomendacji dla użytkownika {user_name}:")
for movie in add_movie_descriptions(anti_recommendations_euclidean):
    console.print(f"- [red]{movie['title']}[/red]: {movie['description']}")

console.rule("[purple]Pearson[/purple]")
recommendations_pearson, anti_recommendations_pearson = get_recommendations(ratings_data, user_name, pearson_score)

print(f"Top 5 rekomendacji dla użytkownika {user_name}:")
for movie in add_movie_descriptions(recommendations_pearson):
    console.print(f"- [green]{movie['title']}[/green]: {movie['description']}")
print(f"\nTop 5 antyrekomendacji dla użytkownika {user_name}:")
for movie in add_movie_descriptions(anti_recommendations_pearson):
    console.print(f"- [red]{movie['title']}[/red]: {movie['description']}")
