Navigating the Unknown was an interesting challenge. Very different to what I have seen before so I just asked for help from our good friend ChatGPT.

We get two files, a Setup.sol which contains the code below:

```python
pragma solidity ^0.8.18;

import {Unknown} from "./Unknown.sol";

contract Setup {
    Unknown public immutable TARGET;

    constructor() {
        TARGET = new Unknown();
    }

    function isSolved() public view returns (bool) {
        return TARGET.updated();
    }
}
```

And a Unknown.sol file which contains the code below:

```python
pragma solidity ^0.8.18;


contract Unknown {
    
    bool public updated;

    function updateSensors(uint256 version) external {
        if (version == 10) {
            updated = true;
        }
    }

}
```

They also provide the helpful Readme.md below in order to introduce us to these kinds of challenges:

## Guidelines

The point of this README is to provide some guidance for people who attempt solving a blockchain challenge for the first time.

### Ports

As you have already seen, there are 2 ports provided.

- The one port is the `tcp` port, which is used to retrieve information about connecting to the private chain, such as private key, and the target contract's addresses. You can connect to this one using `netcat`.
- The other port is the `rpc` url. You will need this in order to connect to the private chain.

In order to figure out which one is which, try using `netcat` against both. The one which works is the `tcp` port, while the other one is the `rpc url`.

### Contract Sources

In these challenges, you will meet 2 type of smart contract source files, the `Setup.sol` file and the challenge files.

#### Setup.sol

The `Setup.sol` file contains a single contract, the `Setup`. As the name indicates, inside this contract all the initialization actions are happening. There will typically be 3 functions:

- `constructor()`: It is called automatically once when the contract is deployed and cannot be called again. It contains all the initialization actions of the challenge, like deploying the challenge contracts and any other actions needed.
- `TARGET()`: It returns the address of the challenge contract.
- `isSolved()`: This function contains the final objective of the challenge. It returns `true` if the challenge is solved, `false` otherwise. By reading its source, one is able to figure out what the objective is.

#### Other source files

All the other files provided are the challenge contracts. You will only have to interact with them to solve the challenge. Try analyzing their source carefully and figure out how to break them, following the objective specified in `isSolved` function of the `Setup` contract.

### Interacting with the blockchain

In order to interact wth the smart contracts in the private chain, you will need:

- A private key with some ether. We provide it via the tcp endpoint.
- The target contract's address. We provide both the Setup's and the Target's addresses.
- The rpc url, which can be found using what described earlier.

After having collected all the connection information, then you can either use `web3py` or `web3js` to perform function calls in the smart contracts or any other actions needed. You can find some useful tutorials about both with a little googlin'.
An even handier way is using a tool like `foundry-rs`, which is an easy-to-use cli utility to interact with the blockchain, but there are less examples online than the other alternatives.


# Solution

I connected to the TCP endpoint to get the connection information:
![image](https://user-images.githubusercontent.com/80063008/227478323-75fdf59f-8e54-46b8-a36c-8dbd953bee35.png)

I passed all this information to ChatGPT and it provided code very similar to the solution below. I just had to fix a couple syntax issues since ChatGPT seemed to be using an older version of web3.

```python
from web3 import Web3

# Connect to the local blockchain
rpc_url = "http://144.126.196.198:31130"
web3 = Web3(Web3.HTTPProvider(rpc_url))

# Set the account that will send the transaction
private_key = "0x8486566dfbde7605e5a06ec2422eb7085bf80132ec836ecf2379b432a6fa8ff6"
account = web3.eth.account.from_key(private_key)

# Load the Unknown contract interface
unknown_address = "0x4d5DF02772B413697A808A67CC434ccF27EF83E7"
unknown_abi = [{"inputs":[{"internalType":"uint256","name":"version","type":"uint256"}],"name":"updateSensors","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"updated","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"}]
unknown_contract = web3.eth.contract(address=unknown_address, abi=unknown_abi)

# Call the updateSensors function
version = 10
tx_hash = unknown_contract.functions.updateSensors(version).transact({"from": account.address})
receipt = web3.eth.wait_for_transaction_receipt(tx_hash)

# Check the updated variable
updated = unknown_contract.functions.updated().call()
print(f"Updated: {updated}")
```

I ran the script and got confirmation that the contract was updated:

![image](https://user-images.githubusercontent.com/80063008/227478444-cc83dda6-6b67-4aee-af97-5c3e54201bf3.png)

After updating the contract, we connect back the TCP endpoint and get the flag:

![image](https://user-images.githubusercontent.com/80063008/227478591-1d88dc0c-c91f-43f0-8150-08fe5ecbc644.png)

HTB{9P5_50FtW4R3_UPd4t3D}