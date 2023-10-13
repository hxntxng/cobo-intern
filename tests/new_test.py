import pytest
from brownie import accounts, network
from scripts.alienbase import deposit


def test_account_balance():
    balance = accounts[0].balance()
    accounts[0].transfer(accounts[1], "10 ether", gas_price=0)

    assert balance - "10 ether" == accounts[0].balance()
    
network.connect('base-main-fork')
accounts.add()
print(accounts)
print(accounts[0].balance())

print(network.is_connected())



def test_alienbase_deposit():
    acct = accounts[0]
    print(dir(acct))
    acct.transfer(accounts[1], "10 ether", gas_price=0)
    deposit(acct, 5)
    assert accounts[0].balance() == 5

test_alienbase_deposit()