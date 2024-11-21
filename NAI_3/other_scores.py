import json
import numpy as np


def euclidean_score(dataset, user1, user2):
    """
        Oblicza wynik podobieństwa między dwoma użytkownikami na podstawie odległości euklidesowej.

        Args:
            dataset (dict): Zbiór danych zawierający oceny filmów przez użytkowników.
            user1 (str): Pierwszy użytkownik.
            user2 (str): Drugi użytkownik.

        Returns:
            float: Wynik podobieństwa, gdzie wyższa wartość oznacza większe podobieństwo.
                   Zwraca 0, jeśli nie ma wspólnych ocen.
        """

    if user1 not in dataset:
        raise TypeError('Cannot find ' + user1 + ' in the dataset')

    if user2 not in dataset:
        raise TypeError('Cannot find ' + user2 + ' in the dataset')

    common_movies = {}

    for item in dataset[user1]:
        if item in dataset[user2]:
            common_movies[item] = 1

    if len(common_movies) == 0:
        return 0

    squared_diff = []

    for item in dataset[user1]:
        if item in dataset[user2]:
            squared_diff.append(np.square(dataset[user1][item] - dataset[user2][item]))

    return 1 / (1 + np.sqrt(np.sum(squared_diff)))


def pearson_score(dataset, user1, user2):
    """
        Oblicza wynik podobieństwa między dwoma użytkownikami na podstawie współczynnika korelacji Pearsona.

        Args:
            dataset (dict): Zbiór danych zawierający oceny filmów przez użytkowników.
            user1 (str): Pierwszy użytkownik.
            user2 (str): Drugi użytkownik.

        Returns:
            float: Wynik podobieństwa Pearsona, gdzie wartości w zakresie [-1, 1] określają siłę i kierunek korelacji.
                   Zwraca 0, jeśli nie ma wspólnych ocen lub gdy nie można obliczyć współczynnika.
        """

    if user1 not in dataset:
        raise TypeError('Cannot find ' + user1 + ' in the dataset')

    if user2 not in dataset:
        raise TypeError('Cannot find ' + user2 + ' in the dataset')

    common_movies = {}

    for item in dataset[user1]:
        if item in dataset[user2]:
            common_movies[item] = 1

    num_ratings = len(common_movies)

    if num_ratings == 0:
        return 0

    user1_sum = np.sum([dataset[user1][item] for item in common_movies])
    user2_sum = np.sum([dataset[user2][item] for item in common_movies])

    user1_squared_sum = np.sum([np.square(dataset[user1][item]) for item in common_movies])
    user2_squared_sum = np.sum([np.square(dataset[user2][item]) for item in common_movies])

    sum_of_products = np.sum([dataset[user1][item] * dataset[user2][item] for item in common_movies])

    Sxy = sum_of_products - (user1_sum * user2_sum / num_ratings)
    Sxx = user1_squared_sum - np.square(user1_sum) / num_ratings
    Syy = user2_squared_sum - np.square(user2_sum) / num_ratings

    if Sxx * Syy == 0:
        return 0

    return Sxy / np.sqrt(Sxx * Syy)


def find_closest_relation(dataset, user, score_func):
    """
        Znajduje najbardziej podobnych użytkowników na podstawie wybranej funkcji podobieństwa.

        Args:
            dataset (dict): Zbiór danych zawierający oceny filmów przez użytkowników.
            user (str): Użytkownik, dla którego szukamy podobieństw.
            score_func (function): Funkcja używana do obliczania podobieństwa (np. euclidean_score lub pearson_score).

        Returns:
            list: Posortowana lista krotek (użytkownik, wynik podobieństwa), zaczynając od najwyższego podobieństwa.
        """

    scores = {}
    for other_user in dataset:
        if other_user != user:
            score = score_func(dataset, user, other_user)
            scores[other_user] = score

    sorted_scores = sorted(scores.items(), key=lambda item: item[1], reverse=True)
    return sorted_scores


def get_recommendations(dataset, user, score_func, num_recommendations=5, num_anti_recommendations=5):
    """
        Generuje listę rekomendacji i antyrekomendacji na podstawie ocen podobnych użytkowników.

        Args:
            dataset (dict): Zbiór danych zawierający oceny filmów przez użytkowników.
            user (str): Użytkownik, dla którego generujemy rekomendacje.
            score_func (function): Funkcja używana do obliczania podobieństwa (euclidean_score lub pearson_score).
            num_recommendations (int, optional): Liczba rekomendacji do zwrócenia. Domyślnie 5.
            num_anti_recommendations (int, optional): Liczba antyrekomendacji do zwrócenia. Domyślnie 5.

        Returns:
            tuple: Dwie listy:
                - Pierwsza lista zawiera rekomendowane filmy.
                - Druga lista zawiera antyrekomendowane filmy.
        """

    closest_relations = find_closest_relation(dataset, user, score_func)

    watched_movies = set(dataset[user].keys())
    recommendations = []
    anti_recommendations = []

    for related_user, score in closest_relations:
        if score <= 0:
            break

        related_user_movies = dataset[related_user]

        sorted_related_movies = sorted(related_user_movies.items(), key=lambda item: item[1], reverse=True)
        for movie, rating in sorted_related_movies:
            if movie not in watched_movies and len(recommendations) < num_recommendations:
                recommendations.append(movie)
                watched_movies.add(movie)

        sorted_related_movies.reverse()
        for movie, rating in sorted_related_movies:
            if movie not in watched_movies and len(anti_recommendations) < num_anti_recommendations:
                anti_recommendations.append(movie)
                watched_movies.add(movie)
            elif len(
                    anti_recommendations) < num_anti_recommendations:
                break

    return recommendations, anti_recommendations
