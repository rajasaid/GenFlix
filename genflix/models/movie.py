## This is Movie class Python file
from dataclasses import dataclass, field

@dataclass
class Movie:
    title: str
    genres: set[str] = field(default_factory=set)
    year: int = 2020

    def __str__(self):
        return f"Movie '{self.title}' - Year {self.year}\n Genres: {', '.join(self.genres)}"
    
    


        