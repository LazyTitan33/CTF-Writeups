# Dynastic

## Solution 
For this challenge, we get an output.txt and source.py file.

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/196697f0-7717-4d2f-9d9d-dbc261bb2504)

The output.txt contains:

```
Make sure you wrap the decrypted text with the HTB flag format :-]
DJF_CTA_SWYH_NPDKK_MBZ_QPHTIGPMZY_KRZSQE?!_ZL_CN_PGLIMCU_YU_KJODME_RYGZXL
```

And the source.py contains the python code:  

```python3
from secret import FLAG
from random import randint

def to_identity_map(a):
    return ord(a) - 0x41

def from_identity_map(a):
    return chr(a % 26 + 0x41)

def encrypt(m):
    c = ''
    for i in range(len(m)):
        ch = m[i]
        if not ch.isalpha():
            ech = ch
        else:
            chi = to_identity_map(ch)
            ech = from_identity_map(chi + i)
        c += ech
    return c

with open('output.txt', 'w') as f:
    f.write('Make sure you wrap the decrypted text with the HTB flag format :-]\n')
    f.write(encrypt(FLAG))
```

I don't know much about crypto but ChatGPT told me to modify the `chi + i` and make it a `chi - i`:  

```python3
from random import randint

def to_identity_map(a):
    return ord(a) - 0x41

def from_identity_map(a):
    return chr(a % 26 + 0x41)

def encrypt(m):
    c = ''
    for i in range(len(m)):
        ch = m[i]
        if not ch.isalpha():
            ech = ch
        else:
            chi = to_identity_map(ch)
            ech = from_identity_map(chi - i)
        c += ech
    return c
decrypted_text = encrypt('DJF_CTA_SWYH_NPDKK_MBZ_QPHTIGPMZY_KRZSQE?!_ZL_CN_PGLIMCU_YU_KJODME_RYGZXL')
print('HTB{' + decrypted_text + '}')
```
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/d89ff72e-9d8d-4f5b-8235-65c43c459edb)

`HTB{DID_YOU_KNOW_ABOUT_THE_TRITHEMIUS_CIPHER?!_IT_IS_SIMILAR_TO_CAESAR_CIPHER}`
