// import { Allowlist } from "../../build/typechain/Allowlist"
// import AllowlistArtifact from "../../build/artifacts/contracts/Allowlist.sol/Allowlist.json"
import { BigNumber } from "@ethersproject/bignumber"
// import { BigNumber} from "ethers"

import { GenericERC20 } from "../../build/typechain/GenericERC20"
import GenericERC20Artifact from "../../build/artifacts/contracts/helper/GenericERC20.sol/GenericERC20.json"
import { MathUtils } from "../../build/typechain/MathUtils"
import MathUtilsArtifact from "../../build/artifacts/contracts/MathUtils.sol/MathUtils.json"
import { Swap } from "../../build/typechain/Swap"
import SwapArtifact from "../../build/artifacts/contracts/Swap.sol/Swap.json"
import { SwapUtils } from "../../build/typechain/SwapUtils"
import SwapUtilsArtifact from "../../build/artifacts/contracts/SwapUtils.sol/SwapUtils.json"
import { deployContract } from "ethereum-waffle"
import { deployContractWithLibraries } from "../../test/testUtils"
import { ethers } from "hardhat"
import { SignerWithAddress } from "@nomiclabs/hardhat-ethers/dist/src/signer-with-address"
var Web3 = require('web3');

const INITIAL_A_VALUE = 200
const INITIAL_A2_VALUE = 250
const SWAP_FEE = 4e6 // 4bps
const ADMIN_FEE = 0
const WITHDRAW_FEE = 0
const USD_LP_TOKEN_NAME = "USD LP Token Name"
const USD_LP_TOKEN_SYMBOL = "USD LP Token Symbol"

// Multisig address to own the btc swap pool
// List of signers can be found here: https://docs.saddle.finance/faq#who-controls-saddles-admin-keys
// https://gnosis-safe.io/app/#/safes/0x186B2E003Aa42C9Df56BBB643Bb9550D1a45a360/settings
const MULTISIG_ADDRESS = "0x186B2E003Aa42C9Df56BBB643Bb9550D1a45a360"

// To run this script and deploy the contracts on the mainnet:
//    npx hardhat run deployment/onchain/swap-mainnet.ts --network mainnet
//
// To verify the source code on etherscan:
//    npx hardhat verify --network mainnet DEPLOYED_CONTRACT_ADDRESS [arg0, arg1, ...]

