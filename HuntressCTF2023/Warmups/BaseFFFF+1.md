# BaseFFFF+1

### Challenge Description
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/34d9db40-87f8-412a-add8-8f0c7d7cf533)

### Solution
Reading the file, we get some symbols that are very unfamiliar:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/d472eebc-5ca6-44af-8652-3448a78eff1e)

This is the content:
```bash
鹎驣𔔠𓁯噫谠啥鹭鵧啴陨驶𒄠陬驹啤鹷鵴𓈠𒁯ꔠ𐙡啹院驳啳驨驲挮售𖠰筆筆鸠啳樶栵愵欠樵樳昫鸠啳樶栵嘶谠ꍥ啬𐙡𔕹𖥡唬驨驲鸠啳𒁹𓁵鬠陬潧㸍㸍ꍦ鱡汻欱靡驣洸鬰渰汢饣汣根騸饤杦样椶𠌸
```
A quick google helps us determine that `ffff` in decimal is actually just 65535:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/c3b0ff12-c493-40d7-b1d5-b0ffa55749ef)

Since 65535 + 1 = 65536, let's search and see if `base65536` is actually a thing:  

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/7911c009-3c6b-4a29-be03-ce480d801095)

We seem to be on the right track as we have results indicating that this does in fact exist. We can use this online decoder and get our flag: 
https://www.better-converter.com/Encoders-Decoders/Base65536-Decode

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/01d00640-fa35-42db-accd-58c7a50b794c)

flag{716abce880f09b7cdc7938eddf273648}
