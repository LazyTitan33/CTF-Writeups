Shooting 101 is the second challenge in the Blockchain category. We receive the `Setup.sol` with the code below:

```python
pragma solidity ^0.8.18;

import {ShootingArea} from "./ShootingArea.sol";

contract Setup {
    ShootingArea public immutable TARGET;

    constructor() {
        TARGET = new ShootingArea();
    }

    function isSolved() public view returns (bool) {
        return TARGET.firstShot() && TARGET.secondShot() && TARGET.thirdShot();
    }
}
```
The second file is called `ShootingArea.sol` and contains the code below:

```python
pragma solidity ^0.8.18;

contract ShootingArea {
    bool public firstShot;
    bool public secondShot;
    bool public thirdShot;

    modifier firstTarget() {
        require(!firstShot && !secondShot && !thirdShot);
        _;
    }

    modifier secondTarget() {
        require(firstShot && !secondShot && !thirdShot);
        _;
    }

    modifier thirdTarget() {
        require(firstShot && secondShot && !thirdShot);
        _;
    }

    receive() external payable secondTarget {
        secondShot = true;
    }

    fallback() external payable firstTarget {
        firstShot = true;
    }

    function third() public thirdTarget {
        thirdShot = true;
    }
}
```

I also solved this with ChatGPT's help but it was much more of a struggle as it kept giving me incorrect code. I went through too many steps to fix and teach ChatGPT on what to provide. Sometimes it's better to give ChatGPT smaller requests, in smaller steps and then build up from there.

We connect to the TCP endpoint again to get the connection information we need to reach the contract:

![image](https://user-images.githubusercontent.com/80063008/227481795-6d80b231-3e60-4de5-a5f7-33e5f0ae9d4f.png)

Ultimately we get the solver script below:

```python
from web3 import Web3
import json

# connect to the blockchain
w3 = Web3(Web3.HTTPProvider('http://68.183.37.122:31168'))

# set the private key and the account address
private_key = '0x6840d3f07bd2b72d35be78376e334ae56cfad8ba0d47dc604b5b45f890714d1a'
account_address = '0x9A5F9b600CC88a04a2315Df8EEc837F0a43891E5'

# set up the contract instances
target_address = '0x080322a844525a6070C21C92b2271c1215461FC4'
target_abi = [
    {
        "inputs": [],
        "name": "firstShot",
        "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "secondShot",
        "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "thirdShot",
        "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "firstTarget",
        "outputs": [],
        "stateMutability": "view",
        "type": "modifier"
    },
    {
        "inputs": [],
        "name": "secondTarget",
        "outputs": [],
        "stateMutability": "view",
        "type": "modifier"
    },
    {
        "inputs": [],
        "name": "thirdTarget",
        "outputs": [],
        "stateMutability": "view",
        "type": "modifier"
    },
    {
        "inputs": [],
        "name": "receive",
        "outputs": [],
        "stateMutability": "payable",
        "type": "function",
        "payable": True,
        "modifiers": [{"name": "secondTarget", "type": "modifier"}]
    },
    {
        "inputs": [],
        "name": "fallback",
        "outputs": [],
        "stateMutability": "payable",
        "type": "function",
        "payable": True,
        "modifiers": [{"name": "firstTarget", "type": "modifier"}]
    },
    {
        "inputs": [],
        "name": "third",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
        "modifiers": [{"name": "thirdTarget", "type": "modifier"}]
    }
]

target = w3.eth.contract(address=target_address, abi=target_abi)

setup_address = '0xDC3c85F904A4150a415C45aba28b6cfb4D9E091D'
setup_abi = [
    {
        "inputs": [],
        "name": "TARGET",
        "outputs": [{"internalType": "contract ShootingArea", "name": "", "type": "address"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "isSolved",
        "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "TARGET",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "constructor"
    }
]

setup = w3.eth.contract(address=setup_address, abi=setup_abi)

nonce = w3.eth.get_transaction_count(account_address)
tx_hash = w3.eth.account.sign_transaction({
    'nonce': nonce,
    'from': account_address,
    'to': target_address,
    'value': 0,
    'gas': 100000,
    'gasPrice': 200000
}, private_key=private_key)
tx_receipt = w3.eth.send_raw_transaction(tx_hash.rawTransaction)

# wait for the transaction to be mined
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_receipt)



nonce = w3.eth.get_transaction_count(account_address)
# call the receive function on the target contract to trigger the secondShot modifier
tx_hash = target.functions.receive().build_transaction({
    'nonce': nonce,
    'from': account_address,
    'value': 1,
    'gas': 100000
})
signed_tx = w3.eth.account.sign_transaction(tx_hash, private_key=private_key)
tx_receipt = w3.eth.send_raw_transaction(signed_tx.rawTransaction)

# wait for the transaction to be mined
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_receipt)

# call the third function on the target contract to trigger the thirdShot modifier
nonce = w3.eth.get_transaction_count(account_address)
tx_hash = target.functions.third().build_transaction({
    'nonce': nonce,
    'from': account_address,
    'gas': 100000
})
signed_tx = w3.eth.account.sign_transaction(tx_hash, private_key=private_key)
tx_receipt = w3.eth.send_raw_transaction(signed_tx.rawTransaction)

# wait for the transaction to be mined
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_receipt)

# check the new state
is_solved = setup.functions.isSolved().call()
first_shot = target.functions.firstShot().call()
second_shot = target.functions.secondShot().call()
third_shot = target.functions.thirdShot().call()

# print the new state
print(f'firstShot: {first_shot}')
print(f'secondShot: {second_shot}')
print(f'thirdShot: {third_shot}')
print(f'isSolved: {is_solved}')
```

After running the script we see that all our conditions have been met:

![image](https://user-images.githubusercontent.com/80063008/227481891-4e3b3628-5dfe-4bda-849f-3acbb4d54b6d.png)

After all the conditions were met we can connect to the TCP endpoint and get the flag:

![image](https://user-images.githubusercontent.com/80063008/227485784-3ec51433-8e09-46d3-bf39-894f982df3e4.png)

HTB{f33l5_n1c3_h1771n6_y0ur_74r6375}