async function deploySwap(): Promise<void> {
  const [deployer]: SignerWithAddress[] = await ethers.getSigners()
  console.log(`Deploying with ${deployer.address}`)

  // Deploy USDT token
  const USDT = (await deployContract(
    deployer,
    GenericERC20Artifact,
    ["USDT Token", "USDT", "18"],
  )) as GenericERC20
  await USDT.deployed()
  console.log(`USDT token address: ${USDT.address}`)

  // Deploy USDC token
  const USDC = (await deployContract(
    deployer,
    GenericERC20Artifact,
    ["USDC Token", "USDC", "18"],
  )) as GenericERC20
  await USDC.deployed()
  console.log(`USDC token address: ${USDC.address}`)

  // Deploy USDC token
/*    const TUSD = (await deployContract(
        deployer,
        GenericERC20Artifact,
        ["TUSD Token", "TUSD", "18"],
      )) as GenericERC20
      await TUSD.deployed()
      console.log(`USDC token address: ${TUSD.address}`)
*/
  // Deploy DAI token
/*  const DAI = (await deployContract(
    deployer,
    GenericERC20Artifact,
    ["DAI Token", "DAI", "18"],
  )) as GenericERC20
  await USDC.deployed()
  console.log(`DAI token address: ${DAI.address}`)
*/
  // Mint 100 M = 1e26 FRAX tokens
  // await fraxToken.mint(deployer.address, String(BigNumber.from(String(1e26))))
  await USDT.mint(deployer.address, BigNumber.from("100000000000000000000000000"))

  // Mint 100 M = 1e26 FXS tokens
  // await fxsToken.mint(deployer.address, String(BigNumber.from(String(1e26))))
  await USDC.mint(deployer.address, BigNumber.from("100000000000000000000000000"))
  // await DAI.mint(deployer.address, BigNumber.from("100000000000000000000000000"))
  // await TUSD.mint(deployer.address, BigNumber.from("100000000000000000000000000"))

  // for minting to multiple addresses
  // await asyncForEach([deployer, user1, user2], async (signer) => {
  //   const address = await signer.getAddress()
  //   await fraxToken.mint(address, String(1e26))
  //   await fxsToken.mint(address, String(1e26))
  // })


  // Swap.sol constructor parameter values
  const TOKEN_ADDRESSES = [
    USDT.address, 
    USDC.address/*, 
    TUSD.address,
    DAI.address*/
  ]

  // Deploy Allowlist
  // Estimated deployment cost = 0.00081804 * gwei
/*  const allowlist = (await deployContract(
    deployer,
    AllowlistArtifact,
    // ["0xca0f8c7ee1addcc5fce6a7c989ba3f210db065c36c276b71b8c8253a339318a3"], // test merkle root https://github.com/saddle-finance/saddle-test-addresses
    ["0xc799ec3a26ef7b4c295f6f02d1e6f65c35cef24447ff343076060bfc0eafb24e"], // production merkle root
  )) as Allowlist
  await allowlist.deployed()
  console.log(`Allowlist address: ${allowlist.address}`)
*/
  // Deploy MathUtils
  const mathUtils = (await deployContract(
    deployer,
    MathUtilsArtifact,
  )) as MathUtils
  await mathUtils.deployed()
  console.log(`mathUtils address: ${mathUtils.address}`)

  // Deploy SwapUtils with MathUtils library
  const swapUtils = (await deployContractWithLibraries(
    deployer,
    SwapUtilsArtifact,
    {
      MathUtils: mathUtils.address,
    },
  )) as SwapUtils
  await swapUtils.deployed()
  console.log(`swapUtils address: ${swapUtils.address}`)

  // Deploy Swap with SwapUtils library
  const swapConstructorArgs = [
    TOKEN_ADDRESSES,
    [18, 18/*, 18, 18*/],
    USD_LP_TOKEN_NAME,
    USD_LP_TOKEN_SYMBOL,
    INITIAL_A_VALUE,
    INITIAL_A2_VALUE,
    SWAP_FEE,
    ADMIN_FEE,
    WITHDRAW_FEE,
    Web3.utils.toWei('1', 'ether')/*
    allowlist.address,*/
  ]

  console.log(swapConstructorArgs)

  // Deploy USD swap
  // Estimated deployment cost = 0.004333332 * gwei
  const USDSwap = (await deployContractWithLibraries(
    deployer,
    SwapArtifact,
    { SwapUtils: swapUtils.address },
    swapConstructorArgs,
  )) as Swap
  await USDSwap.deployed()

  // console.log("USD swap deployed")

  // Set limits for deposits
  // Total supply limit = 150 FRAX
/*  await allowlist.setPoolCap(
    fraxSwap.address,
    BigNumber.from(10).pow(18).mul(150),
  )
*/  
  // Individual deposit limit = 1 FRAX
/*  await allowlist.setPoolAccountLimit(
    fraxSwap.address,
    BigNumber.from(10).pow(18),
  )
*/
  // await fraxSwap.deployed()
  const USDLpToken = (await USDSwap.swapStorage()).lpToken

  console.log(`Tokenized USD Swap address: ${USDSwap.address}`)
  console.log(`Tokenized USD Swap token address: ${USDLpToken}`)

  // Transfer the ownership of the frax/fxs swap and the allowlist to the multisig
  //await USDLpToken.transferOwnership(MULTISIG_ADDRESS)
  // await allowlist.transferOwnership(MULTISIG_ADDRESS)
/*   console.log(
    // `Transferred the ownership of the FRAX swap contract and the allowlist to multisig: ${MULTISIG_ADDRESS}`,
    `Transferred the ownership of the FRAX/FXS swap contract to multisig: ${MULTISIG_ADDRESS}`,
  ) */
}

deploySwap().then(() => {
  console.log("Successfully deployed contracts to rinkeby network...")
})
