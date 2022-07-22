from brownie import (
    accounts,
    network,
    config,
    Contract,
    LinkToken,
    VRFCoordinatorMock,
)
from web3 import Web3

POKEMON_MAPPING = {
    0: "BULBASAUR",
    1: "CHARMANDER",
    2: "SQUIRTLE",
    3:  "CATERPIE",
    4:  "WEEDLE",
    5: "PIDGEY",
    6: "RATTATA",
    7: "SPEAROW",
    8: "EKANS",
    9:  "PIKACHU",
    10: "SANDSHREW"
}

LOCAL_BLOCKCHAIN_ENVIROMENTS = [
    "development",
    "mainnet-fork",
    "mainnet-fork-dev",
]

def get_account(index=None, id= None):
    if index:
        return accounts[index]
    if id:
        return accounts.load(id)
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIROMENTS:
        return accounts[0]
    return accounts.add(config["wallets"]["from_key"])

contract_to_mock = {"link_token": LinkToken, "vrf_coordinator": VRFCoordinatorMock}

def get_contract(contract_name):
    contract_type = contract_to_mock[contract_name]
    contract_address = config["networks"][network.show_active()][contract_name]
    contract = Contract.from_abi(
        contract_type._name, contract_address, contract_type.abi
    )
    return contract

def fund_with_link(
    contract_address, account = None, link_token = None, amount = Web3.toWei(0.2, "ether")
):
    account = account if account else get_account()
    link_token = link_token if link_token else get_contract("link_token")
    funding_tx = link_token.transfer(contract_address, amount, {"from": account})
    funding_tx.wait(1)
    print(f"Funded {contract_address}")
    return funding_tx


def get_pokemon(pokemon_number):
    return POKEMON_MAPPING[pokemon_number]