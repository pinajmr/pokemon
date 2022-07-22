from scripts.helpful_scripts import (
    fund_with_link,
    get_account,
)

from brownie import PokemonFactory
from web3 import Web3 


def main():
    account = get_account()
    pokemon_factory = PokemonFactory[-1]
    fund_with_link(pokemon_factory.address, amount=Web3.toWei(0.1, "ether"))
    creation_transaction = pokemon_factory.createPokemon({"from": account})
    creation_transaction.wait(1)
    print("New pokemon is created!")
