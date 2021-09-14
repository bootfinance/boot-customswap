#!/usr/bin/python3

import pytest
import json
from brownie import chain

# wBTC = "0x2260fac5e5542a773aa44fbcfedf7c193bc2c599"
# sBTC = "0xfe18be6b3bd88a2d2a7f928d00292e7a9963cfc6"
# renBTC = "0xeb4c2781e4eba804ce9a9803c67d0893436bb27d"
# LPBTC = "0x28a8746e75304c0780E011BEd21C72cD78cd535E"
A_BTC = 0
_init_fee_BTC = 0
_admin_fee_BTC = 0

# USDT = "0xdac17f958d2ee523a2206206994597c13d831ec7"
# USDC = "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48"
# TUSD = "0x0000000000085d4780B73119b644AE5ecd22b376"
# DAI = "0x6b175474e89094c44da98b954eedeac495271d0f"
# LPUSD = "0x28a8746e75304c0780E011BEd21C72cD78cd535E"
A_USD = 0
_init_fee_USD = 0

# WETH = "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2"
# WETH1 = "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2"
# LPETH = "0x28a8746e75304c0780E011BEd21C72cD78cd535E"
A_ETH = 100
_init_fee_ETH = 4000000
_admin_fee_ETH = 5000000000

VOTING_ESCROW_NAME = "Voting Escrow Name"
VOTING_ESCROW_SYMBOL = "Voting Escrow Symbol"
VOTING_ESCROW_VERSION = "Voting Escrow V1"

USD_LP_TOKEN_NAME = "USD LP Token Name"
USD_LP_TOKEN_SYMBOL = "USD LP Token Symbol"
USD_LP_TOKEN_DECIMALS = 18
USD_LP_TOKEN_SUPPLY = 1000000e18

BTC_LP_TOKEN_NAME = "BTC LP Token Name"
BTC_LP_TOKEN_SYMBOL = "BTC LP Token Symbol"
BTC_LP_TOKEN_DECIMALS = 18
BTC_LP_TOKEN_SUPPLY = 1000000e18

ETH_LP_TOKEN_NAME = "ETH LP Token Name"
ETH_LP_TOKEN_SYMBOL = "ETH LP Token Symbol"
ETH_LP_TOKEN_DECIMALS = 18
ETH_LP_TOKEN_SUPPLY = 1000000e18

SWAP_FEE = 1e7
MAX_UINT256 = 2**256 - 1

@pytest.fixture(scope="session")
def admin(accounts):
    return accounts[1] # owns the deployment process and resulting contract instances

@pytest.fixture(scope="session")
def provider(accounts):
    return accounts[2] # provides liquidity, synonym for trader1

@pytest.fixture(scope="session")
def provider1(accounts):
    return accounts[2] # provides liquidity

@pytest.fixture(scope="session")
def provider2(accounts):
    return accounts[3] # provides liquidity 

@pytest.fixture(scope="session")
def provider3(accounts):
    return accounts[4] # provides liquidity 

@pytest.fixture(scope="session")
def trader(accounts):
    return accounts[5] # trades/swaps via custom swap, synonym for trader1

@pytest.fixture(scope="session")
def trader1(accounts):
    return accounts[5] # trades/swaps via custom swap

@pytest.fixture(scope="session")
def trader2(accounts):
    return accounts[6] # trades/swaps via custom swap

@pytest.fixture(scope="session")
def trader3(accounts):
    return accounts[7] # trades/swaps via custom swap

@pytest.fixture(scope="session")
def account(accounts):
    return accounts[8] # synonym for account1

@pytest.fixture(scope="session")
def account1(accounts):
    return accounts[8] # trades/swaps via custom swap

@pytest.fixture(scope="session")
def account2(accounts):
    return accounts[9]

@pytest.fixture(scope="module")
def boot(MainToken, admin):
    return MainToken.deploy("BOOT Finance Token", "BOOT", 18, {'from': admin})

@pytest.fixture(scope="module")
def voting_escrow(boot, admin, VotingEscrow):
    return VotingEscrow.deploy(boot.address, VOTING_ESCROW_NAME, VOTING_ESCROW_SYMBOL, VOTING_ESCROW_VERSION, {'from': admin})

@pytest.fixture(scope="module")
def gauge_controller(boot, voting_escrow, admin, GaugeController):
    r = GaugeController.deploy(boot.address, voting_escrow.address, {'from': admin})
    r.add_type("Pool Gauge1")
    r.add_type("Pool Gauge2")
    return r

@pytest.fixture(scope="module")
def minter(boot, gauge_controller, admin, Minter):
    m = Minter.deploy(boot.address, gauge_controller.address, {'from': admin})
    boot.set_minter(m)
    return m

@pytest.fixture(scope="module")
def faucet(boot, minter, accounts):
    chain.sleep(52*7*24*60*60)      # to increase available_supply
    boot.update_mining_parameters() # here
    qty = boot.available_supply()
    assert qty != 0
    n = 10 * 10**18
    assert boot.mint(accounts[0], 0, n, {'from': minter})
    balance = boot.balanceOf(accounts[0])
    assert balance == n
    return accounts[0]

# A number of ERC20 tests in tests/token expect accounts[0] to be the faucet
# and assume the token fixture is the main BOOT token.
#
@pytest.fixture(scope="module")
def token(boot, faucet):
    return boot

@pytest.fixture(scope="module")
def wBTC(Token, faucet):
    return Token.deploy("wBTC Token", "wBTC", 18, 1e21, {'from': faucet})
@pytest.fixture(scope="module")
def sBTC(Token, faucet):
    return Token.deploy("sBTC Token", "sBTC", 18, 1e21, {'from': faucet})
