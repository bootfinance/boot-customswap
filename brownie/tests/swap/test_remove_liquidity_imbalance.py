import brownie
import pytest
from brownie import chain

pytestmark = pytest.mark.usefixtures("add_initial_liquidity")


@pytest.mark.parametrize("divisor", [2, 5, 10])
def test_remove_balanced(
    alice, swap, coins, pool_token, divisor, initial_amounts, n_coins, base_amount
):
    amounts = [i // divisor for i in initial_amounts]
    max_burn = (n_coins * 10 ** 18 * base_amount) // divisor

    pool_token.approve(swap, max_burn + 1, {"from": alice})
    swap.removeLiquidityImbalance(amounts, max_burn + 1, chain.time() + 60, {"from": alice})

    for i, coin in enumerate(coins):
        assert coin.balanceOf(alice) == amounts[i]
        assert coin.balanceOf(swap) == initial_amounts[i] - amounts[i]

    assert abs(pool_token.balanceOf(alice) - (n_coins * 10 ** 18 * base_amount - max_burn)) <= 1
    assert abs(pool_token.totalSupply() - (n_coins * 10 ** 18 * base_amount - max_burn)) <= 1


@pytest.mark.itercoins("idx")
def test_remove_some(
    alice, swap, coins, pool_token, idx, initial_amounts, n_coins, base_amount
):
    amounts = [i // 2 for i in initial_amounts]
    amounts[idx] = 0

    pool_token.approve(swap, n_coins * 10 ** 18 * base_amount, {"from": alice})
    swap.removeLiquidityImbalance(amounts, n_coins * 10 ** 18 * base_amount, chain.time() + 60, {"from": alice})

    for i, coin in enumerate(coins):
        assert coin.balanceOf(alice) == amounts[i]
        assert coin.balanceOf(swap) == initial_amounts[i] - amounts[i]

    actual_balance = pool_token.balanceOf(alice)
    actual_total_supply = pool_token.totalSupply()
    ideal_balance = 10 ** 18 * base_amount * n_coins - 10 ** 18 * base_amount // 2 * (n_coins - 1)

    assert actual_balance == actual_total_supply
    assert ideal_balance * 0.9 < actual_balance < ideal_balance


@pytest.mark.itercoins("idx")
def test_remove_one(
    alice, swap, coins, pool_token, idx, initial_amounts, base_amount, n_coins
):
    amounts = [0] * n_coins
    amounts[idx] = initial_amounts[idx] // 2

    pool_token.approve(swap, n_coins * 10 ** 18 * base_amount, {"from": alice})
    swap.removeLiquidityImbalance(amounts, n_coins * 10 ** 18 * base_amount, chain.time() + 60, {"from": alice})

    for i, coin in enumerate(coins):
        assert coin.balanceOf(alice) == amounts[i]
        assert coin.balanceOf(swap) == initial_amounts[i] - amounts[i]

    actual_balance = pool_token.balanceOf(alice)
    actual_total_supply = pool_token.totalSupply()
    ideal_balance = 10 ** 18 * base_amount * n_coins - 10 ** 18 * base_amount // 2

    assert actual_balance == actual_total_supply
    assert ideal_balance * 0.9 < actual_balance < ideal_balance


@pytest.mark.parametrize("divisor", [1, 2, 10])
def test_exceed_max_burn(
    alice, swap, coins, pool_token, divisor, initial_amounts, base_amount, n_coins
):
    amounts = [i // divisor for i in initial_amounts]
    max_burn = (n_coins * 10 ** 18 * base_amount) // divisor

    with brownie.reverts("tokenAmount > maxBurnAmount"):
        pool_token.approve(swap, max_burn - 1, {"from": alice})
        swap.removeLiquidityImbalance(amounts, max_burn - 1, chain.time() + 60, {"from": alice})


def test_cannot_remove_zero(alice, swap, n_coins):
    with brownie.reverts():
        swap.removeLiquidityImbalance([0] * n_coins, 0, chain.time() + 60, {"from": alice})
    with brownie.reverts():
        swap.removeLiquidityImbalance([0] * n_coins, 1, chain.time() + 60, {"from": alice})


def test_no_totalsupply(alice, swap, pool_token, n_coins):
    pool_token.approve(swap, pool_token.totalSupply(), {"from": alice})
    swap.removeLiquidity(pool_token.totalSupply(), [0] * n_coins, chain.time() + 60, {"from": alice})
    with brownie.reverts():
        swap.removeLiquidityImbalance([0] * n_coins, 0, chain.time() + 60, {"from": alice})


def test_event(alice, bob, swap, pool_token, coins, initial_amounts, n_coins, base_amount):
    pool_token.transfer(bob, pool_token.balanceOf(alice), {"from": alice})
    amounts = [i // 5 for i in initial_amounts]
    max_burn = n_coins * 10 ** 18 * base_amount

    pool_token.approve(swap, max_burn, {"from": bob})
    tx = swap.removeLiquidityImbalance(amounts, max_burn, chain.time() + 60, {"from": bob})

    event = tx.events["RemoveLiquidityImbalance"]
    assert event["provider"] == bob
    assert event["lpTokenSupply"] == pool_token.totalSupply()
    for coin, amount in zip(coins, event["tokenAmounts"]):
        assert coin.balanceOf(bob) == amount
