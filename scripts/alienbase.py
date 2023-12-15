import time
from dotenv import load_dotenv
from brownie import *
from . import abi
load_dotenv()

UNISWAP_ROUTER_ADDRESS = '0x8c1A3cF8f83074169FE5D7aD50B978e1cD6b37c7'
CBETH_TOKEN_ADDRESS = '0x2Ae3F1Ec7F1F5012CFEab0185bfc7aa3cf0DEc22'
BASED_DISTRIBUTOR_ADDRESS = '0x52eaeCAC2402633d98b95213d0b473E069D86590'

def approve_tokens(contract, spender, val, account):
    contract.approve(spender, val, {'from': account})

def swap_eth_for_tokens(acct, val, token=None):
    unlim = 2**256-1
    cbeth_token_abi = abi.alienbase_cbeth_token_abi
    cbeth_token_contract = Contract.from_abi("UpgradeableOptimismMintableERC20", address = CBETH_TOKEN_ADDRESS, abi = cbeth_token_abi)
    if token == None:
        token = cbeth_token_contract
    approve_tokens(token, UNISWAP_ROUTER_ADDRESS, unlim, acct)
    uniswap_router_abi = abi.alienbase_uniswap_router_abi
    uniswap_router_contract = Contract.from_abi("UniswapV2Router02", address = UNISWAP_ROUTER_ADDRESS, abi = uniswap_router_abi)
    acct_address = acct.address
    uniswap_router_contract.swapExactETHForTokens(0, ["0x4200000000000000000000000000000000000006", token.address], acct_address, int(time.time()) + 60 * 10, {'from':acct, 'value':val})

def deposit(acct, val, token = None):
    cbeth_token_abi = abi.alienbase_cbeth_token_abi
    cbeth_token_contract = Contract.from_abi("UpgradeableOptimismMintableERC20", address = CBETH_TOKEN_ADDRESS, abi = cbeth_token_abi)
    if token == None:
        token = cbeth_token_contract
    unlim = 2**256-1
    approve_tokens(token, UNISWAP_ROUTER_ADDRESS, unlim, acct)
    uniswap_router_abi = abi.alienbase_uniswap_router_abi
    uniswap_router_contract = Contract.from_abi("UniswapV2Router02", address = UNISWAP_ROUTER_ADDRESS, abi = uniswap_router_abi)
    acct_address = acct.address
    swap_eth_for_tokens(acct, acct.balance()/5)
    token_amt = int(token.balanceOf.call(acct.address, {"from": acct}))
    token_min = 1
    eth_min = 1
    deadline = int(time.time()) + 1800
    uniswap_router_contract.addLiquidityETH(token.address, token_amt, token_min, eth_min, acct_address, deadline, {'from': acct, 'value': acct.balance()/20})
    uniswap_pair_address = '0x9BB646BF0F4Da44bfaF3d899e774DE065731EDFe'
    uniswap_pair_abi = abi.alienbase_uniswap_pair_abi
    uniswap_pair_contract = Contract.from_abi("UniswapV2Pair", address = uniswap_pair_address, abi = uniswap_pair_abi)
    approve_tokens(uniswap_pair_contract, BASED_DISTRIBUTOR_ADDRESS, val, acct)
    based_distributor_abi = abi.alienbase_based_distributor_abi
    based_distributor_contract = Contract.from_abi("BasedDistributorV2", address = BASED_DISTRIBUTOR_ADDRESS, abi = based_distributor_abi)
    pid = 6
    based_distributor_contract.deposit(pid, val, {"from": acct})
    return

def get_val(acct):
    based_distributor_abi = abi.alienbase_based_distributor_abi
    based_distributor_contract = Contract.from_abi("BasedDistributorV2", BASED_DISTRIBUTOR_ADDRESS, based_distributor_abi)
    pid = 6
    val = 0
    based_distributor_contract.deposit(pid, val, {'from': acct})
    val = based_distributor_contract.userInfo.call(6, acct.address, {'from': acct})[0]
    return val

def withdraw(acct):
    based_distributor_abi = abi.alienbase_based_distributor_abi
    based_distributor_contract = Contract.from_abi("BasedDistributorV2", address = BASED_DISTRIBUTOR_ADDRESS, abi = based_distributor_abi)
    pid = 6
    val = 0
    based_distributor_contract.deposit(pid, val, {"from": acct})
    val = get_val(acct)
    based_distributor_contract.withdraw(6, val, {"from": acct})
    return

