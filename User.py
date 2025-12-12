## User Class for GenFlix Application
from pprint import pprint 
from dataclasses import dataclass, field

@dataclass
class User:
    user_id: int
    name: str
    age: int
    preferences: list[str] = field(default_factory=list)
    watch_history: list[dict] = field(default_factory=list, init=False) # list of dicts with 'movie' and 'rating' keys

    def __str__(self):
        return f"User: {self.name}, ID: {self.user_id}"

    def print_details(self):
        print(self)
        print("Preferences: ")
        pprint(self.preferences)
        print("Watch History: ")
        pprint(self.watch_history)