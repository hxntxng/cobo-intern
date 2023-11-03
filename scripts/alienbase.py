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
    cbeth_token_contract = Contract.from_abi("UpgradeableOptimismMintableERC20", address = cbeth_token_address, abi = cbeth_token_abi)
    uniswap_router_address = '0x8c1A3cF8f83074169FE5D7aD50B978e1cD6b37c7'
    unlim = 115792089237316195423570985008687907853269984665640564039457584007913129639935
    cbeth_token_contract.approve(uniswap_router_address, unlim, {'from': acct})
    # approve_cbeth_token_signtxn = w3.eth.account.sign_transaction(approve_cbeth_token_txn, private_key = acct.private_key)
    # w3.eth.send_raw_transaction(approve_cbeth_token_signtxn.rawTransaction)
    # breakpoint()
    uniswap_router_abi = abi.alienbase_uniswap_router_abi
    uniswap_router_contract = Contract.from_abi("UniswapV2Router02", address = uniswap_router_address, abi = uniswap_router_abi)
    acct_address = acct.address
    # print(dir(add_contract.functions))
    uniswap_router_contract.swapExactETHForTokens(0, ["0x4200000000000000000000000000000000000006", cbeth_token_address], acct_address, int(time.time()) + 60 * 10, {'from':acct, 'value':acct.balance()/5})
    token_amt = acct.balance()/10
    token_min = 1
    eth_min = 1
    deadline = int(time.time()) + 1800
    uniswap_router_contract.addLiquidityETH(cbeth_token_address, token_amt, token_min, eth_min, acct_address, deadline, {'from': acct, 'value': acct.balance()/20})
    # addLiquidity_uniswap_signtxn = w3.eth.account.sign_transaction(addLiquidity_uniswap_txn, private_key = acct.private_key)
    # w3.eth.send_raw_transaction(addLiquidity_uniswap_signtxn.rawTransaction)
    # breakpoint()
    uniswap_pair_address = '0x9BB646BF0F4Da44bfaF3d899e774DE065731EDFe'
    uniswap_pair_abi = abi.alienbase_uniswap_pair_abi
    uniswap_pair_contract = Contract.from_abi("UniswapV2Pair", address = uniswap_pair_address, abi = uniswap_pair_abi)
    based_distributor_address = '0x52eaeCAC2402633d98b95213d0b473E069D86590'
    uniswap_pair_contract.approve(based_distributor_address, val, {'from': acct})
    # approve_uniswap_signtxn = w3.eth.account.sign_transaction(approve_uniswap_txn, private_key = acct.private_key)
    # w3.eth.send_raw_transaction(approve_uniswap_signtxn.rawTransaction)
    # breakpoint()
    based_distributor_abi = abi.alienbase_based_distributor_abi
    based_distributor_contract = Contract.from_abi("BasedDistributorV2", address = based_distributor_address, abi = based_distributor_abi)
    pid = 6
    amount = 9764677045213 # not sure what this number is
    based_distributor_contract.deposit(pid, val, {"from": acct})
    # deposit_distributor_signtxn = w3.eth.account.sign_transaction(deposit_distributor_txn, private_key = acct.private_key)
    # w3.eth.send_raw_transaction(deposit_distributor_signtxn.rawTransaction)
    return

def a_get_val(w3, acct):
    nonce = w3.eth.get_transaction_count(acct.address)
    chainId = 1337
    based_distributor_address = '0x52eaeCAC2402633d98b95213d0b473E069D86590'
    based_distributor_abi = abi.alienbase_based_distributor_abi
    based_distributor_contract = Contract.from_abi("BasedDistributorV2", based_distributor_address, based_distributor_abi)
    pid = 6
    val = 0 # find value of alb
    based_distributor_contract.deposit(pid, val, {'from': acct})
    # .build_transaction({'gas': 200000, 'gasPrice': w3.toWei('0.01', 'gwei'), 'nonce': nonce,})
    # deposit_distributor_signtxn = w3.eth.account.sign_transaction(deposit_distributor_txn, private_key = acct.private_key)
    # w3.eth.send_raw_transaction(deposit_distributor_signtxn.rawTransaction)
    val = based_distributor_contract.userInfo.call(6, acct.address, {'from': acct})[0]

    return val

def a_withdraw(w3, acct):
    chainId=1337
    nonce = w3.eth.get_transaction_count(acct.address)
    based_distributor_address = '0x52eaeCAC2402633d98b95213d0b473E069D86590'
    based_distributor_abi = abi.alienbase_based_distributor_abi
    based_distributor_contract = Contract.from_abi("BasedDistributorV2", address = based_distributor_address, abi = based_distributor_abi)
    pid = 6
    val = 0 # find value of alb
    based_distributor_contract.deposit(pid, val, {"from": acct})
    # deposit_distributor_signtxn = w3.eth.account.sign_transaction(deposit_distributor_txn, private_key = acct.private_key)
    # w3.eth.send_raw_transaction(deposit_distributor_signtxn.rawTransaction)
    val = a_get_val(w3, acct)
    # breakpoint()
    based_distributor_contract.withdraw(6, val, {"from": acct})
    # withdraw_distributor_signtxn = w3.eth.account.sign_transaction(withdraw_distributor_txn, private_key = acct.private_key)
    # w3.eth.send_raw_transaction(withdraw_distributor_signtxn.rawTransaction)
    return

