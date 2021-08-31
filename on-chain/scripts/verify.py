from io import StringIO
import os
import subprocess
from pathlib import Path
import requests
from time import sleep
import json
import argparse
import shutil
import re
import time
from web3 import Web3
from scripts.constants import (
    API_URLS,
    EXPLORER_URLS,
    apiKey
)

def verify_contract(w3, network, contract_name='BPool', cache_file_name='contract_cache.json'):

    cache_file = Path(__file__).parent / 'contract-cache' / cache_file_name
    with open(cache_file, 'r') as f:
        contract_cache = json.load(f)

    if network == 'bsc-testnet':
        chain_id = 97
        bscscan_api = API_URLS[chain_id]
        apikey = apiKey[chain_id]

    if contract_name == 'BPool':
        build_file = Path(__file__).parent / ".." / \
                 'mettalex-balancer' / 'build' / 'contracts' / 'BPool.json'
        with open(build_file, 'r') as f:
            contract_details = json.load(f)

        source_file = Path(__file__).parent / ".." / \
                 'mettalex-balancer' / 'contracts'/'flats'/'BPool.sol'
        with open(source_file, 'r') as code:
            source_code = source_file.read_text()
            
            constructor_args = ''
            sendVerifyRequest(
                    bscscan_api,
                    apikey,
                    contract_details,
                    contract_cache['BPool'], 
                    source_code,
                    constructor_args) 
        
    # Strategy contracts
    elif contract_name == 'PoolController':    
    
        build_file_name = f'StrategyBalancerMettalexV3.json'
        pool_controller_build_file = Path(
            __file__).parent / ".." / 'pool-controller' / 'build' / 'contracts' / build_file_name

        with open(pool_controller_build_file, 'r') as f:
            contract_details = json.load(f)

        source_file = Path(__file__).parent / ".." / \
                 'pool-controller' /'contracts'/'flats'/'StrategyBalancerMettalexV3_flat.sol'
        with open(source_file, 'r') as code:
            source_code = source_file.read_text()
            constructor_args = '0000000000000000000000002e8fe590c8420c571ee3b7cb3a52f6990c2f43d1000000000000000000000000ba0c01aa68ac556bf38b1d6d1eefe1b4248b13e9000000000000000000000000ac0e6711739784e24f08c228017467578733c5ad000000000000000000000000dc15c2d1467e14b92a8b93df91f0064f9b760cdf000000000000000000000000962ae1f7ac7c0551f2d547dbcc76b65b6df9689a000000000000000000000000db56bda74642b4d570cdc79d6243070163df8210000000000000000000000000ba0c01aa68ac556bf38b1d6d1eefe1b4248b13e9'

    #    print('constructor_args', constructor_arguments, constructor_types, constructor_args) 
        
        sendVerifyRequest(
                    bscscan_api,
                    apikey,
                    contract_details,
                    contract_cache['PoolController'], 
                    source_code,
                    constructor_args)
    
    # Strategy Helper contract
    elif contract_name == 'StrategyHelper':    
    
        StrategyHelper_build_file = Path(
            __file__).parent / ".." / 'pool-controller' / 'build' / 'contracts' / 'StrategyHelper.json'
            
        with open(StrategyHelper_build_file, 'r') as f:
            contract_details = json.load(f)

        source_file = Path(__file__).parent / ".." / \
                 'pool-controller' /'contracts'/'flats'/'StrategyHelper_flat.sol'
        
        with open(source_file, 'r') as code:
            source_code = source_file.read_text()
            constructor_args = ''

        sendVerifyRequest(
                    bscscan_api,
                    apikey,
                    contract_details,
                    contract_cache['StrategyHelper'], 
                    source_code,
                    constructor_args)
    #Vault Contract
    elif contract_name == 'Vault':    
    
        Vault_build_file = Path(
            __file__).parent / ".." / 'mettalex-vault' / 'build' / 'contracts' / 'Vault.json'
            
        with open(Vault_build_file, 'r') as f:
            contract_details = json.load(f)

        source_file = Path(__file__).parent / ".." / \
                 'mettalex-vault' /'contracts'/'flats'/'Vault.sol'
        
        with open(source_file, 'r') as code:
            source_code = source_file.read_text()
            constructor_args = '0000000000000000000000000000000000000000000000000000000000000160000000000000000000000000000000000000000000000000000000000000000100000000000000000000000045f72c3ce459806adf2ebd35871abf7be1ce354b000000000000000000000000758b88428c6ac03a1c4a7153d2a280c214ef2020000000000000000000000000f2ff172e2f0dbf79b58b80e8dfdcdecbcc936068000000000000000000000000fcc8428a2236abecafb2d133235c53c3dbe753d5000000000000000000000000032bbd87f5371d26660483a92b281a27f8e35ab10000000000000000000000000000000000000000000000000000000000000bb800000000000000000000000000000000000000000000000000000000000007d000000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000000000000e4d657474616c6578205661756c74000000000000000000000000000000000000'
            
    #    print('constructor_args', constructor_arguments, constructor_types, constructor_args) 
        sendVerifyRequest(
                    bscscan_api,
                    apikey,
                    contract_details,
                    contract_cache['Vault'], 
                    source_code,
                    constructor_args)
        


