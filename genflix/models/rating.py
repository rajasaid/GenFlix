# Rating class Python file
from dataclasses import dataclass, field
from ..models.user import User
from ..models.movie import Movie
import datetime

@dataclass
class Rating:
    user: User = field(repr=False)
    movie: Movie = field(repr=False)
    user_rating: float
    date: datetime.date
    genres: set[str] = field(default_factory=set)

    def __str__(self):
        return f"Rating on {self.date}, by {self.user.user_name} (ID: {self.user.user_id}, Age: {self.user.user_age}) for '{self.movie.movie_title}' ({self.movie.movie_year}): {self.user_rating}/5"
    