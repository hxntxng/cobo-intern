from web3 import Web3, HTTPProvider
from dotenv import load_dotenv
from brownie import *
import os
from . import abi
import binascii
load_dotenv()

# w3 = Web3(HTTPProvider(os.getenv("network_key")))
def c_deposit(w3, acct, val):
    chainId=1337
    nonce = w3.eth.get_transaction_count(acct.address)
    cWETH_address = '0x46e6b214b524310239732D51387075E0e70970bf'
    cWETH_abi = abi.cWETH_abi
    cWETH_contract = Contract.from_abi("CometExt", address = cWETH_address, abi = cWETH_abi)
    base_bulk_address = '0x78D0677032A35c63D142a48A2037048871212a8C'
    allowed = True
    cWETH_contract.allow(base_bulk_address, allowed, {"from": acct})
    # allow_cWETH_signtxn = w3.eth.account.sign_transaction(allow_cWETH_txn, private_key = acct.private_key)
    # w3.eth.send_raw_transaction(allow_cWETH_signtxn.rawTransaction)
    base_bulk_abi = abi.compound_base_bulk_abi
    base_bulk_contract = Contract.from_abi("BaseBulker", address = base_bulk_address, abi = base_bulk_abi)
    deposit_action = '0x414354494f4e5f535550504c595f4e41544956455f544f4b454e000000000000'
    data =  '0x00000000000000000000000046e6b214b524310239732d51387075e0e70970bf0000000000000000000000000f25496cf87be88c0a352d822c4ba92479f536010000000000000000000000000000000000000000000000000001c6bf52634000'
    base_bulk_contract.invoke(deposit_action, data, {"from": acct, "value": acct.balance/2})
    # invoke_bulker_signtxn = w3.eth.account.sign_transaction(invoke_bulker_txn, private_key = acct.private_key)
    # w3.eth.send_raw_transaction(invoke_bulker_signtxn.rawTransaction)
    return

def c_get_val(w3, acct):
    implement_contract_address = '0x46e6b214b524310239732D51387075E0e70970bf'
    implement_contract_abi = abi.compound_implement_abi 
    implement_contract = Contract.from_abi("BaseBulker", implement_contract_address, implement_contract_abi)
    val = implement_contract.balanceOf.call(acct.address, {"from": acct}) # how to put val into data?
    return val

def c_withdraw(w3, acct):
    chainId=1337
    base_bulk_address = '0x78D0677032A35c63D142a48A2037048871212a8C'
    base_bulk_abi = abi.compound_base_bulk_abi
    base_bulk_contract = Contract.from_abi("BaseBulker", address = base_bulk_address, abi = base_bulk_abi)
    val = c_get_val(w3, acct)
    withdraw_action = b'0x414354494f4e5f57495448445241575f4e41544956455f544f4b454e00000000'.ljust(32, b'\0')[:32]
    data = b'0x00000000000000000000000046e6b214b524310239732d51387075e0e70970bf0000000000000000000000000f25496cf87be88c0a352d822c4ba92479f53601ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff'
    base_bulk_contract.invoke(withdraw_action, data, {"from": acct, "value": val})
    # invoke_bulker_signtxn = w3.eth.account.sign_transaction(invoke_bulker_txn, private_key = acct.private_key)
    # w3.eth.send_raw_transaction(invoke_bulker_signtxn.rawTransaction)
    return