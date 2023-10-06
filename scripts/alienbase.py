from web3 import Web3, HTTPProvider
from dotenv import load_dotenv
import os
load_dotenv()

w3 = Web3(HTTPProvider('https://base-mainnet.g.alchemy.com/v2/UvGuEYnKdeysDcuxqu6Zy5mZkzYBMx3e'))
def deposit(acct, val):
    nonce = w3.eth.get_transaction_count(acct.address)
    approve_contract_address = '0x2Ae3F1Ec7F1F5012CFEab0185bfc7aa3cf0DEc22'
    approve_contract_abi = os.getenv("alienbase_approve_abi")
    approve_contract = w3.eth.contract(address = approve_contract_address, abi = approve_contract_abi)
    approve_contract_txn = approve_contract.functions.approve('0x8c1A3cF8f83074169FE5D7aD50B978e1cD6b37c7',115792089237316195423570985008687907853269984665640564039457584007913129639935).build_transaction({'chainId': 8453, 'gas': 200000, 'gasPrice': w3.to_wei('0.01', 'gwei'), 'nonce': nonce,})
    approve_contract_signtxn = w3.eth.account.sign_transaction(approve_contract_txn, private_key = acct._private_key)
    # w3.eth.send_raw_transaction(approve_contract_signtxt.rawTransaction)
    
    add_contract_address = '0x8c1A3cF8f83074169FE5D7aD50B978e1cD6b37c7'
    add_contract_abi = os.getenv("alienbase_add_eth_abi")
    add_contract = w3.eth.contract(address = add_contract_address, abi = add_contract_abi)
    acct_address = acct.address
    # print(dir(add_contract.functions))
    add_contract_txn = add_contract.functions.addLiquidityETH(acct_address, 9547905041126, 9500165515920, 9950000000000, '0x0F25496cf87bE88C0a352d822C4BA92479F53601', 1695788793)
    add_contract_signtxn = w3.eth.account.sign_transaction(add_contract_txn, private_key = acct._private_key)
    # w3.eth.send_raw_transaction(add_contract_signtxn.rawTransaction)
    
    approve_spec_contract_address = '0x9BB646BF0F4Da44bfaF3d899e774DE065731EDFe'
    approve_spec_contract_abi = os.getenv("alienbase_approve_spec_abi")
    approve_spec_contract = w3.eth.contract(address = approve_spec_contract_address, abi = approve_spec_contract_abi)
    approve_spec_contract_txn = approve_spec_contract.functions.approve('0x52eaeCAC2402633d98b95213d0b473E069D86590', 5000000000000000000000000)
    approve_spec_contract_signtxn = w3.eth.account.sign_transaction(approve_spec_contract_txn, private_key = acct._private_key)
    # w3.eth.send_raw_transaction(approve_spec_contract_signtxn.rawTransaction)
    
    deposit_contract_address = '0x52eaeCAC2402633d98b95213d0b473E069D86590'
    deposit_contract_abi = os.getenv("alienbase_deposit_abi")
    deposit_contract = w3.eth.contract(address = deposit_contract_address, abi = deposit_contract_abi)
    deposit_contract_txn = deposit_contract.functions.deposit(6, 9764677045213)
    deposit_contract_signtxn = w3.eth.account.sign_transaction(deposit_contract_txn, private_key = acct._private_key)
    # w3.eth.send_raw_transaction(deposit_contract_signtxn.rawTransaction)

def withdraw(acct):
    deposit_contract_address = w3.to_checksum_address('0x52eaecac2402633d98b95213d0b473e069d86590')
    deposit_contract_abi = os.getenv("alienbase_deposit_abi")
    deposit_contract = w3.eth.contract(address = deposit_contract_address, abi = deposit_contract_abi)
    deposit_contract_txn = deposit_contract.functions.deposit(6, 0)
    # deposit_contract_signtxn = w3.eth.account.sign_transaction(deposit_contract_txn, private_key = acct._private_key)
    # w3.eth.send_raw_transaction(deposit_contract_signtxn.rawTransaction)
    withdraw_contract_address = w3.to_checksum_address('0x52eaecac2402633d98b95213d0b473e069d86590')
    withdraw_contract_abi = os.getenv("alienbase_deposit_abi")
    withdraw_contract = w3.eth.contract(address = withdraw_contract_address, abi = withdraw_contract_abi)
    val = withdraw_contract.functions.userInfo(6, w3.to_checksum_address('0x0f25496cf87be88c0a352d822c4ba92479f53601')).call()
    print(val)
    # withdraw_contract_txn = withdraw_contract.functions.withdraw(6, val)   
    # withdraw_contract_signtxn = w3.eth.account.sign_transaction(withdraw_contract_txn, private_key = acct._private_key)
    # w3.eth.send_raw_transaction(withdraw_contract_signtxn.rawTransaction)
from ape import accounts, Contract
import alienbase, compound
acct = accounts.load("test")
withdraw(acct)