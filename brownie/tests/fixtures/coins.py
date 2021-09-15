import pytest
from brownie import ETH_ADDRESS, ZERO_ADDRESS, ERC20Mock, ERC20MockNoReturn
from brownie_tokens import MintableForkToken
from conftest import WRAPPED_COIN_METHODS

# public fixtures - these can be used when testing


@pytest.fixture(scope="module")
def USDT(ERC20Mock, admin):
    return ERC20Mock.deploy("USDT Token", "USDT", 18, {'from': admin})


@pytest.fixture(scope="module")
def USDC(ERC20Mock, admin):
    return ERC20Mock.deploy("USDC Token", "USDC", 18, {'from': admin})


@pytest.fixture(scope="module")
def TUSD(ERC20Mock, admin):
    return ERC20Mock.deploy("TUSD Token", "TUSD", 18, {'from': admin})


@pytest.fixture(scope="module")
def DAI(ERC20Mock, admin):
    return ERC20Mock.deploy("DAI Token", "DAI", 18, {'from': admin})


@pytest.fixture(scope="module")
def coins(DAI, USDC):
    return [DAI, USDC]


@pytest.fixture(scope="module")
def decimals(coins):
    return [coin.decimals() for coin in coins]


@pytest.fixture(scope="module")
def pool_token(project, alice, pool_data):
    return _pool_token(project, alice, pool_data)


@pytest.fixture(scope="module")
def base_pool_token(project, charlie, base_pool_data, is_forked):
    if base_pool_data is None:
        return
    if is_forked:
        return _MintableTestToken(base_pool_data["lp_token_address"], base_pool_data)

    # we do some voodoo here to make the base LP tokens work like test ERC20's
    # charlie is the initial liquidity provider, he starts with the full balance
    def _mint_for_testing(target, amount, tx=None):
        token.transfer(target, amount, {"from": charlie})

    token = _pool_token(project, charlie, base_pool_data)
    token._mint_for_testing = _mint_for_testing
    return token


# private API below


class _MintableTestToken(MintableForkToken):
    def __init__(self, address, pool_data=None):
        super().__init__(address)

        # standardize mint / rate methods
        if pool_data is not None and "wrapped_contract" in pool_data:
            fn_names = WRAPPED_COIN_METHODS[pool_data["wrapped_contract"]]
            for target, attr in fn_names.items():
                if hasattr(self, attr) and target != attr:
                    setattr(self, target, getattr(self, attr))


def _deploy_wrapped(project, alice, pool_data, idx, underlying, aave_lending_pool):
    coin_data = pool_data["coins"][idx]
    fn_names = WRAPPED_COIN_METHODS[pool_data["wrapped_contract"]]
    deployer = getattr(project, pool_data["wrapped_contract"])

    decimals = coin_data["wrapped_decimals"]
    name = coin_data.get("name", f"Coin {idx}")
    symbol = coin_data.get("name", f"C{idx}")

    if pool_data["wrapped_contract"] == "ATokenMock":
        contract = deployer.deploy(
            name, symbol, decimals, underlying, aave_lending_pool, {"from": alice}
        )
    else:
        contract = deployer.deploy(name, symbol, decimals, underlying, {"from": alice})

    for target, attr in fn_names.items():
        if target != attr:
            setattr(contract, target, getattr(contract, attr))
    if coin_data.get("withdrawal_fee"):
        contract._set_withdrawal_fee(coin_data["withdrawal_fee"], {"from": alice})

    return contract


def _underlying(alice, project, pool_data, is_forked, base_pool_token):
    coins = []

    if is_forked:
        for data in pool_data["coins"]:
            if data.get("underlying_address") == ETH_ADDRESS:
                coins.append(ETH_ADDRESS)
            else:
                coins.append(
                    _MintableTestToken(
                        data.get("underlying_address", data.get("wrapped_address")), pool_data
                    )
                )
    else:
        for i, coin_data in enumerate(pool_data["coins"]):
            if coin_data.get("underlying_address") == ETH_ADDRESS:
                coins.append(ETH_ADDRESS)
                continue
            if coin_data.get("base_pool_token"):
                coins.append(base_pool_token)
                continue
            if not coin_data.get("decimals"):
                contract = _deploy_wrapped(project, alice, pool_data, i, ZERO_ADDRESS, ZERO_ADDRESS)
            else:
                decimals = coin_data["decimals"]
                deployer = ERC20MockNoReturn if coin_data["tethered"] else ERC20Mock
                contract = deployer.deploy(
                    f"Underlying Coin {i}", f"UC{i}", decimals, {"from": alice}
                )
            coins.append(contract)

    return coins


def _pool_token(project, alice, pool_data):
    name = pool_data["name"]
    deployer = getattr(project, pool_data["lp_contract"])
    args = [f"Curve {name} LP Token", f"{name}CRV", 18, 0][: len(deployer.deploy.abi["inputs"])]
    return deployer.deploy(*args, {"from": alice})


# private fixtures used for setup in other fixtures - do not use in tests!


@pytest.fixture(scope="module")
def _underlying_coins(
    alice, project, pool_data, is_forked, base_pool_token, _add_base_pool_liquidity
):
    return _underlying(alice, pool_data, is_forked, base_pool_token)


@pytest.fixture(scope="module")
def _base_coins(alice, base_pool_data, is_forked):
    if base_pool_data is None:
        return []
    return _underlying(alice, base_pool_data, is_forked, None)
