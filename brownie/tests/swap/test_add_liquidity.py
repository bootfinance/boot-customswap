import brownie
import pytest
from brownie import chain
from brownie.test import given, strategy

pytestmark = pytest.mark.usefixtures("add_initial_liquidity", "mint_bob", "approve_bob")


def test_deadline_not_met(bob, swap, initial_amounts):
    with brownie.reverts("Deadline not met"):
        swap.addLiquidity(initial_amounts, 0, chain.time() - 60, {"from": bob})


def test_add_liquidity(bob, swap, coins, pool_token, initial_amounts, base_amount, n_coins):
    swap.addLiquidity(initial_amounts, 0, chain.time() + 60, {"from": bob})

    for coin, amount in zip(coins, initial_amounts):
        assert coin.balanceOf(bob) == 0
        assert coin.balanceOf(swap) == amount * 2

    assert pool_token.balanceOf(bob) == n_coins * 10 ** 18 * base_amount
    assert pool_token.totalSupply() == n_coins * 10 ** 18 * base_amount * 2


def test_add_with_slippage(bob, swap, pool_token, decimals, n_coins):
    amounts = [10 ** i for i in decimals]
    amounts[0] = int(amounts[0] * 0.99)
    amounts[1] = int(amounts[1] * 1.01)

    swap.addLiquidity(amounts, 0, chain.time() + 60, {"from": bob})

    balance = pool_token.balanceOf(bob) / (n_coins * 10 ** 18)
    assert 0.999 < balance < 1


@given(idx=strategy('uint', min_value=0, max_value=1))
def test_add_one_coin(bob, swap, coins, pool_token, initial_amounts, base_amount, idx, n_coins):
    amounts = [0] * n_coins
    amounts[idx] = initial_amounts[idx]

    swap.addLiquidity(amounts, 0, chain.time() + 60, {"from": bob})

    for i, coin in enumerate(coins):
        assert coin.balanceOf(bob) == initial_amounts[i] - amounts[i]
        assert coin.balanceOf(swap) == initial_amounts[i] + amounts[i]

    balance = pool_token.balanceOf(bob) / (10 ** 18 * base_amount)
    assert 0.99 < balance < 1


def test_insufficient_balance(charlie, swap, coins, decimals, pool_token):
    amounts = [(10 ** i) for i in decimals]

    with brownie.reverts():
        swap.addLiquidity(amounts, 0, chain.time() + 60, {"from": charlie})
        assert pool_token.balanceOf(charlie) == 0


def test_min_amount_too_high(bob, swap, decimals, coins, n_coins):
    amounts = [10 ** i for i in decimals]

    min_amount = (10 ** 18 * n_coins) + 1
    with brownie.reverts():
        swap.addLiquidity(amounts, min_amount, 0, {"from": bob})


def test_min_amount_with_slippage(bob, swap, decimals, coins, n_coins):
    amounts = [10 ** i for i in decimals]
    amounts[0] = int(amounts[0] * 0.99)
    amounts[1] = int(amounts[1] * 1.01)

    with brownie.reverts("Couldn't mint min requested"):
        swap.addLiquidity(amounts, n_coins * 10 ** 18, chain.time() + 60, {"from": bob})


def test_event(bob, swap, pool_token, initial_amounts, coins):
    tx = swap.addLiquidity(initial_amounts, 0, chain.time() + 60, {"from": bob})

    event = tx.events["AddLiquidity"]
    assert event["provider"] == bob
    assert event["tokenAmounts"] == initial_amounts
    assert event["lpTokenSupply"] == pool_token.totalSupply()
