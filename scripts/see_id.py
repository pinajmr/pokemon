from brownie import PokemonFactory


def see():
    pokemon_factory = PokemonFactory[-1]
    print(pokemon_factory.tokenCounter())
    print(pokemon_factory.tokenIdToPokemon(1))


def main():
    see()