## This is GenFlixService class Python file

from .genflix import GenFlix
from ..models.user import User
from ..models.movie import Movie
import numpy as np
from scipy.cluster.vq import kmeans, vq, whiten
import pandas as pd

class GenFlixService:
    def __init__(self, genflix: GenFlix) -> None:
        self.genflix = genflix

    def restart(self) -> None:
        self.genflix.restart_genflix()

    def get_ratings_dataframe(self) -> pd.DataFrame:
        return self.genflix.get_ratings_dataframe()
    
    def get_user_name(self, user_id: int) -> str:
        if user_id < 1 or user_id > len(self.genflix.users):
            raise ValueError("User ID out of range")
        user = self.genflix.users[user_id - 1]
        return user.name

    def find_movie_data(self) -> str:
        while True:
            movie_input = input("\nEnter movie title: ").strip()
            query = movie_input.lower()

            matches = [
                movie for movie in self.genflix.movies
                if movie.title.lower() == query
            ]

            if matches:
                movie = matches[0]
                self.print_movie_info(movie)
                return movie.title

            print("❌ No movie found with that title. Please try again.")
    
    def find_user_data(self) -> int:
        while True:
            user_input = input(f"Enter user name or user id (1–{len(self.genflix.users)}): ").strip()

            # user entered an integer (ID search)
            try:
                user_id = int(user_input)

                if 1 <= user_id <= len(self.genflix.users):
                    user = self.genflix.users[user_id - 1]
                    self.print_user_info(user)
                    return user_id
                else:
                    print("❌ ID out of range, try again.")
                    continue

            except ValueError:
                # not an integer → treat as name
                pass

            # user entered a name (string search)
            name_search = user_input.lower()
            matches = [user for user in self.genflix.users if user.name.lower() == name_search]

            if matches:
                user = matches[0]
                from menu import print_user_info
                print_user_info(user)
                return user.user_id

            print("❌ No user found with that name or ID. Try again.")
    
    # do recommendation of movies to users based on Movies Clustering using K-Means algorithm
    def recommend_similar_movies(self, movie_title: str, num_recommendations: int) -> list[str]:
        df = self.genflix.get_ratings_dataframe()
        df_movies = df.groupby("movie_title").agg({
                    "movie_year": "first",
                    "IS_Action": "mean",    
                    "IS_Comedy": "mean",
                    "IS_Drama": "mean",
                    "IS_Romance": "mean",
                    "IS_SciFi": "mean",
                    "IS_Thriller": "mean",
                    "IS_Adventure": "mean",
                    "IS_Animation": "mean",
                    "IS_Fantasy": "mean",
                    "IS_Horror": "mean",
                    "IS_Musical": "mean",
                    "IS_Mystery": "mean",
                    "IS_Western": "mean",
                    "user_rating": "mean"
                }).reset_index()

        X_movies = df_movies.drop(columns=["movie_title"]).to_numpy()
        X_movies_whitened = whiten(X_movies)

        np.random.seed(42) # certain results reproducibility
        centroids, dist = kmeans(X_movies_whitened, 5)
        labels, _ = vq(X_movies_whitened, centroids)

        df_movies["cluster"] = labels

        movie_cluster = df_movies[df_movies["movie_title"] == movie_title]["cluster"].iloc[0]
        cluster_movies = df_movies[df_movies["cluster"] == movie_cluster].sort_values("user_rating", ascending=False)
        cluster_movies = cluster_movies[cluster_movies["movie_title"] != movie_title]
        if len(cluster_movies) <= num_recommendations:
            if len(cluster_movies) == 0:
                return []
            return cluster_movies["movie_title"].tolist()
        return cluster_movies.head(num_recommendations)["movie_title"].tolist()
    
    # Do Recommendation of movies to users based on Consumption of earlier movies using Kmeans algorithm
    def recommend_movies_to_user(self, user_id : int, num_recommendations: int = 5) -> list[str]:
        df = self.genflix.get_ratings_dataframe()
        df_users = df.groupby("user_id").agg({
                    "user_age": "first",
                    "IS_Action": "mean",    
                    "IS_Comedy": "mean",
                    "IS_Drama": "mean",
                    "IS_Romance": "mean",
                    "IS_SciFi": "mean",
                    "IS_Thriller": "mean",
                    "IS_Adventure": "mean",
                    "IS_Animation": "mean",
                    "IS_Fantasy": "mean",
                    "IS_Horror": "mean",
                    "IS_Musical": "mean",
                    "IS_Mystery": "mean",
                    "IS_Western": "mean",
                    "user_rating": "mean"
                })

        X_users = df_users.to_numpy()
        X_users_whitened = whiten(X_users)

        np.random.seed(45)  # certain results reproducibility
        centroids, dist = kmeans(X_users_whitened, 5) ## number of clusters = 5 as number of rate scale 1-5
        labels, _ = vq(X_users_whitened, centroids)

        df_users["cluster"] = labels
        df_with_clusters = df.merge(
            df_users["cluster"],
            left_on="user_id",
            right_index=True
        )
        top_movies_by_cluster = (
            df_with_clusters
            .groupby(["cluster", "movie_title"])["user_rating"]
            .mean()
            .reset_index()
            )

            # Find this user's cluster
        cluster = df_users.loc[user_id, "cluster"]
        
        # Get that cluster's movies
        cluster_movies = top_movies_by_cluster[
            top_movies_by_cluster["cluster"] == cluster
        ]
        
        # Sort by highest rating
        recommended = (
            cluster_movies
            .sort_values("user_rating", ascending=False)
            .head(num_recommendations)
        )
        
        return recommended["movie_title"].tolist()
    def print_user_info(self, user : User)  -> None:
        print(r"""
    ┌────────────────────────────────────────────────────────────┐
    │                         USER DETAILS                       │
    └────────────────────────────────────────────────────────────┘
    """)

        print(f"  ID:          {user.user_id}")
        print(f"  Name:        {user.name}")
        print(f"  Age:         {user.age}")

        print("\n  Preferences:")
        print("  ------------")
        for genre in user.preferences:
            print(f"   • {genre}")

        print("\n  Watch History:")
        print("  --------------")
        if not user.watch_history:
            print("   (no movies watched yet)")
        else:
            for entry in user.watch_history:
                movie_title = entry["movie"]
                rating = entry["rating"]
                print(f"   • {movie_title} — rated {rating}/5")

        print("\n──────────────────────────────────────────────────────────────\n")

    def print_movie_info(self, movie: Movie)  -> None:
        print(r"""
    ┌────────────────────────────────────────────────────────────┐
    │                         MOVIE DETAILS                      │
    └────────────────────────────────────────────────────────────┘
    """)

        print(f"  Title:       {movie.title}")
        print(f"  Year:        {movie.year}")

        print("\n  Genres:")
        print("  --------")
        for genre in movie.genres:
            print(f"   • {genre}")

        print("\n──────────────────────────────────────────────────────────────\n")