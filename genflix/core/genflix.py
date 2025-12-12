## Class GenFlix Python File
import random 
from faker import Faker
from ..models.user import User
from ..models.movie import Movie
from ..models.rating import Rating
import pandas as pd
from dataclasses import dataclass, field


@dataclass
class GenFlix:
    flix_genres: list[str] = field(default_factory=lambda: 
                  ['Action', 'Adventure', 'Animation', 'Comedy', 'Drama', 'Fantasy',
                  'Horror', 'Musical', 'Mystery', 'Romance', 'SciFi', 'Thriller', 'Western'], init=False)
    number_of_movies: int = 200
    number_of_users: int = 100
    number_of_ratings: int = 1000
    users: list[User] = field(default_factory=list, init=False)
    movies: list[Movie] = field(default_factory=list, init=False)
    ratings_data_frame: pd.DataFrame = field(default=None, init=False)
    ratings: list[Rating] = field(default_factory=list, init=False)
    faker: Faker = field(default_factory=Faker, init=False)
    restarted: bool = field(default=False, init=False)
    
    def __post_init__(self):
        self.restart_genflix()
        

    def __str__(self):
        return f"Genflix instance has {len(self.users)} users, {len(self.movies)} movies and {len(self.ratings)} ratings in total"

    # Generate Users
    def _generate_users(self) -> None:
        self.users = []       # list of User objects we start with empty list in case we restart GenFlix
        for user_id in range(1, self.number_of_users + 1):
            name = self.faker.name()
            age = random.randint(10, 80)
            preferences = random.sample(self.flix_genres, k=random.randint(1, 5))
            user = User(user_id, name, age, preferences)
            self.users.append(user)

    # Generate Movies
    def _generate_movies(self) -> None:
        self.movies = []      # list of Movie objects we start with empty list in case we restart GenFlix
        for _ in range(self.number_of_movies):
            title = self.faker.sentence(nb_words=3).rstrip('.')
            year = random.randint(1950, 2024)
            genres = set(random.sample(self.flix_genres, k=random.randint(1, 3)))
            movie = Movie(title, genres, year)
            self.movies.append(movie)

    # Generate Ratings - create Rating objects out of movie objects and user objects with the watch history
    def _generate_ratings(self):
        self.ratings = []     # list of Rating objects we start with empty list in case we restart GenFlix
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
                # generate a random date within the last 5 years
                random_datetime = self.faker.date_time_between(start_date="-5y", end_date="now").date()
                # create Rating object
                rating = Rating(
                    user= user,
                    movie= movie,
                    user_rating=user_rating,
                    date=random_datetime,
                    genres=set(movie.genres)
                )
                self.ratings.append(rating)

    # Generate the dataframe out of ratings for easier data manipulation and analysis
    def _generate_dataframe(self)  -> None:
       
        # We need to flatten user and movie attributes into the DataFrame
        for r in self.ratings:
            setattr(r, "user_id", r.user.user_id)
            setattr(r, "user_name", r.user.name)
            setattr(r, "user_age", r.user.age)
            setattr(r, "movie_title", r.movie.title)
            setattr(r, "movie_year", r.movie.year)
        df =  pd.DataFrame([r.__dict__ for r in self.ratings])
        # onehotencoding of genres
        for genre in self.flix_genres:
            df[f"IS_{genre}"] = df['genres'].apply(lambda genres: 1 if genre in genres else 0)
        self.ratings_data_frame = df.drop(columns=['user', 'movie', 'genres'])
        # turning date column into datetime type
        self.ratings_data_frame['date'] = pd.to_datetime(self.ratings_data_frame['date'])
        # Now dataframe is ready for manipulation and analysis
    
    # method for returning data frame
    def get_ratings_dataframe(self) -> pd.DataFrame:
        if self.ratings_data_frame is None or self.restarted is True:
            self._generate_dataframe()
            if self.restarted is True:
                self.restarted = False
        return self.ratings_data_frame
    

    
    # start filling (Generating) own data (fake data) for GenFlix Application to be able to function
    def restart_genflix(self):
        print("""
        ------------------------------------------------------------
                        STARTING GENFLIX DATA GENERATION
        ------------------------------------------------------------
        """)

        print("> Generating movies...")
        self._generate_movies()

        print("> Generating users...")
        self._generate_users()

        print("> Generating ratings...")
        self._generate_ratings()
        self.restarted = True

        print("""
        DATA GENERATION COMPLETED.
        ------------------------------------------------------------
        """)

    

   
    