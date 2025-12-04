## This is Movie class Python file

class Movie:
    def __init__(self, title, genres, year):
        self.title = title
        self.genres = genres   ## list of the genres of the Movie
        self.year = year
        ## TBD think of average rating for the movie. 
    
    def __str__(self):
        return f"Movie '{self.title}' - Year {self.year}\n Genres: {', '.join(self.genres)}"
    
    def __repr__(self):
        return str(self)
    


        