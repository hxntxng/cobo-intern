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
    print('accounts', accounts, len(accounts))    
    for i, acct in enumerate(accounts):
        print(f'account {i}: address {acct.address}, balance {acct.balance()}')
        print(type(acct), type(acct).__bases__)
    print(web3._chain_id)
    acct = accounts[10]
    print('acct', acct)
    # breakpoint()
    print("AAAA")
    a_deposit(web3, acct, 5)
    assert a_get_val(web3, acct) == 5

# test_alienbase_deposit()
