import json

with open("bestiary-mm.json", "r", encoding="utf-8") as file:
    bestiary = json.load(file)

print(list(bestiary.items())[0])