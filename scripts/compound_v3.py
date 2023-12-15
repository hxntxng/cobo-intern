from web3 import Web3
from dotenv import load_dotenv
from brownie import Contract
from eth_abi import encode
from . import abi
from brownie.network.gas.strategies import GasNowStrategy
import time
load_dotenv()

UNISWAP_ROUTER_ADDRESS = '0x8c1A3cF8f83074169FE5D7aD50B978e1cD6b37c7'
CBETH_TOKEN_ADDRESS = '0x2Ae3F1Ec7F1F5012CFEab0185bfc7aa3cf0DEc22'
CWETH_ADDRESS = '0x46e6b214b524310239732D51387075E0e70970bf'
BASE_BULK_ADDRESS = '0x78D0677032A35c63D142a48A2037048871212a8C'

def approve_token(contract, spender, val, account):
    contract.approve(spender, val, {'from': account})

def swap_eth_for_token(token, acct, val):
    unlim = 2**256-1
    approve_token(token, UNISWAP_ROUTER_ADDRESS, unlim, acct)
    uniswap_router_abi = abi.alienbase_uniswap_router_abi
    uniswap_router_contract = Contract.from_abi("UniswapV2Router02", address = UNISWAP_ROUTER_ADDRESS, abi = uniswap_router_abi)
    acct_address = acct.address
    uniswap_router_contract.swapExactETHForTokens(0, ["0x4200000000000000000000000000000000000006", CBETH_TOKEN_ADDRESS], acct_address, int(time.time()) + 60 * 10, {'from':acct, 'value':val})


def deposit_collateral(acct, val, token=None):
    gas_strategy = GasNowStrategy("fast")
    cWETH_abi = abi.cWETH_abi
    cWETH_contract = Contract.from_abi("CometExt", address = CWETH_ADDRESS, abi = cWETH_abi)
    cWETH_contract.allow(BASE_BULK_ADDRESS, True, {"from": acct})
    cbeth_token_abi = abi.alienbase_cbeth_token_abi
    cbeth_token_contract = Contract.from_abi("UpgradeableOptimismMintableERC20", address = CBETH_TOKEN_ADDRESS, abi = cbeth_token_abi)
    if token == None:
        token = cbeth_token_contract
    swap_eth_for_token(token, acct, acct.balance()/5)
    base_bulk_abi = abi.compound_base_bulk_abi
    base_bulk_contract = Contract.from_abi("BaseBulker", address = BASE_BULK_ADDRESS, abi = base_bulk_abi)
    deposit_action = [Web3.toBytes(hexstr='0x414354494f4e5f535550504c595f415353455400000000000000000000000000')]
    val = int(token.balanceOf.call(acct.address, {"from": acct}))
    data = [encode(['address', 'address', 'address', 'uint'], [CWETH_ADDRESS, acct.address, CBETH_TOKEN_ADDRESS, val])]
    approve_token(token, UNISWAP_ROUTER_ADDRESS, 1000 * 10**18, acct)
    base_bulk_contract.invoke(deposit_action, data, {"from": acct.address, "value": 0, "gasPrice": gas_strategy, "allow_revert": True})
    return val

def get_collateral_val(acct, token=None):
    cWETH_abi = abi.cWETH_abi
    cWETH_contract = Contract.from_abi("cWETH proxy", CWETH_ADDRESS, cWETH_abi)
    cbeth_token_abi = abi.alienbase_cbeth_token_abi
    cbeth_token_contract = Contract.from_abi("UpgradeableOptimismMintableERC20", address = CBETH_TOKEN_ADDRESS, abi = cbeth_token_abi)
    if token == None:
        token = cbeth_token_contract
    val = cWETH_contract.collateralBalanceOf(acct, token.address)
    return val

def withdraw_collateral(acct, token=None):
    gas_strategy = GasNowStrategy("fast")
    cWETH_abi = abi.cWETH_abi
    cWETH_contract = Contract.from_abi("CometExt", address = CWETH_ADDRESS, abi = cWETH_abi)
    cWETH_contract.allow(BASE_BULK_ADDRESS, True, {"from": acct})
    base_bulk_abi = abi.compound_base_bulk_abi
    base_bulk_contract = Contract.from_abi("BaseBulker", address = BASE_BULK_ADDRESS, abi = base_bulk_abi)
    cbeth_token_abi = abi.alienbase_cbeth_token_abi
    cbeth_token_contract = Contract.from_abi("UpgradeableOptimismMintableERC20", address = CBETH_TOKEN_ADDRESS, abi = cbeth_token_abi)
    if token == None:
        token = cbeth_token_contract
    val = int(get_collateral_val(acct))
    withdraw_action = [Web3.toBytes(hexstr='0x414354494f4e5f57495448445241575f41535345540000000000000000000000')]
    # print(decode('string', withdraw_action[0]), encode(['string', "ACTION_WITHDRAW_ASSET"]))
    data = [encode(['address', 'address', 'address', 'uint'], [CWETH_ADDRESS, acct.address, token.address, val])]
    base_bulk_contract.invoke(withdraw_action, data, {"from": acct.address, "value": 0, "gasPrice": gas_strategy, "allow_revert": True})
    return