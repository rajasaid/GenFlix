from .core.genflix import GenFlix
from .core.service import GenFlixService

from .plotting.ratings_graphs import GraphGenerator
from .plotting.user_graphs import UserGraphGenerator

from .models.user import User
from .models.movie import Movie
from .models.rating import Rating

from .ui.menu import initiate_genflix