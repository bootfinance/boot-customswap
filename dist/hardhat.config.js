"use strict";
var __assign = (this && this.__assign) || function () {
    __assign = Object.assign || function(t) {
        for (var s, i = 1, n = arguments.length; i < n; i++) {
            s = arguments[i];
            for (var p in s) if (Object.prototype.hasOwnProperty.call(s, p))
                t[p] = s[p];
        }
        return t;
    };
    return __assign.apply(this, arguments);
};
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
var _a;
Object.defineProperty(exports, "__esModule", { value: true });
require("@nomiclabs/hardhat-ethers");
require("@nomiclabs/hardhat-waffle");
require("@nomiclabs/hardhat-web3");
require("@nomiclabs/hardhat-etherscan");
require("hardhat-gas-reporter");
require("solidity-coverage");
require("hardhat-typechain");
var dotenv_1 = __importDefault(require("dotenv"));
dotenv_1.default.config();
var config = {
    defaultNetwork: "hardhat",
    networks: {
        coverage: {
            url: "http://127.0.0.1:8555",
        },
        // mainnet: {
        //   url: process.env.ALCHEMY_API,
        //   gasPrice: 55 * 1000000000,
        // },
    },
    paths: {
        artifacts: "./build/artifacts",
        cache: "./build/cache",
    },
    solidity: {
        compilers: [
            {
                version: "0.6.12",
                settings: {
                    optimizer: {
                        enabled: true,
                        runs: 10000,
                    },
                },
            },
            {
                version: "0.5.16",
            },
        ],
    },
    typechain: {
        outDir: "./build/typechain/",
        target: "ethers-v5",
    },
    gasReporter: {
        currency: "USD",
        gasPrice: 21,
    },
    mocha: {
        timeout: 200000,
    },
};
if (process.env.ETHERSCAN_API) {
    config = __assign(__assign({}, config), { etherscan: { apiKey: process.env.ETHERSCAN_API } });
}
if (process.env.ACCOUNT_PRIVATE_KEYS) {
    config.networks = __assign(__assign({}, config.networks), { mainnet: __assign(__assign({}, (_a = config.networks) === null || _a === void 0 ? void 0 : _a.mainnet), { accounts: JSON.parse(process.env.ACCOUNT_PRIVATE_KEYS) }) });
}
exports.default = config;
//# sourceMappingURL=hardhat.config.js.map