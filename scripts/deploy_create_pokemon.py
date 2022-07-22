from scripts.helpful_scripts import (
    get_account,
    fund_with_link,
    get_contract
    ) 
from brownie import (
    PokemonFactory,
    config,
    network
)

def deploy_and_create():
    account = get_account()
    pokemon_factory = PokemonFactory.deploy(
        get_contract("vrf_coordinator"),
        get_contract("link_token"),
        config["networks"][network.show_active()]["key_hash"],
        config["networks"][network.show_active()]["fee"],
        {"from":account}
    )

    fund_with_link(pokemon_factory.address)
    creating_tx = pokemon_factory.createPokemon({"from":account})
    creating_tx.wait(1)
    print("New Pokemon has been created!")
    return pokemon_factory, creating_tx


def main():
    deploy_and_create()
    