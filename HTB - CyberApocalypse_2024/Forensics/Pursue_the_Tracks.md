# Pursue the Tracks

## Enumeration
This one starts with an MFT file:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/fe7ca245-b478-4acb-8753-63beca0db35f)

We can use [MFT Explorer](https://f001.backblazeb2.com/file/EricZimmermanTools/MFTExplorer.zip) to read these and can see some interesting folders already:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/51f62872-bc45-49c9-b963-3c85e2f41ada)

## Solution
Let's start the challenge by connecting to the provided IP and Port. Question one can be answered directly as it is clear what we can see:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/9ed9615a-231f-4801-9ace-9786c0b3ddec)

Second question:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/816f9680-255c-434a-807a-80b4aa652fd2)

We can find this answer by enumerating and looking carefully at the creation dates:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/12012ba6-e45c-4cb5-931c-d78ca52e97a4)

Third question:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/7534585a-64cf-4cfa-b934-a945fee0e63e)

Deleted files are flagged as such in MFT Explorer:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/93b3b99b-cc09-435f-820c-585cdd9d36da)

Fourth question:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/4bca7def-4831-4691-b1a8-c1fd8dea68f1)

Not sure how to identify hidden mode for files in MFT Explorer, this was just easier to guess.

Fifth question:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/b1709317-d97d-4da9-bff3-6d77966d38d8)

This file looks important for sure and it's the only .txt file:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/68b4ae45-0c83-45a2-9062-fd8123f5e3c6)

Sixth question:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/50e0e3f3-756f-49d9-addf-d9b6a72922d9)

Copied files are also flagged and as such are easy to find:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/dee85ef3-aac3-416b-bcef-39b88a092a69)

Seventh question:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/d7bc099b-cea1-4ee0-8c42-4153cbefd96f)

This one requires careful enumeration again by looking at the creation date vs modified date:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/fd195521-a32d-4d31-8f3f-d41e5f1aa64f)

Eighth question:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/e454478d-1433-481b-8e08-29a1b5a39af9)

Record numbers for files show up in the top left corner of the Overview in HEX format. 0x2d is 45 in decimal:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/b70d8c9c-e7d7-4e85-9c8f-e8d4f9a7e606)

Ninth question:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/d51e4b1d-0ba2-4d92-9105-522fd208f518)

Record number 40 is 0x28 in HEX. The total file size is mentioned in the `Allocated size` for the file. In this case file with Record Number `0x28` in HEX is the one we are interested in and the size is `0xE000`.   
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/c4fa0e03-e300-429b-acdb-970e30c93ddd)

We can convert that to decimal [online](https://www.rapidtables.com/convert/number/hex-to-decimal.html):  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/09d35e5f-89d5-4ff5-a55a-656f8c07e7e8)

`HTB{p4rs1ng_mft_1s_v3ry_1mp0rt4nt_s0m3t1m3s}`

