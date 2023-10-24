import time
from web3 import Web3, HTTPProvider
from dotenv import load_dotenv
from brownie import *
import os
from . import abi
load_dotenv()

#w3 = Web3(HTTPProvider(os.getenv("network_key"), request_kwargs={'timeout':60}))
def a_deposit(w3, acct, val):
    nonce = w3.eth.get_transaction_count(acct.address)
    cbeth_token_address = '0x2Ae3F1Ec7F1F5012CFEab0185bfc7aa3cf0DEc22'
    cbeth_token_abi = abi.alienbase_cbeth_token_abi
    cbeth_token_contract = w3.eth.contract(address = cbeth_token_address, abi = cbeth_token_abi)
    uniswap_router_address = '0x8c1A3cF8f83074169FE5D7aD50B978e1cD6b37c7'
    unlim = 115792089237316195423570985008687907853269984665640564039457584007913129639935
    approve_cbeth_token_txn = cbeth_token_contract.functions.approve(uniswap_router_address, unlim).build_transaction({'gas': 200000, 'gasPrice': w3.toWei('0.01', 'gwei'), 'nonce': nonce,})
    approve_cbeth_token_signtxn = w3.eth.account.sign_transaction(approve_cbeth_token_txn, private_key = acct.private_key)
    w3.eth.send_raw_transaction(approve_cbeth_token_signtxn.rawTransaction)
    # breakpoint()
    uniswap_router_abi = abi.alienbase_uniswap_router_abi
    uniswap_router_contract = w3.eth.contract(address = uniswap_router_address, abi = uniswap_router_abi)
    acct_address = acct.address
    # print(dir(add_contract.functions))
    token_amt = 9547905041126
    token_min = 9500165515920
    eth_min = 9950000000000
    deadline = int(time.time()) + 1800
    addLiquidity_uniswap_txn = uniswap_router_contract.functions.addLiquidityETH(cbeth_token_address, token_amt, token_min, eth_min, acct_address, deadline).build_transaction({'gas': 200000, 'gasPrice': w3.toWei('0.01', 'gwei'), 'nonce': nonce, 'value': w3.toWei(f'{val/10000000}', 'gwei')})
    addLiquidity_uniswap_signtxn = w3.eth.account.sign_transaction(addLiquidity_uniswap_txn, private_key = acct.private_key)
    w3.eth.send_raw_transaction(addLiquidity_uniswap_signtxn.rawTransaction)
    # breakpoint()
    uniswap_pair_address = '0x9BB646BF0F4Da44bfaF3d899e774DE065731EDFe'
    uniswap_pair_abi = abi.alienbase_uniswap_pair_abi
    uniswap_pair_contract = w3.eth.contract(address = uniswap_pair_address, abi = uniswap_pair_abi)
    based_distributor_address = '0x52eaeCAC2402633d98b95213d0b473E069D86590'
    approve_uniswap_txn = uniswap_pair_contract.functions.approve(based_distributor_address, val).build_transaction({'gas': 200000, 'gasPrice': w3.toWei('0.01', 'gwei'), 'nonce': nonce,})
    approve_uniswap_signtxn = w3.eth.account.sign_transaction(approve_uniswap_txn, private_key = acct.private_key)
    w3.eth.send_raw_transaction(approve_uniswap_signtxn.rawTransaction)
    # breakpoint()
    based_distributor_abi = abi.alienbase_based_distributor_abi
    based_distributor_contract = w3.eth.contract(address = based_distributor_address, abi = based_distributor_abi)
    pid = 6
    amount = 9764677045213 # not sure what this number is
    deposit_distributor_txn = based_distributor_contract.functions.deposit(pid, val).build_transaction({'gas': 200000, 'gasPrice': w3.toWei('0.01', 'gwei'), 'nonce': nonce,})
    deposit_distributor_signtxn = w3.eth.account.sign_transaction(deposit_distributor_txn, private_key = acct.private_key)
    w3.eth.send_raw_transaction(deposit_distributor_signtxn.rawTransaction)
    return

def a_get_val(w3, acct):
    nonce = w3.eth.get_transaction_count(acct.address)
    chainId = 1337
    based_distributor_address = '0x52eaeCAC2402633d98b95213d0b473E069D86590'
    based_distributor_abi = abi.alienbase_based_distributor_abi
    based_distributor_contract = w3.eth.contract(address = based_distributor_address, abi = based_distributor_abi)
    pid = 6
    val = 0 # find value of alb
    deposit_distributor_txn = based_distributor_contract.functions.deposit(pid, val).build_transaction({'gas': 200000, 'gasPrice': w3.toWei('0.01', 'gwei'), 'nonce': nonce,})
    deposit_distributor_signtxn = w3.eth.account.sign_transaction(deposit_distributor_txn, private_key = acct.private_key)
    # breakpoint()
    w3.eth.send_raw_transaction(deposit_distributor_signtxn.rawTransaction)
    # breakpoint()
    val = based_distributor_contract.functions.userInfo(6, acct.address).call()[0]
    # build_transaction({'gas': 200000, 'gasPrice': w3.toWei('0.01', 'gwei'), 'nonce': nonce,})
    # val_signtxn = w3.eth.account.sign_transaction(val_txn, private_key = acct.private_key)
    # print(val.call)
    return val

def a_withdraw(w3, acct):
    chainId=1337
    nonce = w3.eth.get_transaction_count(acct.address)
    print(nonce)
    based_distributor_address = '0x52eaeCAC2402633d98b95213d0b473E069D86590'
    based_distributor_abi = abi.alienbase_based_distributor_abi
    based_distributor_contract = w3.eth.contract(address = based_distributor_address, abi = based_distributor_abi)
    pid = 6
    val = 0 # find value of alb
    breakpoint()
    deposit_distributor_txn = based_distributor_contract.functions.deposit(pid, val).build_transaction({'gas': 200000, 'gasPrice': w3.toWei('0.01', 'gwei'), 'nonce': nonce,})
    deposit_distributor_signtxn = w3.eth.account.sign_transaction(deposit_distributor_txn, private_key = acct.private_key)
    w3.eth.send_raw_transaction(deposit_distributor_signtxn.rawTransaction)
    val = a_get_val(w3, acct)
    print(nonce)
    breakpoint()
    nonce = w3.eth.get_transaction_count(acct.address)
    withdraw_distributor_txn = based_distributor_contract.functions.withdraw(6, val).build_transaction({'gas': 200000, 'gasPrice': w3.toWei('0.01', 'gwei'), 'nonce': nonce,})
    withdraw_distributor_signtxn = w3.eth.account.sign_transaction(withdraw_distributor_txn, private_key = acct.private_key)
    w3.eth.send_raw_transaction(withdraw_distributor_signtxn.rawTransaction)
    return

