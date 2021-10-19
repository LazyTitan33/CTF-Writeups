We are given a key and an encrypted string. The name of the challenge hints at a substitution cipher so I used the Python maketrans() function in a loop until I got the flag.

key = {'1': 'j', '0': 'X', '3': 'F', '2': 'o', '5': 'T', '4': 'x', '7': '0', '6': 'P', '9': '}', '8': 'J', ':': 'b', 'A': 'c', 'C': 'p', 'B': 'q', 'E': '7', 'D': 'a', 'G': 'v', 'F': '3', 'I': '5', 'H': '1', 'K': 'O', 'J': 'K', 'M': 'g', 'L': '2', 'O': 'n', 'N': '8', 'Q': 'y', 'P': 'E', 'S': 'e', 'R': 'R', 'U': 'h', 'T': 'W', 'W': 'N', 'V': 'm', 'Y': '9', 'X': 'G', 'Z': 'S', 'a': 'k', 'c': 't', 'b': 'd', 'e': '{', 'd': '4', 'g': 'C', 'f': 'L', 'i': '6', 'h': 'l', 'k': 'Z', 'j': 'z', 'm': 'U', 'l': 's', 'o': 'B', 'n': 'M', 'q': 'I', 'p': 'i', 's': ':', 'r': 'Q', 'u': 'Y', 't': 'r', 'w': 'V', 'v': 'H', 'y': 'D', 'x': 'A', '{': 'f', 'z': 'w', '}': 'u'}

encrypted = 'erBQUpW3fpQDirBFb7c}}FdPT0}x0jdLcokk}xq7jaT3Lpqkju'


```python
key = {'1': 'j', '0': 'X', '3': 'F', '2': 'o', '5': 'T', '4': 'x', '7': '0', '6': 'P', '9': '}', '8': 'J', ':': 'b', 'A': 'c', 'C': 'p', 'B': 'q', 'E': '7', 'D': 'a', 'G': 'v', 'F': '3', 'I': '5', 'H': '1', 'K': 'O', 'J': 'K', 'M': 'g', 'L': '2', 'O': 'n', 'N': '8', 'Q': 'y', 'P': 'E', 'S': 'e', 'R': 'R', 'U': 'h', 'T': 'W', 'W': 'N', 'V': 'm', 'Y': '9', 'X': 'G', 'Z': 'S', 'a': 'k', 'c': 't', 'b': 'd', 'e': '{', 'd': '4', 'g': 'C', 'f': 'L', 'i': '6', 'h': 'l', 'k': 'Z', 'j': 'z', 'm': 'U', 'l': 's', 'o': 'B', 'n': 'M', 'q': 'I', 'p': 'i', 's': ':', 'r': 'Q', 'u': 'Y', 't': 'r', 'w': 'V', 'v': 'H', 'y': 'D', 'x': 'A', '{': 'f', 'z': 'w', '}': 'u'}
encrypted = 'erBQUpW3fpQDirBFb7c}}FdPT0}x0jdLcokk}xq7jaT3Lpqkju'

while True:
encrypted = encrypted.translate(str.maketrans(key))
if 'StormCTF' in encrypted and encrypted[-1] == "}":
print(encrypted)
break
```

StormCTF{Crypto3:EA993b6579471bfA2aa94BE1D5FfCBa1}
