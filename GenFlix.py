## Class GenFlix Python File
import random 
from faker import Faker
from User import User
from Movie import Movie
from Rating import Rating
import pandas as pd


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


    # start filling it's own data
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