@pytest.fixture(scope="module")
def renBTC(Token, faucet):
    return Token.deploy("renBTC Token", "renBTC", 18, 1e21, {'from': faucet})
@pytest.fixture(scope="module")
def LPBTC(Token, faucet):
    return Token.deploy("LPBTC Token", "LPBTC", 18, 1e21, {'from': faucet})

@pytest.fixture(scope="module")
def USDT(Token, faucet):
    return Token.deploy("USDT Token", "USDT", 18, 1e21, {'from': faucet})
@pytest.fixture(scope="module")
def USDC(Token, faucet):
    return Token.deploy("USDC Token", "USDC", 18, 1e21, {'from': faucet})
@pytest.fixture(scope="module")
def TUSD(Token, faucet):
    return Token.deploy("TUSD Token", "TUSD", 18, 1e21, {'from': faucet})
@pytest.fixture(scope="module")
def DAI(Token, faucet):
    return Token.deploy("DAI Token", "DAI", 18, 1e21, {'from': faucet})
@pytest.fixture(scope="module")
def LPUSD(Token, faucet):
    return Token.deploy("LPUSD Token", "LPUSD", 18, 1e21, {'from': faucet})

@pytest.fixture(scope="module")
def WETH(Token, faucet):
    return Token.deploy("WETH Token", "WETH", 18, 1e21, {'from': faucet})
@pytest.fixture(scope="module")
def WETH1(Token, faucet):
    return Token.deploy("WETH1 Token", "WETH1", 18, 1e21, {'from': faucet})
@pytest.fixture(scope="module")
def LPETH(Token, faucet):
    return Token.deploy("LPETH Token", "LPETH", 18, 1e21, {'from': faucet})

@pytest.fixture(scope="module")
def usdLPToken(admin, USDLPToken):
    return USDLPToken.deploy(USD_LP_TOKEN_NAME, USD_LP_TOKEN_SYMBOL, USD_LP_TOKEN_DECIMALS, USD_LP_TOKEN_SUPPLY, {'from': admin})
@pytest.fixture(scope="module")
def btcLPToken(admin, BTCLPToken):
    return BTCLPToken.deploy(BTC_LP_TOKEN_NAME, BTC_LP_TOKEN_SYMBOL, BTC_LP_TOKEN_DECIMALS, BTC_LP_TOKEN_SUPPLY, {'from': admin})
@pytest.fixture(scope="module")
def ethLPToken(admin, ETHLPToken):
    return ETHLPToken.deploy(ETH_LP_TOKEN_NAME, ETH_LP_TOKEN_SYMBOL, ETH_LP_TOKEN_DECIMALS, ETH_LP_TOKEN_SUPPLY, {'from': admin})

@pytest.fixture(scope="module")
def usdPoolGauge(minter, admin, usdLPToken, gauge_controller, USDPoolGauge):
    r = USDPoolGauge.deploy(usdLPToken.address, minter, {'from': admin})
    gauge_controller.add_gauge(r.address, 0, 1)
    return r
@pytest.fixture(scope="module")
def btcPoolGauge(minter, admin, btcLPToken, gauge_controller, BTCPoolGauge):
    r = BTCPoolGauge.deploy(btcLPToken.address, minter, {'from': admin})
    gauge_controller.add_gauge(r.address, 1, 1)
    return r
@pytest.fixture(scope="module")
def ethPoolGauge(minter, admin, ethLPToken, gauge_controller, ETHPoolGauge):
    r = ETHPoolGauge.deploy(ethLPToken.address, minter, {'from': admin})
    gauge_controller.add_gauge(r.address, 1, 1)
    return r

@pytest.fixture(scope="module")
def btcPool(BTCPoolDelegator, admin, wBTC, sBTC, renBTC, LPBTC):
    return BTCPoolDelegator.deploy(admin,
        [wBTC.address, sBTC.address, renBTC.address],
        LPBTC.address, A_BTC, _init_fee_BTC, _admin_fee_BTC, {'from': admin})

@pytest.fixture(scope="module")
def usdPool(USDPoolDelegator, admin, USDT, USDC, TUSD, DAI, LPUSD):
    return USDPoolDelegator.deploy(
        [USDT.address, USDC.address, TUSD.address, DAI.address],
        [USDT.address, USDC.address, TUSD.address, DAI.address],
        LPUSD.address, A_USD, _init_fee_USD, {'from': admin})

@pytest.fixture(scope="module")
def ethPool(ETHPoolDelegator, admin, WETH, WETH1, LPETH):
    return ETHPoolDelegator.deploy(admin,
        [WETH.address, WETH1.address],
        LPETH.address, A_ETH, _init_fee_ETH, _admin_fee_ETH, {'from': admin})

@pytest.fixture(scope="module")
def usdSwap(Swap, MathUtils, SwapUtils, admin, USDT, USDC, TUSD, DAI):
    MathUtils.deploy({'from': admin})
    SwapUtils.deploy({'from': admin})
    return Swap.deploy(
        [USDT.address, USDC.address, TUSD.address, DAI.address],
        [18, 18, 18, 18],
        'USD Liquidity',
        'USDLP',
        50,  # a
        70,  # a2
        SWAP_FEE,
        0,   # admin fee
        0,   # withdraw fee
        {'from': admin})

@pytest.fixture(scope="module")
def usdSwapPoolGauge(minter, admin, usdSwap, gauge_controller, USDPoolGauge):
    r = USDPoolGauge.deploy(usdSwap.swapStorage()['lpToken'], minter, {'from': admin})
    gauge_controller.add_gauge(r.address, 0, 1)
    return r
