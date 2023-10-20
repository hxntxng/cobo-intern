import pytest
from brownie import accounts, network, web3
from scripts.alienbase import a_deposit, a_get_val, a_withdraw
from scripts.compound import c_deposit, c_get_val, c_withdraw


# def test_account_balance():
#     account = get_account()

#     acct1_balance = accounts[0].balance()
#     print(acct1_balance)
#     accounts[0].transfer(accounts[1], "10 ether", gas_price=1000000, gas_limit=100000)
#     assert acct1_balance + 10 * 10**18 == accounts[1].balance()


def test_alienbase_deposit():
    accounts.add()
    accounts[0].transfer(accounts[10], "10 ether", gas_price = 1000000, gas_limit=100000)
    print(web3.chain_id)
    acct = accounts[10]
    val = 5
    a_deposit(web3, acct, val)
    assert a_get_val(web3, acct) == val

def test_alienbase_withdraw():
    accounts.add()
    accounts[0].transfer(accounts[10], "10 ether", gas_price = 1000000, gas_limit=100000)
    acct = accounts[10]
    bal = acct.balance()
    val = a_get_val(web3, acct)
    a_withdraw(web3, acct)
    assert bal + val == acct.balance()
    assert a_get_val(web3, acct) == 0

def test_compound_deposit():
    accounts.add()
    accounts[0].transfer(accounts[10], "10 ether", gas_price = 1000000, gas_limit=100000)
    acct = accounts[10]
    val = 5
    c_deposit(web3, acct, val)
    assert c_get_val(web3, acct) == val

def test_compound_withdraw():
    accounts.add()
    accounts[0].transfer(accounts[10], "10 ether", gas_price = 1000000, gas_limit=100000)
    acct = accounts[10]
    bal = acct.balance()
    val = c_get_val(web3, acct)
    c_withdraw(web3, acct)
    assert bal + val == acct.balance()
    assert c_get_val(web3, acct) == 0

def test_alienbase_get_val():
    accounts.add()
    accounts[0].transfer(accounts[10], "10 ether", gas_price = 1000000, gas_limit=100000)
    acct = accounts[10]
    assert a_get_val(web3, acct) == 0

def test_compound_get_val():
    accounts.add()
    accounts[0].transfer(accounts[10], "10 ether", gas_price = 1000000, gas_limit=100000)
    acct = accounts[10]
    assert c_get_val(web3, acct) == 0


# test_alienbase_deposit()
