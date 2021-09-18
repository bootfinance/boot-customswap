import brownie
import pytest
from brownie import chain

pytestmark = [
    pytest.mark.usefixtures("add_initial_liquidity"),
]


@pytest.mark.itercoins("idx")
@pytest.mark.parametrize("rate_mod", [0.9, 0.99, 1.01, 1.1])
def test_amount_received(chain, alice, initial_amounts, swap, coins, decimals, pool_token, idx, rate_mod):
    pool_token.approve(swap, initial_amounts[idx], {"from": alice})
    swap.removeLiquidityOneToken(initial_amounts[idx], idx, 0, chain.time() + 60, {"from": alice})
    balance = coins[idx].balanceOf(alice)
    assert 10 ** decimals[idx] // rate_mod <= balance <= initial_amounts[idx]


@pytest.mark.itercoins("idx")
@pytest.mark.parametrize("divisor", [42, 5, 2])
def test_lp_token_balance(alice, swap, pool_token, initial_amounts, n_coins, base_amount, idx, divisor):
    amount = pool_token.balanceOf(alice) // divisor
    pool_token.approve(swap, amount, {"from": alice})
    swap.removeLiquidityOneToken(amount, idx, 0, chain.time() + 60, {"from": alice})
    assert pool_token.balanceOf(alice) == n_coins * base_amount * 10 ** 18 - amount


@pytest.mark.itercoins("idx")
@pytest.mark.parametrize("rate_mod", [0.9, 1.1])
def test_expected_vs_actual(
    chain, alice, swap, coins, pool_token, n_coins, idx, rate_mod, base_amount
):
    amount = pool_token.balanceOf(alice) // 10
    expected = swap.calculateRemoveLiquidityOneToken(alice, amount, idx)
    pool_token.approve(swap, amount, {"from": alice})
    swap.removeLiquidityOneToken(amount, idx, 0, chain.time() + 60, {"from": alice})
    assert coins[idx].balanceOf(alice) == expected
    assert pool_token.balanceOf(alice) == n_coins * 10 ** 18 * base_amount - amount


@pytest.mark.itercoins("idx")
def test_amount_exceeds_balance(bob, swap, coins, pool_token, idx):
    with brownie.reverts():
        swap.removeLiquidityOneToken(1, idx, 0, chain.time() + 60, {"from": bob})


def test_above_n_coins(alice, swap, coins, n_coins):
    with brownie.reverts():
        swap.removeLiquidityOneToken(1, n_coins, 0, chain.time() + 60, {"from": alice})


@pytest.mark.itercoins("idx")
def test_event(alice, bob, swap, pool_token, idx, coins):
    amount = 10 ** 18
    pool_token.transfer(bob, amount, {"from": alice})
    pool_token.approve(swap, amount, {"from": bob})
    tx = swap.removeLiquidityOneToken(amount, idx, 0, chain.time() + 60, {"from": bob})

    event = tx.events["RemoveLiquidityOne"]
    assert event["provider"] == bob
    assert event["lpTokenAmount"] == 10 ** 18

    coin = coins[idx]
    assert coin.balanceOf(bob) == event["tokensBought"]


def test_cannot_remove_all_sparse_liquidity_in_one_coin(alice, swap, pool_token):
    amount = pool_token.balanceOf(alice)
    assert amount == pool_token.totalSupply()
    pool_token.approve(swap, amount, {"from": alice})
    with brownie.reverts():
        swap.removeLiquidityOneToken(amount, 0, 0, chain.time() + 60, {"from": alice})


def test_can_remove_all_liquidity_share_in_one_coin(alice, bob, mint_bob, approve_bob, swap, pool_token, initial_amounts):
    swap.addLiquidity(initial_amounts, 0, chain.time() + 60, {"from": bob})
    amount = pool_token.balanceOf(bob)
    assert amount < pool_token.totalSupply()
    pool_token.approve(swap, amount, {"from": bob})
    swap.removeLiquidityOneToken(amount, 0, 0, chain.time() + 60, {"from": bob})
