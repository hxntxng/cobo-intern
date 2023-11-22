from web3 import Web3, HTTPProvider
from dotenv import load_dotenv
from brownie import *
from eth_abi import encode, decode
from . import abi
import time
load_dotenv()

def c_deposit(acct, val):
    cWETH_address = '0x46e6b214b524310239732D51387075E0e70970bf'
    cbeth_token_address = '0x2Ae3F1Ec7F1F5012CFEab0185bfc7aa3cf0DEc22'
    cWETH_abi = abi.cWETH_abi
    cWETH_contract = Contract.from_abi("CometExt", address = cWETH_address, abi = cWETH_abi)
    base_bulk_address = '0x78D0677032A35c63D142a48A2037048871212a8C'
    allowed = True
    # cWETH_contract.allow(base_bulk_address, allowed, {"from": acct})
    # cbeth_token_address = '0x2Ae3F1Ec7F1F5012CFEab0185bfc7aa3cf0DEc22'
    cbeth_token_abi = abi.alienbase_cbeth_token_abi
    cbeth_token_contract = Contract.from_abi("UpgradeableOptimismMintableERC20", address = cbeth_token_address, abi = cbeth_token_abi)
    uniswap_router_address = '0x8c1A3cF8f83074169FE5D7aD50B978e1cD6b37c7'
    unlim = 115792089237316195423570985008687907853269984665640564039457584007913129639935
    cbeth_token_contract.approve(uniswap_router_address, unlim, {'from': acct})
    uniswap_router_abi = abi.alienbase_uniswap_router_abi
    uniswap_router_contract = Contract.from_abi("UniswapV2Router02", address = uniswap_router_address, abi = uniswap_router_abi)
    acct_address = acct.address
    uniswap_router_contract.swapExactETHForTokens(0, ["0x4200000000000000000000000000000000000006", cbeth_token_address], acct_address, int(time.time()) + 60 * 10, {'from':acct, 'value':acct.balance()/5})
    base_bulk_abi = abi.compound_base_bulk_abi
    base_bulk_contract = Contract.from_abi("BaseBulker", address = base_bulk_address, abi = base_bulk_abi)
    deposit_action = [Web3.toBytes(hexstr='0x414354494f4e5f535550504c595f415353455400000000000000000000000000')]
    val = int(acct.balance()/70)
    print(val, acct.balance())
    data = [encode(['address', 'address', 'address', 'uint'], [cWETH_address, acct.address, cbeth_token_address, val])]
    print(decode(['address', 'address', 'address', 'uint256'], data[0]))
    print(cbeth_token_contract.balanceOf.call(acct.address, {"from": acct}), val, acct.balance())
    cbeth_token_contract.approve(cWETH_address, 1000*10**18, {"from": acct, "gasPrice": 1000000000000, "gas": 10000000, "allow_revert": True})
    base_bulk_contract.invoke(deposit_action, data, {"from": acct, "value": val, "gasPrice": 100000000000000000, "gas": 10000000, "allow_revert": True})
    print([i for i in history])
    return val

def c_get_val(acct):
    implement_contract_address = '0x46e6b214b524310239732D51387075E0e70970bf'
    implement_contract_abi = abi.compound_implement_abi 
    implement_contract = Contract.from_abi("BaseBulker", implement_contract_address, implement_contract_abi)
    val = implement_contract.balanceOf.call(acct.address, {"from": acct})
    print(val)
    return val

def c_withdraw(acct):
    base_bulk_address = '0x78D0677032A35c63D142a48A2037048871212a8C'
    base_bulk_abi = abi.compound_base_bulk_abi
    base_bulk_contract = Contract.from_abi("BaseBulker", address = base_bulk_address, abi = base_bulk_abi)
    val = c_get_val(acct)
    withdraw_action = [Web3.toBytes(hexstr='0x414354494f4e5f57495448445241575f4e41544956455f544f4b454e00000000')]
    data = [Web3.toBytes(hexstr='0x00000000000000000000000046e6b214b524310239732d51387075e0e70970bf0000000000000000000000000f25496cf87be88c0a352d822c4ba92479f53601ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff')]
    base_bulk_contract.invoke(withdraw_action, data, {"from": acct, "value": val})
    return