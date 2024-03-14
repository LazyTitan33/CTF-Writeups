# Primary Knowledge

## Solution 
For this challenge, we get an output.txt and source.py file.

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/196697f0-7717-4d2f-9d9d-dbc261bb2504)

The output.txt contains the following:  

```
Key : 850c1413787c389e0b34437a6828a1b2
Ciphertext : b36c62d96d9daaa90634242e1e6c76556d020de35f7a3b248ed71351cc3f3da97d4d8fd0ebc5c06a655eb57f2b250dcb2b39c8b2000297f635ce4a44110ec66596c50624d6ab582b2fd92228a21ad9eece4729e589aba644393f57736a0b870308ff00d778214f238056b8cf5721a843
```

The source.py contains the following considerably longer code:  

```python3
import os
from secret import FLAG
from Crypto.Util.Padding import pad
from Crypto.Util.number import bytes_to_long as b2l, long_to_bytes as l2b
from enum import Enum

class Mode(Enum):
    ECB = 0x01
    CBC = 0x02

class Cipher:
    def __init__(self, key, iv=None):
        self.BLOCK_SIZE = 64
        self.KEY = [b2l(key[i:i+self.BLOCK_SIZE//16]) for i in range(0, len(key), self.BLOCK_SIZE//16)]
        self.DELTA = 0x9e3779b9
        self.IV = iv
        if self.IV:
            self.mode = Mode.CBC
        else:
            self.mode = Mode.ECB
    
    def _xor(self, a, b):
        return b''.join(bytes([_a ^ _b]) for _a, _b in zip(a, b))

    def encrypt(self, msg):
        msg = pad(msg, self.BLOCK_SIZE//8)
        blocks = [msg[i:i+self.BLOCK_SIZE//8] for i in range(0, len(msg), self.BLOCK_SIZE//8)]
        
        ct = b''
        if self.mode == Mode.ECB:
            for pt in blocks:
                ct += self.encrypt_block(pt)
        elif self.mode == Mode.CBC:
            X = self.IV
            for pt in blocks:
                enc_block = self.encrypt_block(self._xor(X, pt))
                ct += enc_block
                X = enc_block
        return ct

    def encrypt_block(self, msg):
        m0 = b2l(msg[:4])
        m1 = b2l(msg[4:])
        K = self.KEY
        msk = (1 << (self.BLOCK_SIZE//2)) - 1

        s = 0
        for i in range(32):
            s += self.DELTA
            m0 += ((m1 << 4) + K[0]) ^ (m1 + s) ^ ((m1 >> 5) + K[1])
            m0 &= msk
            m1 += ((m0 << 4) + K[2]) ^ (m0 + s) ^ ((m0 >> 5) + K[3])
            m1 &= msk
        
        m = ((m0 << (self.BLOCK_SIZE//2)) + m1) & ((1 << self.BLOCK_SIZE) - 1) # m = m0 || m1

        return l2b(m)

if __name__ == '__main__':
    KEY = os.urandom(16)
    cipher = Cipher(KEY)
    ct = cipher.encrypt(FLAG)
    with open('output.txt', 'w') as f:
        f.write(f'Key : {KEY.hex()}\nCiphertext : {ct.hex()}')
```
As you can probably tell from the "abundance" of details and effort I put into these crypto writeups, I'm not much of a fan. I know just enough to do the very easy ones and to detect imaginations from ChatGPT. That helps me get some points in the CTF and also helps me lead ChatGPT into building a good enough script to get the flag.

```python3
from Crypto.Util.Padding import pad, unpad
from Crypto.Util.number import bytes_to_long as b2l, long_to_bytes as l2b
from enum import Enum

class Mode(Enum):
    ECB = 0x01
    CBC = 0x02

class Cipher:
    def __init__(self, key, iv=None):
        self.BLOCK_SIZE = 64
        self.KEY = [b2l(key[i:i+self.BLOCK_SIZE//16]) for i in range(0, len(key), self.BLOCK_SIZE//16)]
        self.DELTA = 0x9e3779b9
        self.IV = iv
        if self.IV:
            self.mode = Mode.CBC
        else:
            self.mode = Mode.ECB

    def _xor(self, a, b):
        return b''.join(bytes([_a ^ _b]) for _a, _b in zip(a, b))

    def decrypt(self, ct):
        blocks = [ct[i:i+self.BLOCK_SIZE//8] for i in range(0, len(ct), self.BLOCK_SIZE//8)]
        pt = b''
        X = self.IV or bytes([0] * (self.BLOCK_SIZE//8))  # Initialize X with IV or zeros
        
        for ct_block in blocks:
            pt += self.decrypt_block(ct_block, X)
            X = ct_block  # Set previous ciphertext block for next iteration
        
        return pt

    def decrypt_block(self, ct_block, prev_ct_block):
        c = b2l(ct_block)
        msk = (1 << (self.BLOCK_SIZE//2)) - 1

        m1 = c & msk
        m0 = c >> (self.BLOCK_SIZE//2)

        K = self.KEY
        s = self.DELTA << 5
        for i in range(32):
            m1 -= ((m0 << 4) + K[2]) ^ (m0 + s) ^ ((m0 >> 5) + K[3])
            m1 &= msk
            m0 -= ((m1 << 4) + K[0]) ^ (m1 + s) ^ ((m1 >> 5) + K[1])
            m0 &= msk
            s -= self.DELTA

        # XOR with previous ciphertext block
        m0 ^= b2l(prev_ct_block[:4])
        m1 ^= b2l(prev_ct_block[4:])

        # Feedback
        m0 ^= b2l(prev_ct_block[:4])
        m1 ^= b2l(prev_ct_block[4:])

        return l2b((m0 << (self.BLOCK_SIZE//2)) + m1)


if __name__ == '__main__':
    # Ciphertext obtained from the output.txt file
    ct_hex = "b36c62d96d9daaa90634242e1e6c76556d020de35f7a3b248ed71351cc3f3da97d4d8fd0ebc5c06a655eb57f2b250dcb2b39c8b2000297f635ce4a44110ec66596c50624d6ab582b2fd92228a21ad9eece4729e589aba644393f57736a0b870308ff00d778214f238056b8cf5721a843"
    ct = bytes.fromhex(ct_hex)

    # Key obtained from the output.txt file
    KEY_hex = "850c1413787c389e0b34437a6828a1b2"
    KEY = bytes.fromhex(KEY_hex)

    # Decrypt the ciphertext
    cipher = Cipher(KEY)
    pt = cipher.decrypt(ct)

    print(pt.decode())
```
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/96f245e3-7cfd-4268-99f4-ad1f4020a401)

`HTB{th1s_1s_th3_t1ny_3ncryp710n_4lg0r1thm_____y0u_m1ght_h4v3_4lr34dy_s7umbl3d_up0n_1t_1f_y0u_d0_r3v3rs1ng}`

