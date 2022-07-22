from brownie import PokemonFactory, network 
from scripts.helpful_scripts import (
    get_pokemon
)
from metadata.sample_metada import metadata_template
from pathlib import Path
import os
import json
import requests
pokemon_to_image_uri = {
   "CATERPIE" : "https://ipfs.io/ipfs/QmdzjgkMFFxAj6npzqdsTGpKz67sCPfXqJHZEFwyzrcmgU?filename=c",
    "CHARMANDER":"https://ipfs.io/ipfs/QmPdRCb7Q7nTYeKCxdPZ9SCaxQH5FkhabRRmvd62XVfoRY?filename=c"
}
def main():
    pokemon_factory = PokemonFactory[-1]
    number_of_pokemon = pokemon_factory.tokenCounter()
    print(f"You have created {number_of_pokemon} pokemons !")
    for token_id in range(number_of_pokemon):
        pokemon = get_pokemon(pokemon_factory.tokenIdToPokemon(token_id))
        metadata_file_name = (
            f"./metadata/{network.show_active()}/{token_id}-{pokemon}.json"
        )
        pokemon_metadata = metadata_template
        if Path(metadata_file_name).exists():
            print(f"{metadata_file_name} already exists! Delete it to overwrite it.")
        else:
            print(f"Creating Metadata file: {metadata_file_name}")
            pokemon_metadata["name"] = pokemon
            pokemon_metadata["description"] = f"{pokemon} that can generate powerful electricity have cheek sacs that are extra soft and super stretchy.!"
            image_path = "./img/" + pokemon.lower().replace("_", "-") + ".png"
            image_uri = None
            print(os.getenv("UPLOAD_IPFS"))
            if os.getenv("UPLOAD_IPFS") == "true":
                image_uri = upload_to_ipfs(image_path)
            image_uri = image_uri if image_uri else pokemon_to_image_uri[pokemon]

            pokemon_metadata["image"] = image_uri
            with open(metadata_file_name, "w") as file:
                json.dump(pokemon_metadata, file)
            if os.getenv("UPLOAD_IPFS") == "true":
                upload_to_ipfs(metadata_file_name)


def upload_to_ipfs(filepath):
    with Path(filepath).open("rb") as fp:
        image_binary = fp.read()
        ipfs_url = "http://127.0.0.1:5001"
        endpoint = "/api/v0/add"
        response = requests.post(ipfs_url + endpoint, files={"file": image_binary})
        ipfs_hash = response.json()["Hash"]
        # "./img/0-PUG.png" -> "0-PUG.png"
        filename = filepath.split("/")[-1][0]
        image_uri = f"https://ipfs.io/ipfs/{ipfs_hash}?filename={filename}"
        print(image_uri)
        return image_uri
