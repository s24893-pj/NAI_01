import pandas as pd
import json
from sklearn.cluster import KMeans

file_path = 'ratings.json'
with open(file_path, 'r') as file:
    data = json.load(file)
ratings_df = pd.DataFrame(data).T.fillna(0)


def cluster_users_and_recommend(user_name, ratings_df, n_clusters=3, top_n=5, anti_n=5):
    """
        Klasteryzuje użytkowników na podstawie ich ocen i generuje rekomendacje.

        Args:
            user_name (str): Nazwa użytkownika, dla którego generujemy rekomendacje.
            ratings_df (pd.DataFrame): DataFrame z ocenami użytkowników.
            n_clusters (int, optional): Liczba klastrów. Domyślnie 2.
            top_n (int, optional): Liczba rekomendacji do zwrócenia. Domyślnie 5.
            anti_n (int, optional): Liczba antyrekomendacji do zwrócenia. Domyślnie 5.

        Returns:
            tuple: Dwie listy:
                - Pierwsza lista zawiera tytuły rekomendowanych filmów.
                - Druga lista zawiera tytuły antyrekomendowanych filmów.
        """

    kmeans = KMeans(n_clusters=n_clusters, random_state=0)
    ratings_df['cluster'] = kmeans.fit_predict(ratings_df)

    user_cluster = ratings_df.loc[user_name, 'cluster']

    similar_users = ratings_df[ratings_df['cluster'] == user_cluster]
    user_movies = ratings_df.loc[user_name][ratings_df.loc[user_name] > 0].index

    recommendations = {}
    anti_recommendations = {}

    for other_user in similar_users.index:
        if other_user == user_name:
            continue

        other_user_movies = ratings_df.loc[other_user][ratings_df.loc[other_user] > 0].index
        unseen_movies = set(other_user_movies) - set(user_movies)

        for movie in unseen_movies:
            rating = ratings_df.loc[other_user, movie]
            if rating >= 7:
                recommendations[movie] = recommendations.get(movie, 0) + rating
            elif rating <= 4:
                anti_recommendations[movie] = anti_recommendations.get(movie, 0) + rating

    sorted_recommendations = sorted(recommendations.items(), key=lambda x: -x[1])[:top_n]
    sorted_anti_recommendations = sorted(anti_recommendations.items(), key=lambda x: x[1])[:anti_n]

    return [movie for movie, _ in sorted_recommendations], [movie for movie, _ in sorted_anti_recommendations]