def sendVerifyRequest(
        bscscan_api,
        apikey,
        contract_details,
        contract_address,
        source_code,
        constructor_args=''
    ):

    contract_name = contract_details['contractName']

    print(f'APIKEY= {apikey}')
    print(f'deployed contract address: {contract_address}')
    print(f'Contract to verify:{contract_name}')

    data = {
        # A valid API-Key is required
        'apikey': apikey,
        # Do not change
        'module': 'contract',
        # Do not change
        'action': 'verifysourcecode',
        'contractaddress': contract_address,
        'sourceCode': source_code,
        'codeformat': 'solidity-single-file',
        'contractname': contract_name,
        'compilerversion': 'v'+contract_details['compiler']['version'],
        'optimizationUsed': 0 if contract_details['compiler']['optimizer']['enabled'] is False else 1,
        'runs': 200,
        'constructorArguments': constructor_args,
        'EVMVersion' : contract_details['compiler']['evmVersion'],
    }

    print(f'{data}')

    response = requests.post(bscscan_api, data=data)

    content = json.loads(response.content.decode())
    print(content)

    print(f'Status: {content["status"]}; {content["message"]} ; GUID = {content["result"]}')

    if content["status"] == "1":
        status = '0'
        retries = 10
        while status == '0' and retries > 0:
            retries -= 1
            r = guid_status(bscscan_api, apikey, content["result"])
            status = r['status']
            if r['result'] == 'Fail - Unable to verify':
                return
            print('Retrying...')
            sleep(10)
    
def guid_status(bscscan_api, apikey, guid):
    data = {
        'apikey': apikey,
        'module': "contract",
        'action': "checkverifystatus",
        'guid': guid, 
    }
    r = requests.get(bscscan_api, data=data)
    status_content = json.loads(r.content.decode())
    print(status_content)
    return status_content

# def fetchConstructorValues(contract_address, chain_id):
#    try:
#        data = {
#            'apikey': apikey,
#            'module': "account",
#           'action': "txlist",
#            'address': contract_address,
#            'page' : 1,
#            'sort' : "asc",

#            'offset' : 1
#        }
#        url = bscscan_api + data
#        res = requests.get(url)
#    except:
#            raise Exception('Failed to connect to bscscan API at url')
    
#    if res["status"] == "1" and res["result"]:
        
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser('Mettalex System Verification')
    parser.add_argument(
        '--action', '-a', dest='action', default='verify',
        help='Action to perform: connect, deploy (default), setup, verify'
    )
    parser.add_argument(
        '--network', '-n', dest='network', default='local',
        help='For connecting to local, kovan, bsc-testnet or bsc-mainnet network'
    )
    parser.add_argument(
        '--strategy', '-v', dest='strategy', default=3,
        help='For getting strategy version we want to deploy DEX for'
    )
    parser.add_argument(
        '--simulation', '-s', dest='simulation', default='none',
        help=''
    )
    parser.add_argument(
       '--contract-name', dest='contract_name', default='BPool',
       help='contract name that we want to verify' 
    )
    parser.add_argument(
        '--forceConstructorargs:string', dest='constructor-args', default='none',
        help=''
    )

    args = parser.parse_args()
    assert args.network in {'local', 'kovan', 'bsc-testnet', 'bsc-mainnet'}
    assert args.strategy in {'1', '2', '3', '4'}

    if args.action == 'verify':
        verify_contract(w3, args.network, StringIO(args.contract_name))
    else:
        raise ValueError(f'Unknown action: {args.action}')
