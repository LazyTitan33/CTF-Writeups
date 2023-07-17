### Challenge description

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/5f25ec84-fc05-4775-a96e-29f27f1d586f)

We get bash script from this challenge:

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/773aebe1-07c1-40fb-8616-2d394803a191)

I didn't look to deep into it, so I don't know what it actually does. My eyes fell directly and some base64 strings in several different parts of the code.

Part 1 on line 761:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/f8f56c8a-8189-4fe8-97f0-a50aecda4557)

```bash
echo cGFydDE9IkhUQnttMW4xbmciCg==|base64 -d
```
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/c7e40797-6e4d-45b4-b65e-197ede85fa78)

Part 2 on line 636:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/89cb1857-b054-4e7f-8037-e1f01bd97c1a)

```bash
echo cGFydDI9Il90aDMxcl93NHkiCg==|base64 -d
```
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/5a674d08-75c2-43f3-8f4b-644e4873c0e7)

Part 3 on line 701:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/31449608-b23d-4a24-b52f-2cd9eab44864)

```bash
echo X3QwX200cnN9Cg==|base64 -d
```
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/49cb28c5-b839-45d8-8302-baf814cc55bf)

HTB{m1n1ng_th31r_w4y_t0_m4rs}
