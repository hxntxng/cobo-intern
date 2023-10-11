from web3 import Web3, HTTPProvider
from dotenv import load_dotenv
import abi
load_dotenv()

def deposit(acct, val):
    nonce = w3.eth.get_transaction_count(acct.address)
    compound_proxy_address = '0x46e6b214b524310239732d51387075e0e70970bf'
    compound_proxy_abi = abi.compound_proxy_abi
    proxy_contract = w3.eth.contract(address = compound_proxy_abi, abi = compound_proxy_abi)
    base_bulk_address = '0x78D0677032A35c63D142a48A2037048871212a8C'
    allowed = true
    allow_proxy_txn = allow_contract.functions.allow(base_bulk_address, allowed)
    allow_proxy_signtxn = w3.eth.account.sign_transaction(allow_proxy_txn, private_key = acct._private_key)
    # w3.eth.send_raw_transaction(allow_proxy_signtxn.rawTransaction)
    base_bulk_abi = abi.compound_base_bulk_abi
    base_bulk_contract = w3.eth.contract(address = base_bulk_address, abi = base_bulk_abi)
    deposit_action = '0x414354494f4e5f535550504c595f4e41544956455f544f4b454e000000000000'
    data =  '0x00000000000000000000000046e6b214b524310239732d51387075e0e70970bf0000000000000000000000000f25496cf87be88c0a352d822c4ba92479f536010000000000000000000000000000000000000000000000000001c6bf52634000'
    invoke_bulker_txn = base_bulk_abi.functions.invoke(deposit_action, data)
    invoke_bulker_signtxn = w3.eth.account.sign_transaction(invoke_bulker_txn, private_key = acct._private_key)
    # w3.eth.send_raw_transaction(invoke_bulker_signtxn.rawTransaction)

def withdraw(acct):
    base_bulk_address = '0x78D0677032A35c63D142a48A2037048871212a8C'
    base_bulk_abi = abi.compound_base_bulk_abi
    base_bulk_contract = w3.eth.contract(address = base_bulk_address, abi = base_bulk_abi)
    implement_contract_address = '0x46e6b214b524310239732D51387075E0e70970bf'
    implement_contract_abi = abi.compound_implement_abi
    implement_contract = w3.eth.contract(address = implement_contract_address, abi = implement_contract_abi)
    val = implement_contract.functions.getBalance(acct) # how to put val into data?
    withdraw_action = '0x414354494f4e5f57495448445241575f4e41544956455f544f4b454e00000000'
    data = '0x00000000000000000000000046e6b214b524310239732d51387075e0e70970bf0000000000000000000000000f25496cf87be88c0a352d822c4ba92479f53601ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff'
    invoke_bulker_txn = base_bulk_contract.functions.invokeTransaction(withdraw_action, data)
    invoke_bulker_signtxn = w3.eth.account.sign_transaction(invoke_bulker_txn, private_key = acct._private_key)
    # w3.eth.send_raw_transaction(contract2_signtxn.rawTransaction)