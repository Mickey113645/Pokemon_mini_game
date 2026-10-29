import requests 
import json

def fetch_pokemon(poke_id):
    url=f"https://pokeapi.co/api/v2/pokemon/{poke_id}"
    response = requests.get(url,timeout=10)
    data = response.json()

    stats = {}

    for entry in data["stats"]:
        name = entry["stat"]["name"]
        value = entry["base_stat"]
        name = name.replace("-","_")
        stats[name] = value

    types = data["types"]
    type1 = types[0]["type"]["name"]

    if len(types) == 2:
        type2 = types[1]["type"]["name"]
    else:
        type2 = None

    pokemon = {
        "id": data["id"],
        "name": data["name"],
        "sprite": data["sprites"]["front_default"],
            "hp": stats["hp"],
            "attack": stats["attack"],
            "defense": stats["defense"],
            "special_attack": stats["special_attack"],
            "special_defense": stats["special_defense"],
            "speed": stats["speed"],
            "type1": type1,
            "type2": type2,
    }
    return pokemon

all_poke=[]
for i in range(1,152,1):
    poke=fetch_pokemon(i)
    all_poke.append(poke)

print(len(all_poke))

with open("pokemon.json","w") as poke_file:
    json.dump(all_poke,poke_file)