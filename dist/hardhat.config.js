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
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
var __generator = (this && this.__generator) || function (thisArg, body) {
    var _ = { label: 0, sent: function() { if (t[0] & 1) throw t[1]; return t[1]; }, trys: [], ops: [] }, f, y, t, g;
    return g = { next: verb(0), "throw": verb(1), "return": verb(2) }, typeof Symbol === "function" && (g[Symbol.iterator] = function() { return this; }), g;
    function verb(n) { return function (v) { return step([n, v]); }; }
    function step(op) {
        if (f) throw new TypeError("Generator is already executing.");
        while (_) try {
            if (f = 1, y && (t = op[0] & 2 ? y["return"] : op[0] ? y["throw"] || ((t = y["return"]) && t.call(y), 0) : y.next) && !(t = t.call(y, op[1])).done) return t;
            if (y = 0, t) op = [op[0] & 2, t.value];
            switch (op[0]) {
                case 0: case 1: t = op; break;
                case 4: _.label++; return { value: op[1], done: false };
                case 5: _.label++; y = op[1]; op = [0]; continue;
                case 7: op = _.ops.pop(); _.trys.pop(); continue;
                default:
                    if (!(t = _.trys, t = t.length > 0 && t[t.length - 1]) && (op[0] === 6 || op[0] === 2)) { _ = 0; continue; }
                    if (op[0] === 3 && (!t || (op[1] > t[0] && op[1] < t[3]))) { _.label = op[1]; break; }
                    if (op[0] === 6 && _.label < t[1]) { _.label = t[1]; t = op; break; }
                    if (t && _.label < t[2]) { _.label = t[2]; _.ops.push(op); break; }
                    if (t[2]) _.ops.pop();
                    _.trys.pop(); continue;
            }
            op = body.call(thisArg, _);
        } catch (e) { op = [6, e]; y = 0; } finally { f = t = 0; }
        if (op[0] & 5) throw op[1]; return { value: op[0] ? op[1] : void 0, done: true };
    }
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
var config_1 = require("hardhat/config");
var dotenv_1 = __importDefault(require("dotenv"));
/* This loads the variables in your .env file to `process.env` */
dotenv_1.default.config();
// const chainIds = {
//   ganache: 1337,
//   goerli: 5,
//   hardhat: 31337,
//   kovan: 42,
//   mainnet: 1,
//   rinkeby: 4,
//   ropsten: 3,
// };
// const ETHERSCAN_API_KEY = process.env.ETHERSCAN_API_KEY || "";
var INFURA_API_KEY = process.env.INFURA_API_KEY || "";
var DEPLOYER_PRIVATE_KEY_RINKEBY = process.env.DEPLOYER_PRIVATE_KEY_RINKEBY || "";
// This is a sample Hardhat task. To learn how to create your own go to
// https://hardhat.org/guides/create-task.html
// Usage: `$ npx hardhat accounts` for localhost
config_1.task("accounts", "Prints the list of accounts", function (args, hre) { return __awaiter(void 0, void 0, void 0, function () {
    var accounts, _i, accounts_1, account, _a, _b;
    return __generator(this, function (_c) {
        switch (_c.label) {
            case 0: return [4 /*yield*/, hre.ethers.getSigners()];
            case 1:
                accounts = _c.sent();
                _i = 0, accounts_1 = accounts;
                _c.label = 2;
            case 2:
                if (!(_i < accounts_1.length)) return [3 /*break*/, 5];
                account = accounts_1[_i];
                _b = (_a = console).log;
                return [4 /*yield*/, account.getAddress()];
            case 3:
                _b.apply(_a, [_c.sent()]);
                _c.label = 4;
            case 4:
                _i++;
                return [3 /*break*/, 2];
            case 5: return [2 /*return*/];
        }
    });
}); });
// function createTestnetConfig(network: keyof typeof chainIds): NetworkUserConfig {
//   const url: string = "https://" + network + ".infura.io/v3/" + INFURA_API_KEY;
//   return {
//     accounts: {
//       count: 10,
//       initialIndex: 0,
//       // mnemonic: MNEMONIC,
//       path: "m/44'/60'/0'/0",
//     },
//     chainId: chainIds[network],
//     url,
//   };
// }
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
        rinkeby: {
            url: "https://rinkeby.infura.io/v3/" + INFURA_API_KEY,
            chainId: 4,
            accounts: ["0x" + DEPLOYER_PRIVATE_KEY_RINKEBY],
        },
        // rinkeby: createTestnetConfig("rinkeby"),
    },
    paths: {
        sources: "contracts",
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
        enabled: process.env.REPORT_GAS ? true : false,
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