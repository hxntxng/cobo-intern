import pytest
from brownie import accounts, network
from scripts.alienbase import deposit

def test_account_balance():
<<<<<<< HEAD
    balance = accounts[0].balance()
    accounts[0].transfer(accounts[1], "10 ether", gas_price=0)
    assert balance - "10 ether" == accounts[0].balance()
    
network.connect('base-main-fork')
print(accounts)
print(accounts[0].balance())

print(network.is_connected())



# def test_alienbase_deposit():
#     acct = accounts[0]
#     print(dir(acct))
#     acct.transfer(accounts[1], "10 ether", gas_price=0)
#     deposit(acct, 5)
#     assert accounts[0].balance() == 5
=======
    acct1_balance = accounts[1].balance()
    accounts[0].transfer(accounts[1], "10 ether", gas_price=1000000, gas_limit=100000)
    assert acct1_balance + 10 * 10**18 == accounts[1].balance()


def test_alienbase_deposit():
    acct = accounts[0]
    #breakpoint()
    acct.transfer(accounts[1], "10 ether", gas_price=1000000, gas_limit=100000)
    #deposit(acct, 5)
    #assert accounts[0].balance() == 5
>>>>>>> 43ae2c039169ac61d42ea78f9bb1de86ebf16126
