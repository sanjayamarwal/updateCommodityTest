from enum import Enum


class VerificationStatus(str,Enum):
  FAILED = 'Fail - Unable to verify'
  SUCCESS ='Pass - Verified'
  PENDING = 'Pending in queue'
  ALREADY_VERIFIED = 'Contract source code already verified'

API_URLS = {
  1: 'https://api.etherscan.io/api',
  3: 'https://api-ropsten.etherscan.io/api',
  4: 'https://api-rinkeby.etherscan.io/api',
  5: 'https://api-goerli.etherscan.io/api',
  42: 'https://api-kovan.etherscan.io/api',
  56: 'https://api.bscscan.com/api',
  97: 'https://api-testnet.bscscan.com/api',
  128: 'https://api.hecoinfo.com/api',
  137: 'https://api.polygonscan.com/api',
  250: 'https://api.ftmscan.com/api',
  256: 'https://api-testnet.hecoinfo.com/api',
  4002: 'https://api-testnet.ftmscan.com/api',
  80001: 'https://api-testnet.polygonscan.com/api',
}

EXPLORER_URLS = {
  1: 'https://etherscan.io/address',
  3: 'https://ropsten.etherscan.io/address',
  4: 'https://rinkeby.etherscan.io/address',
  5: 'https://goerli.etherscan.io/address',
  42: 'https://kovan.etherscan.io/address',
  56: 'https://bscscan.com/address',
  97: 'https://testnet.bscscan.com/address',
  128: 'https://hecoinfo.com/address',
  137: 'https://polygonscan.com/address',
  250: 'https://ftmscan.com/address',
  256: 'https://testnet.hecoinfo.com/address',
  4002: 'https://testnet.ftmscan.com/address',
  80001: 'https://mumbai.polygonscan.com/address'
}

class RequestStatus:
  OK= '1'
  NOTOK= '0'


apiKey = {
  97: 'SF5KGIN7T26VP41BPDN5HGI4C9C1Z71TV3',
  1:  " "
}