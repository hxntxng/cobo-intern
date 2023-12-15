from brownie import accounts
from scripts import alienbase, compound_v3


def test_alienbase_deposit():
    acct = accounts[0]
    val = 5
    alienbase.withdraw(acct)
    alienbase.deposit(acct, val)
    assert alienbase.get_val(acct) == val

def test_alienbase_withdraw():
    acct = accounts[0]
    alienbase.withdraw(acct)
    assert alienbase.get_val(acct) == 0

def test_compound_deposit():
    acct = accounts[0]
    val = 5
    compound_v3.withdraw_collateral(acct)
    x = compound_v3.deposit_collateral(acct, val)
    assert x == compound_v3.get_collateral_val(acct)

def test_compound_withdraw():
    acct = accounts[0]
    compound_v3.withdraw_collateral(acct)
    assert compound_v3.get_collateral_val(acct) == 0

def test_alienbase_get_val():
    acct = accounts[0]
    assert alienbase.get_val(acct) == 0

def test_compound_get_val():
    acct = accounts[0]
    compound_v3.withdraw_collateral(acct)
    assert compound_v3.get_collateral_val(acct) == 0
