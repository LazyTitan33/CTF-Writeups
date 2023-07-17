### Challenge description
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/9db1df81-6c8a-4644-9dbf-f0ce6ef107c4)

For this challenge, we receive 3 files:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/15909328-94dd-45a1-8bc4-7cb7acfb3d47)

The Contract.sol has the following content:

```python
// SPDX-License-Identifier: UNLICENSED
pragma solidity 0.8.18;


contract Contract {
    
    bool public signed;

    function signContract(uint256 signature) external {
        if (signature == 1337) {
            signed = true;
        }
    }

}
```
The Setup.sol file contains the following:

```python
// SPDX-License-Identifier: UNLICENSED
pragma solidity 0.8.18;

import {Contract} from "./Contract.sol";

contract Setup {
    Contract public immutable TARGET;

    constructor() {
        TARGET = new Contract();
    }

    function isSolved() public view returns (bool) {
        return TARGET.signed();
    }
}
```
The challenge allows us to spawn two IPs and ports. One of them provides us with some blockchain connection information:
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/b4c564fe-856e-489a-8393-5480b69d9e75)

This is basically a copy+paste from the HTB CyberApocalypse 2023 challenge called [Navigating the Unknown](https://github.com/LazyTitan33/CTF-Writeups/blob/main/HTB%20-%20CyberApocalypse_2023/Blockchain/Navigating_the_Unknown.md).

Because of this, I reused my script and changed the addresses and function names:

```python
from web3 import Web3

# Connect to the local blockchain
rpc_url = "http://94.237.55.114:41746"
web3 = Web3(Web3.HTTPProvider(rpc_url))

# Set the account that will send the transaction
private_key = "0x2a4e0fdeb8a4fab3bcd58c2f04c7b3e234f9ca30f3a3035679fb6dc154e6fcd4"
account = web3.eth.account.from_key(private_key)

# Load the Unknown contract interface
unknown_address = "0x97B1a8abab29598dF887F355fa76e032f68d257e"
unknown_abi = [{"inputs":[{"internalType":"uint256","name":"signature","type":"uint256"}],"name":"signContract","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"signed","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"}]
unknown_contract = web3.eth.contract(address=unknown_address, abi=unknown_abi)

# Call the updateSensors function
signature = 1337
tx_hash = unknown_contract.functions.signContract(signature).transact({"from": account.address})
receipt = web3.eth.wait_for_transaction_receipt(tx_hash)

# Check the signed variable
signed = unknown_contract.functions.signed().call()
print(f"signed: {signed}")
```
We successfully sign the contract:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/47275b1b-1f1c-4bd0-9688-b2d45123a6a1)

Connect back and get the flag:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/d28db0e1-cf68-456e-9569-a73358d31e4e)

HTB{c0n9247u14710n5_y0u_423_kn0w_p427_0f_7h3_734m}

