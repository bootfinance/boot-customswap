import pytest
from brownie import chain
from brownie.test import given, strategy
from conftest import MAX_A_CHANGE, MIN_RAMP_TIME, ONE_DAY, A_PRECISION


@given(st_A=strategy("uint", min_value=0, max_value=3))
def test_path_independence(
    swap_10,
    swap_100,
    swap_10_100,
    swap_100_10,
    admin,
    alice,
    mint_alice,
    bob,
    mint_bob,
    coins,
    decimals,
    base_amount,
    initial_amounts,
    LPToken,
    st_A
):
    swap = [swap_10, swap_100, swap_10_100, swap_100_10][st_A]
    for coin in coins:
        coin.approve(swap, 2 ** 256 - 1, {"from": alice})
        coin.approve(swap, 2 ** 256 - 1, {"from": bob})

    swap.setSwapFee(0)
    swap.setAdminFee(0)

    swap.addLiquidity(initial_amounts, 0, chain.time() + 60, {"from": alice})

    amount = 10 ** decimals[0]

    def price():
        return swap.calculateSwap(0, 1, amount // 100) / 10**decimals[1]

    before = price()
    received = swap.swap(0, 1, amount, 0, chain.time() + 60, {"from": bob}).return_value
    received = swap.swap(1, 0, received, 0, chain.time() + 60, {"from": bob}).return_value
    after = price()
    assert abs(after - before) < 0.00001
    assert amount - received <= 1

    swap.swap(1, 0, amount // 2, 0, chain.time() + 60, {"from": bob})

    before = price()
    received = swap.swap(1, 0, amount // 10, 0, chain.time() + 60, {"from": bob}).return_value
    received += swap.swap(1, 0, amount - (amount // 10), 0, chain.time() + 60, {"from": bob}).return_value
    p1 = price()
    received = swap.swap(0, 1, received, 0, chain.time() + 60, {"from": bob}).return_value
    after = price()
    assert abs(after - before) < 0.00001
    assert amount >= received
    print(before, p1, after, received)

    before = price()
    received = swap.swap(1, 0, amount - (amount // 10), 0, chain.time() + 60, {"from": bob}).return_value
    received += swap.swap(1, 0, amount // 10, 0, chain.time() + 60, {"from": bob}).return_value
    p2 = price()
    received = swap.swap(0, 1, received, 0, chain.time() + 60, {"from": bob}).return_value
    after = price()
    assert abs(after - before) < 0.00001
    assert amount >= received
    print(before, p2, after, received)

    assert abs(p2 - p1) / 10 ** decimals[0] < 0.00001