// SPDX-License-Identifier: MIT

pragma solidity 0.6.12;

import "@openzeppelin/contracts/math/SafeMath.sol";
import "@openzeppelin/contracts/token/ERC20/SafeERC20.sol";
import "@openzeppelin/contracts/utils/ReentrancyGuard.sol";
import "./OwnerPausable.sol";
import "./SwapUtils.sol";
import "./MathUtils.sol";
import "./hardhat/console.sol";
import "./Swap.sol";

/**
 * @title SwapV2 - An extension of a StableSwap implementation in solidity - builds on the Swap.so parent 
 * contract to add the ability to manipulate targetPrice, A, and A2 post contract deployment.
 * @notice This contract is responsible for custody of closely pegged assets (eg. group of stablecoins)
 * and automatic market making system. Users become an LP (Liquidity Provider) by depositing their tokens
 * in desired ratios for an exchange of the pool token that represents their share of the pool.
 * Users can burn pool tokens and withdraw their share of token(s).
 *
 * Each time a swap between the pooled tokens happens, a set fee incurs which effectively gets
 * distributed to the LPs.
 *
 * In case of emergencies, admin can pause additional deposits, swaps, or single-asset withdraws - which
 * stops the ratio of the tokens in the pool from changing.
 * Users can always withdraw their tokens via multi-asset withdraws.
 *
 * @dev Most of the logic is stored as a library `SwapUtils` for the sake of reducing contract's
 * deployment size.
 */
contract SwapV2 is Swap {
    using SafeERC20 for IERC20;
    using SafeMath for uint256;
    using MathUtils for uint256;
    using SwapUtils for SwapUtils.Swap;
    using SwapUtils for SwapUtils.TargetPrice;

    /**
     * @notice Deploys this Swap contract with given parameters as default
     * values. This will also deploy a LPToken that represents users
     * LP position. The owner of LPToken will be this contract - which means
     * only this contract is allowed to mint new tokens.
     *
     * @param _pooledTokens an array of ERC20s this pool will accept
     * @param decimals the decimals to use for each pooled token,
     * eg 8 for WBTC. Cannot be larger than POOL_PRECISION_DECIMALS
     * @param lpTokenName the long-form name of the token to be deployed
     * @param lpTokenSymbol the short symbol for the token to be deployed
     * @param _a the amplification coefficient * n * (n - 1). See the
     * StableSwap paper for details
     * @param _a2 the amplification coefficient * n * (n - 1). See the
     * StableSwap paper for details
     * @param _fee default swap fee to be initialized with
     * @param _adminFee default adminFee to be initialized with
     * @param _withdrawFee default withdrawFee to be initialized with
     * @param _targetPrice default targetPrice to be initialized with
     */

    //   * @param _allowlist address of allowlist contract for guarded launch
    constructor(
        IERC20[] memory _pooledTokens,
        uint8[] memory decimals,
        string memory lpTokenName,
        string memory lpTokenSymbol,
        uint256 _a,
        uint256 _a2,
        uint256 _fee,
        uint256 _adminFee,
        uint256 _withdrawFee,
        uint256 _targetPrice
        // IAllowlist _allowlist
    ) Swap(_pooledTokens, decimals, lpTokenName, lpTokenSymbol, _a, _a2, _fee, _adminFee, _withdrawFee, _targetPrice) public OwnerPausable() {
        
    }

    /**
     * @notice Start ramping up or down Target price towards given futureTargetPrice and futureTime
     * Checks if the change is too rapid, and commits the new Target price value only when it falls under
     * the limit range.
     * @param futureTargetPrice the new target price to ramp towards
     * @param futureTime timestamp when the new target price should be reached
     */
    function rampTargetPrice(uint256 futureTargetPrice, uint256 futureTime) external onlyOwner {
        swapStorage.tokenPrecisionMultipliers[0] = targetPriceStorage.rampTargetPrice(futureTargetPrice, futureTime);
    }


    /**
     * @notice Start ramping up or down A parameter towards given futureA and futureTime
     * Checks if the change is too rapid, and commits the new A value only when it falls under
     * the limit range.
     * @param futureA the new A to ramp towards
     * @param futureTime timestamp when the new A should be reached
     */
    function rampA(uint256 futureA, uint256 futureTime) external onlyOwner {
        swapStorage.rampA(futureA, futureTime);
    }

    /**
     * @notice Start ramping up or down A2 parameter towards given futureA and futureTime
     * Checks if the change is too rapid, and commits the new A value only when it falls under
     * the limit range.
     * @param futureA the new A2 to ramp towards
     * @param futureTime timestamp when the new A2 should be reached
     */
    function rampA2(uint256 futureA, uint256 futureTime) external onlyOwner {
        swapStorage.rampA2(futureA, futureTime);
    }

    /**
     * @notice Stop ramping Target Price immediately. Reverts if ramp Target Price is already stopped.
     */
    function stopRampTargetPrice() external onlyOwner {
        swapStorage.tokenPrecisionMultipliers[0] = targetPriceStorage.stopRampTargetPrice();
    }


    /**
     * @notice Stop ramping A immediately. Reverts if ramp A is already stopped.
     */
    function stopRampA() external onlyOwner {
        swapStorage.stopRampA();
    }

    /**
     * @notice Stop ramping A2 immediately. Reverts if ramp A2 is already stopped.
     */
    function stopRampA2() external onlyOwner {
        swapStorage.stopRampA2();
    }
}
