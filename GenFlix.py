## Class GenFlix Python File
import random 
from faker import Faker
from User import User
from Movie import Movie
from Rating import Rating
import pandas as pd
from scipy.cluster.vq import whiten, kmeans, vq
import numpy as np


class GenFlix:
    flix_genres = ['Action', 'Adventure', 'Animation', 'Comedy', 'Drama', 'Fantasy',
                  'Horror', 'Musical', 'Mystery', 'Romance', 'SciFi', 'Thriller', 'Western']
     
    def __init__(self, number_of_users=100, number_of_movies=200, number_of_ratings=1000):
        self.users = []
        self.movies = []
        self.ratings_data_frame = None
        self.ratings = []
        self.faker = Faker()
        self.number_of_users = number_of_users
        self.number_of_movies = number_of_movies
        self.number_of_ratings = number_of_ratings


    # Generate Users
    def generate_users(self):
       
        for user_id in range(1, self.number_of_users + 1):
            name = self.faker.name()
            age = random.randint(10, 80)
            preferences = random.sample(GenFlix.flix_genres, k=random.randint(1, 5))
            user = User(user_id, name, age, preferences)
            self.users.append(user)

    # Generate Movies
    def generate_movies(self):
        for _ in range(self.number_of_movies):
            title = self.faker.sentence(nb_words=3).rstrip('.')
            year = random.randint(1950, 2024)
            genres = random.sample(self.flix_genres, k=random.randint(1, 3))
            movie = Movie(title, genres, year)
            self.movies.append(movie)
    # Generate Ratings - create Rating objects out of movie objects and user objects with the watch history
    def generate_ratings(self):
        ratings_counter = 0
        while ratings_counter < self.number_of_ratings:
            user = random.choice(self.users)
            movie = random.choice(self.movies)
            user_rating = random.randint(1, 5)
            #populate user's watch history if it's not including the movie and rating yet
            if not any(entry["movie"] == movie.title for entry in user.watch_history):
                user.watch_history.append({
                    "movie": movie.title,
                    "rating": user_rating
                })
                ratings_counter += 1
                # create Rating object
                rating = Rating(
                    user_name=user.name,
                    user_age=user.age,
                    user_id=user.id,
                    movie_title=movie.title,
                    movie_year=movie.year,
                    IS_Action=1 if 'Action' in movie.genres else 0,
                    IS_Adventure=1 if 'Adventure' in movie.genres else 0,
                    IS_Animation=1 if 'Animation' in movie.genres else 0,
                    IS_Comedy=1 if 'Comedy' in movie.genres else 0,
                    IS_Drama=1 if 'Drama' in movie.genres else 0,
                    IS_Fantasy=1 if 'Fantasy' in movie.genres else 0,
                    IS_Horror=1 if 'Horror' in movie.genres else 0,
                    IS_Musical=1 if 'Musical' in movie.genres else 0,
                    IS_Mystery=1 if 'Mystery' in movie.genres else 0,
                    IS_Romance=1 if 'Romance' in movie.genres else 0,
                    IS_SciFi=1 if 'SciFi' in movie.genres else 0,
                    IS_Thriller=1 if 'Thriller' in movie.genres else 0,
                    IS_Western=1 if 'Western' in movie.genres else 0,
                    user_rating=user_rating
                )
                self.ratings.append(rating)

    # Do Recommendation of movies to users based on Consumption of earlier movies using Kmeans algorithm
    def recommend_movies_to_user(self, user_id, n=5):
        df = self.ratings_data_frame
        df_users = df.groupby("user_id").agg({
                    "user_age": "first",
                    "IS_Action": "mean",    # average user perception
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

        X_users = df_users.to_numpy()
        X_users_whitened = whiten(X_users)

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
            .head(n)
        )
        
        return recommended["movie_title"].tolist()

    
    # do reccomendation of movies to users based on Movies Clustering using K-Means algorithm
    def recommend_similar_movies(self, movie_title, n=5):
        df = self.ratings_data_frame
        df_movies = df.groupby("movie_title").agg({
                    "movie_year": "first",
                    "IS_Action": "mean",    # average user perception
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

        centroids, dist = kmeans(X_movies_whitened, 5)
        labels, _ = vq(X_movies_whitened, centroids)

        df_movies["cluster"] = labels

        movie_cluster = df_movies[df_movies["movie_title"] == movie_title]["cluster"].iloc[0]
        cluster_movies = df_movies[df_movies["cluster"] == movie_cluster]
        if len(cluster_movies) <= n:
            if len(cluster_movies) == 0:
                return []
            return cluster_movies["movie_title"].tolist()
        return cluster_movies.sample(n)
       
    # start filling (Generating) own data (fake data) for GenFlix Application to be able to function
    def Start_Genflix(self):
        print("Starting GenFlix Data Generation...")
        print("Generating Movies...")
        self.generate_movies()
        print("Generating Users...")
        self.generate_users()
        print("Generating Ratings...")
        self.generate_ratings()
        print("Generating Ratings DataFrame...")
        self.ratings_data_frame = pd.DataFrame([r.__dict__ for r in self.ratings])
        print("Data Generation Completed.")
