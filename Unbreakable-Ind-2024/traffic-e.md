# traffic-e

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/3743e8d2-b937-4c47-946b-89ae97c1bf8c)

# Solution

The wireshark capture has very few packets. In fact, the screenshot below contains all of them:  

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/25209d6f-892d-4d27-8235-65268a134855)

A grand total of 26 packets:  

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/9daa70ed-38e5-4eba-8c23-871095c4bf89)

This tells me that we have to decrypt this TLS traffic somehow. The only idea is to see if there's a weak RSA key. We can extract the Public Key from the Certificate. We can find that in packet 6. We have the modulus and the exponent:  

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/6e184853-4f46-4fdc-84e2-d3ef8e7c08a6)

Using the [RsaCtfTool](https://github.com/RsaCtfTool/RsaCtfTool) we can pass the modulus and the exponent as arguments and try to recover the private key using `--private`.

```python3
python3 RsaCtfTool.py -n 0x073c0dc93dffa026b888e0eb2fda7ac6e182a7bc5fa43900d361a442eb7cdb44027b319676b5fd37491bce308d76e5be3ea961d87fff5d2552b434ed8ee662a10539ea21f437170df970ef2b6a9be1410916530b8397b4357bf178852a35c90b3320b493213e05fb000966d89eba0925c34422e480a5c9176737cc98ab09993287 -e 0x0097de379a979d080459a7ab09b848eaebbe8379ef79d25c0be74d2435a40c7e11db517b50590cfcbe159dd375221e0f45d1a0d4d9a9403ffe34fb1e402a854b41716c8eaafc0e66e6f709e654eae6838d69b61eb000c0a46d135ce63236c276d5fe262848629798e6e55af557b10d4e8467012235bab0fe5dcf81d9fb832fcbef --private
```
I was quite puzzled by this one because initially I got an error saying the crack failed. Which normally means that the RSA keypair is strong. Turns out I neglected to install the requirements for RsaCtfTool. Normally it is functional without installing them, you can use the tool simply by cloning it from the repo. It turns out that installing the requirements unlocks more attack methods.

So, don't be like me, after you clone RsaCtfTool, don't forget to `pip install -r requirements.txt` then run it. It will show that I was right and the keypair is weak and the `wiener` (great name) method works and we recover the private key:  

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/0bf36203-2de1-4176-bb57-0af3729f518c)

```text
-----BEGIN RSA PRIVATE KEY-----
MIICOgIBAAKBgQc8Dck9/6AmuIjg6y/aesbhgqe8X6Q5ANNhpELrfNtEAnsxlna1
/TdJG84wjXblvj6pYdh//10lUrQ07Y7mYqEFOeoh9DcXDflw7ytqm+FBCRZTC4OX
tDV78XiFKjXJCzMgtJMhPgX7AAlm2J66CSXDRCLkgKXJF2c3zJirCZkyhwKBgQCX
3jeal50IBFmnqwm4SOrrvoN573nSXAvnTSQ1pAx+EdtRe1BZDPy+FZ3TdSIeD0XR
oNTZqUA//jT7HkAqhUtBcWyOqvwOZub3CeZU6uaDjWm2HrAAwKRtE1zmMjbCdtX+
JihIYpeY5uVa9VexDU6EZwEiNbqw/l3Pgdn7gy/L7wIgKIqzRSfsrSJ70+yehHyo
lC84i2XTp1k5fF+qnuf/4AcCQQHpLb+j9n8VJeH6Qn5XFDSp3GTgXehzzOZxgg6D
ky59MWM70WzqewpINccNVf82rMxnSaDHdEyNMo3TDxryQ8ezAkEDyTpp96IT+hqN
qZA9ksJ4VTtnUlvt7YQvzve/xIhGeagI+U/uXxVb/QwhGw0Z7sOEIJGAZctAhu1C
bFQ9JOx/3QIgKIqzRSfsrSJ70+yehHyolC84i2XTp1k5fF+qnuf/4AcCICiKs0Un
7K0ie9PsnoR8qJQvOItl06dZOXxfqp7n/+AHAkEBSnhocZ+Abosm1BunWucnbXHk
IKMrcBmQADljzeTQA8ULJmdxmn1nTnXxVwNy8LJgNE+j0qGbZtpwldJe5SHXjQ==
-----END RSA PRIVATE KEY-----
```
We can save this to a file and go in Wireshark to `Edit` -> `Preferences` -> `Protocols` -> `TLS` -> `Edit` on RSA keys list, add the IP, port and the keyfile. For this particular capture, we don't need to specify a protocol since there's only TLS traffic:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/6b52d939-dc86-4488-9dbe-229093c21995)

Now, the encrypted alerts are decrypted:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/df7e4069-5cae-4373-9ca6-c5b38fbab989)

We can now also follow the TLS stream and get the flag:  

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/312aed23-95b4-40f2-bd48-5e90e3b7fc55)

`CTF{46b1d043b3d2d98a267455affce276c47a1f2bfb940881d1e9725c798373f532}`
