from web3 import Web3, HTTPProvider
from dotenv import load_dotenv
import abi
load_dotenv()

def deposit(acct, val):
    nonce = w3.eth.get_transaction_count(acct.address)
    allow_contract_address = '0x46e6b214b524310239732d51387075e0e70970bf'
    allow_contract_abi = abi.compound_allow_abi
    allow_contract = w3.eth.contract(address = allow_contract_address, abi = allow_contract_abi)
    allow_contract_txn = allow_contract.functions.allow('0x78D0677032A35c63D142a48A2037048871212a8C', true)
    allow_contract_signtxn = w3.eth.account.sign_transaction(allow_contract_txn, private_key = acct._private_key)
    # w3.eth.send_raw_transaction(allow_contract_signtxn.rawTransaction)
    invoke_contract_address = '0x78d0677032a35c63d142a48a2037048871212a8c'
    invoke_contract_abi = abi.compound_invoke_abi
    invoke_contract = w3.eth.contract(address = invoke_contract_address, abi = invoke_contract_abi)
    invoke_contract_txn = invoke_contract.functions.invoke('0x414354494f4e5f535550504c595f4e41544956455f544f4b454e000000000000', '0x00000000000000000000000046e6b214b524310239732d51387075e0e70970bf0000000000000000000000000f25496cf87be88c0a352d822c4ba92479f536010000000000000000000000000000000000000000000000000001c6bf52634000')
    invoke_contract_signtxn = w3.eth.account.sign_transaction(invoke_contract_txn, private_key = acct._private_key)
    # w3.eth.send_raw_transaction(invoke_contract_signtxn.rawTransaction)

def withdraw(acct):
    invoke_contract_address = '0xbc66d5bf7707b6237ebb630370f3f181b37000b9'
    invoke_contract_abi = abi.compound_invoke_abi
    invoke_contract = w3.eth.contract(address = invoke_contract_address, abi = invoke_contract_abi)
    implement_contract_address = '0x46e6b214b524310239732D51387075E0e70970bf'
    implement_contract_abi = abi.compound_implement_abi
    implement_contract = w3.eth.contract(address = implement_contract_address, abi = implement_contract_abi)
    val = implement_contract.functions.getBalance(acct)
    invoke_contract_txn = invoke_contract.functions.invokeTransaction('0x414354494f4e5f57495448445241575f4e41544956455f544f4b454e00000000', '0x00000000000000000000000046e6b214b524310239732d51387075e0e70970bf0000000000000000000000000f25496cf87be88c0a352d822c4ba92479f53601ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff')
    invoke_contract_signtxn = w3.eth.account.sign_transaction(invoke_contract_txn, private_key = acct._private_key)
    # w3.eth.send_raw_transaction(contract2_signtxn.rawTransaction)