import pickle
import os


class Character:
    def __init__(self, character_class, character_race):
        self.character_class = character_class
        self.character_race = character_race

    def save_character(self):
        file_name = "character.pkl"
        with open(file_name, "wb") as file:
            pickle.dump(self, file)
        print(f"Character saved to {os.path.abspath(file_name)}")
