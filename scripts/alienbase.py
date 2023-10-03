from web3 import Web3, HTTPProvider
w3 = Web3(HTTPProvider('https://base-mainnet.g.alchemy.com/v2/UvGuEYnKdeysDcuxqu6Zy5mZkzYBMx3e'))
def deposit(acct, val):
    nonce = w3.eth.get_transaction_count(acct.address)
    contract1_address = 
    contract1_abi = 
    