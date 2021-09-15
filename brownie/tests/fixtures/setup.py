import pytest
from brownie import chain


@pytest.fixture(scope="module")
def base_amount():
    return 1000000


@pytest.fixture(scope="module")
def initial_amounts(coins, base_amount):
    return [10 ** coin.decimals() * base_amount for coin in coins]


@pytest.fixture(scope="module")
def n_coins(coins):
    return len(coins)


@pytest.fixture(scope="module")
def add_initial_liquidity(alice, mint_alice, approve_alice, coins, swap, initial_amounts):
    _add_liquidity(alice, swap, initial_amounts)


@pytest.fixture(scope="module")
def mint_bob(bob, coins, initial_amounts):
    _mint(bob, coins, initial_amounts)


@pytest.fixture(scope="module")
def approve_bob(bob, swap, coins):
    _approve(bob, swap, coins)


@pytest.fixture(scope="module")
def mint_alice(alice, coins, initial_amounts):
    _mint(alice, coins, initial_amounts)


@pytest.fixture(scope="module")
def approve_alice(alice, swap, coins):
    _approve(alice, swap, coins)


# shared logic for pool and base_pool setup fixtures


def _add_liquidity(acct, swap, amounts):
    swap.addLiquidity(amounts, 0, chain.time() + 60, {"from": acct})


def _mint(acct, coins, amounts):
    for coin, amount in zip(coins, amounts):
        coin._mint_for_testing(acct, amount, {"from": acct})


def _approve(owner, spender, *coins):
    for coin in set(x for i in coins for x in i):
        coin.approve(spender, 2 ** 256 - 1, {"from": owner})


@pytest.fixture(scope="module")
def _add_base_pool_liquidity(
    charlie, base_swap, _base_coins, base_pool_data, base_amount, is_forked
):
    # private fixture to add liquidity to the metapool
    if base_pool_data is None:
        return

    decimals = [i.get("decimals", i.get("wrapped_decimals")) for i in base_pool_data["coins"]]
    initial_amounts = [10 ** i * base_amount * 2 for i in decimals]
    _mint(charlie, _base_coins, initial_amounts, [], [], is_forked)
    _approve(charlie, base_swap, _base_coins)
    _add_liquidity(charlie, base_swap, _base_coins, initial_amounts)
