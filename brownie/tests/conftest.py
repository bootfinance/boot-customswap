#!/usr/bin/python3

import pytest
import json
from brownie import chain
import warnings
from pathlib import Path

from brownie._config import CONFIG
from brownie.project.main import get_loaded_projects

pytest_plugins = [
    "fixtures.accounts",
    "fixtures.coins",
    "fixtures.deployments",
    "fixtures.functions",
    "fixtures.setup",
]

# functions in wrapped methods are renamed to simplify common tests

WRAPPED_COIN_METHODS = {
    "ATokenMock": {"get_rate": "_get_rate", "mint": "mint"},
    "cERC20": {"get_rate": "exchangeRateStored", "mint": "mint"},
    "IdleToken": {"get_rate": "tokenPrice", "mint": "mintIdleToken"},
    "renERC20": {"get_rate": "exchangeRateCurrent"},
    "yERC20": {"get_rate": "getPricePerFullShare", "mint": "deposit"},
    "aETH": {"get_rate": "ratio"},
    "rETH": {"get_rate": "getExchangeRate"},
}


@pytest.hookimpl(trylast=True)
def pytest_sessionfinish(session, exitstatus):
    if exitstatus == pytest.ExitCode.NO_TESTS_COLLECTED:
        # because of how tests are filtered in the CI, we treat "no tests collected" as passing
        session.exitstatus = pytest.ExitCode.OK


# isolation setup


@pytest.fixture(autouse=True)
def isolation_setup(fn_isolation):
    pass


SWAP_FEE = 1e7
MAX_UINT256 = 2**256 - 1


@pytest.fixture(scope="module")
def swap(Swap, MathUtils, SwapUtils, coins, decimals, admin):
    MathUtils.deploy({'from': admin})
    SwapUtils.deploy({'from': admin})
    return Swap.deploy(
        coins, #[coin.address for coin in coins],
        decimals,
        'USD Liquidity',
        'USDLP',
        85,     # a
        85,     # a2
        SWAP_FEE,
        0,      # admin fee
        0,      # withdraw fee
        10**18, # Initial Target Price
        {'from': admin})


@pytest.fixture(scope="module")
def pool_token(swap, LPToken):
    return LPToken.at(swap.swapStorage()['lpToken'])
