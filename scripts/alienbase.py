import time
from dotenv import load_dotenv
from brownie import *
from . import abi
load_dotenv()

def swap_eth_for_cbeth(acct, val):
    uniswap_router_address = '0x8c1A3cF8f83074169FE5D7aD50B978e1cD6b37c7'
    unlim = 115792089237316195423570985008687907853269984665640564039457584007913129639935
    cbeth_token_address = '0x2Ae3F1Ec7F1F5012CFEab0185bfc7aa3cf0DEc22'
    cbeth_token_abi = abi.alienbase_cbeth_token_abi
    cbeth_token_contract = Contract.from_abi("UpgradeableOptimismMintableERC20", address = cbeth_token_address, abi = cbeth_token_abi)
    cbeth_token_contract.approve(uniswap_router_address, unlim, {'from': acct})
    uniswap_router_abi = abi.alienbase_uniswap_router_abi
    uniswap_router_contract = Contract.from_abi("UniswapV2Router02", address = uniswap_router_address, abi = uniswap_router_abi)
    acct_address = acct.address
    uniswap_router_contract.swapExactETHForTokens(0, ["0x4200000000000000000000000000000000000006", cbeth_token_address], acct_address, int(time.time()) + 60 * 10, {'from':acct, 'value':val})

def a_deposit(acct, val):
    cbeth_token_address = '0x2Ae3F1Ec7F1F5012CFEab0185bfc7aa3cf0DEc22'
    cbeth_token_abi = abi.alienbase_cbeth_token_abi
    cbeth_token_contract = Contract.from_abi("UpgradeableOptimismMintableERC20", address = cbeth_token_address, abi = cbeth_token_abi)
    uniswap_router_address = '0x8c1A3cF8f83074169FE5D7aD50B978e1cD6b37c7'
    unlim = 115792089237316195423570985008687907853269984665640564039457584007913129639935
    cbeth_token_contract.approve(uniswap_router_address, unlim, {'from': acct})
    uniswap_router_abi = abi.alienbase_uniswap_router_abi
    uniswap_router_contract = Contract.from_abi("UniswapV2Router02", address = uniswap_router_address, abi = uniswap_router_abi)
    acct_address = acct.address
    swap_eth_for_cbeth(acct, acct.balance()/5)
    token_amt = int(cbeth_token_contract.balanceOf.call(acct.address, {"from": acct}))
    token_min = 1
    eth_min = 1
    deadline = int(time.time()) + 1800
    uniswap_router_contract.addLiquidityETH(cbeth_token_address, token_amt, token_min, eth_min, acct_address, deadline, {'from': acct, 'value': acct.balance()/20})
    uniswap_pair_address = '0x9BB646BF0F4Da44bfaF3d899e774DE065731EDFe'
    uniswap_pair_abi = abi.alienbase_uniswap_pair_abi
    uniswap_pair_contract = Contract.from_abi("UniswapV2Pair", address = uniswap_pair_address, abi = uniswap_pair_abi)
    based_distributor_address = '0x52eaeCAC2402633d98b95213d0b473E069D86590'
    uniswap_pair_contract.approve(based_distributor_address, val, {'from': acct})
    based_distributor_abi = abi.alienbase_based_distributor_abi
    based_distributor_contract = Contract.from_abi("BasedDistributorV2", address = based_distributor_address, abi = based_distributor_abi)
    pid = 6
    based_distributor_contract.deposit(pid, val, {"from": acct})
    return

def a_get_val(acct):
    based_distributor_address = '0x52eaeCAC2402633d98b95213d0b473E069D86590'
    based_distributor_abi = abi.alienbase_based_distributor_abi
    based_distributor_contract = Contract.from_abi("BasedDistributorV2", based_distributor_address, based_distributor_abi)
    pid = 6
    val = 0 # find value of alb
    based_distributor_contract.deposit(pid, val, {'from': acct})
    val = based_distributor_contract.userInfo.call(6, acct.address, {'from': acct})[0]
    return val

def a_withdraw(acct):
    based_distributor_address = '0x52eaeCAC2402633d98b95213d0b473E069D86590'
    based_distributor_abi = abi.alienbase_based_distributor_abi
    based_distributor_contract = Contract.from_abi("BasedDistributorV2", address = based_distributor_address, abi = based_distributor_abi)
    pid = 6
    val = 0 # find value of alb
    based_distributor_contract.deposit(pid, val, {"from": acct})
    val = a_get_val(acct)
    based_distributor_contract.withdraw(6, val, {"from": acct})
    return

