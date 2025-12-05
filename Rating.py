

class Rating:
    def __init__(self, user_name, user_age, user_id, movie_title, movie_year, IS_Action, IS_Adventure, 
                 IS_Animation, IS_Comedy, IS_Drama, IS_Fantasy,
                 IS_Horror, IS_Musical, IS_Mystery, IS_Romance, IS_SciFi, IS_Thriller, IS_Western,
                 user_rating, date):
        self.user_name = user_name
        self.movie_title = movie_title
        self.movie_year = movie_year
        self.user_age = user_age
        self.user_id = user_id
        self.IS_Action = IS_Action
        self.IS_Adventure = IS_Adventure
        self.IS_Animation = IS_Animation
        self.IS_Comedy = IS_Comedy
        self.IS_Drama = IS_Drama
        self.IS_Fantasy = IS_Fantasy
        self.IS_Horror = IS_Horror
        self.IS_Musical = IS_Musical
        self.IS_Mystery = IS_Mystery
        self.IS_Romance = IS_Romance
        self.IS_SciFi = IS_SciFi
        self.IS_Thriller = IS_Thriller
        self.IS_Western = IS_Western
        self.user_rating = user_rating
        self.date = date

    def __str__(self):
        return f"Rating on {self.date}, by {self.user_name} (ID: {self.user_id}, Age: {self.user_age}) for '{self.movie_title}' ({self.movie_year}): {self.user_rating}/5"
    def __repr__(self):
        return str(self)
    