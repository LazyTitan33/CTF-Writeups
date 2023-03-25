The first challenge in the Crypto section provides two files. The `output.txt` file contains the encoded data below:

```
0x53465243657a467558336b7764584a66616a4231636d347a655639354d48566664326b786246397a5a544e66644767784e56396c626d4d775a4446755a334e665a58597a636e6c33614756794d33303d
```

We are also provided with the `source.py` file below:

```python
from Crypto.Util.number import bytes_to_long
from base64 import b64encode

FLAG = b"HTB{??????????}"


def encode(message):
    return hex(bytes_to_long(b64encode(message)))


def main():
    encoded_flag = encode(FLAG)
    with open("output.txt", "w") as f:
        f.write(encoded_flag)


if __name__ == "__main__":
    main()
```

As we can see from the source code, the flag is base64 encoded and then hex encoded. No encryption here.. pfew.

This means we can simply unhex and then base64 decode the flag with a oneliner:

```bash
xxd -r -p output.txt|base64 -d
```

And we get our flag:  
![image](https://user-images.githubusercontent.com/80063008/227489718-208649c4-f7a1-47cf-a945-88b4990cd42f.png)

HTB{1n_y0ur_j0urn3y_y0u_wi1l_se3_th15_enc0d1ngs_ev3rywher3}