## User Class for GenFlix Application
from pprint import pprint 

class User:
    def __init__(self, user_id, name, age, preferences):
        self.user_id = user_id
        self.name = name
        self.age = age
        self.preferences = preferences ## list of Genres that the user prefers to watch
        self.watch_history = []
    
    def __str__(self):
        return f"User: {self.name}, ID: {self.user_id}"

    def __repr__(self):
        return str(self)
    
    def print_details(self):
        print(self)
        print("Preferences: ")
        pprint(self.preferences)
        print("Watch History: ")
        pprint(self.watch_history)