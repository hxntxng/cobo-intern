import pytest
from brownie import accounts, network, web3
from scripts.alienbase import a_deposit, a_get_val, a_withdraw
from scripts import compound

# def test_account_balance():
#     account = get_account()
#     acct1_balance = accounts[0].balance()
#     print(acct1_balance)
#     accounts[0].transfer(accounts[1], "10 ether", gas_price=1000000, gas_limit=100000)
#     assert acct1_balance + 10 * 10**18 == accounts[1].balance()


# def test_alienbase_deposit():
#     accounts.add()
#     accounts[0].transfer(accounts[10], "10 ether", gas_price = 1000000, gas_limit=100000)
#     acct = accounts[10]
#     val = 5
#     a_deposit(acct, val)
#     assert a_get_val(acct) == val

# def test_alienbase_withdraw():
#     accounts.add()
#     accounts[0].transfer(accounts[10], "10 ether", gas_price = 1000000, gas_limit=100000)
#     acct = accounts[10]
#     bal = acct.balance()
#     val = a_get_val(acct)
#     a_withdraw(acct)
#     assert bal + val == acct.balance()
#     assert a_get_val(acct) == 0

def test_compound_deposit():
    # accounts.add('0x39f39b237d9339d47c00327dbb4c24cb45076cefa2b7b6bc0da55649fea09410')
    # print(accounts[0].address)
    # accounts[0].transfer(accounts[10], "10 ether", gas_price = 1000000, gas_limit=100000)
    acct = accounts[3]
    val = 5
    x = compound.deposit(acct, val)
    # print(x)
    assert x == compound.get_val(acct)

# def test_compound_withdraw():
#     accounts.add()
#     accounts[0].transfer(accounts[10], "10 ether", gas_price = 1000000, gas_limit=100000)
#     acct = accounts[10]
#     bal = acct.balance()
#     val = c_get_val(acct)
#     c_withdraw(acct)
#     assert bal + val == acct.balance()
#     assert c_get_val(acct) == 0

# def test_alienbase_get_val():
#     accounts.add()
#     accounts[0].transfer(accounts[10], "10 ether", gas_price = 1000000, gas_limit=100000)
#     acct = accounts[10]
#     assert a_get_val(acct) == 0

def test_compound_get_val():
    # accounts.add()
    # accounts[0].transfer(accounts[10], "10 ether", gas_price = 1000000, gas_limit=100000)
    # accounts.add('0x927cf46765031e17b33d0553b7f38d2bede8563b31cf3aa5a2fb10d474cd32fa')
    acct = accounts[4]
    assert compound.get_val(acct) == 0
