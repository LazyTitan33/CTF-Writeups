### Challenge Description

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/c7c36016-1156-45f6-8d63-5c874ebdc24e)

## Enumeration

Pretty good looking Fallout themed website:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/21201937-ebb7-43c9-a7fb-b700e91e316c)

We seem to have an interesting endpoint allowing us to update a Firmware.

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/361bf60f-72a0-4e16-9f76-81327f00dd7f)

## Solution

When making the POST request we can clearly see it is sending XML data so that screams [XXE](https://book.hacktricks.xyz/pentesting-web/xxe-xee-xml-external-entity) from a mile away:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/eb8b859c-0c02-42ec-bac3-16fe7d700cdf)

`HTB{b1om3tric_l0cks_4nd_fl1cker1ng_l1ghts_427cf9303c8fd89feaf3582d1f41a8b9}`
