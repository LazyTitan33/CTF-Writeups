For this challenge, the description is important as it provides some context.

<i>In my company, we are developing a new python game for Halloween. I'm the leader of this project; thus, I want it to be unique. So I researched the most cutting-edge python libraries for game development until I stumbled upon a private game-dev discord server. One member suggested I try a new python library that provides enhanced game development capabilities. I was excited about it until I tried it. Quite simply, all my files are encrypted now. Thankfully I manage to capture the memory and the network traffic of my Linux server during the incident. Can you analyze it and help me recover my files? To get the flag, connect to the docker service and answer the questions.</i>
 
http://138.68.188.84/forensics_poof.zip

We are provided a zip file to download which contains the following files:

![image](https://user-images.githubusercontent.com/80063008/198265955-a9fd8c28-837e-481a-b296-b98af3732650.png)

Connecting to the given IP and Port we see we need to answer some questions.


### 1. Which is the malicious URL that the ransomware was downloaded from? (for example: http://maliciousdomain/example/file.extension)   
Answer: `http://files.pypi-install.com/packages/a5/61/caf3af6d893b5cb8eae9a90a3054f370a92130863450e3299d742c7a65329d94/pygaming-dev-13.37.tar.gz`

The answer to the first question can be found in the wireshark capture. We just need to follow the HTTP stream and can see a GET request. Because the traffic is unencrypted, we know our link is supposed to be http and not https.

![image](https://user-images.githubusercontent.com/80063008/198266518-2d504b29-e4f9-4fac-8703-d3580762b1eb.png)
![image](https://user-images.githubusercontent.com/80063008/198266602-c58a2085-8fc0-4dff-852e-c8f90999310f.png)

### 2. What is the name of the malicious process? (for example: malicious)  
Answer: `configure`

Let's use the Volatility2 profile given to us. We need to copy it under `volatility/volatility/plugins/overlays/linux/` then we can use the `linux_psaux` command to list running processes.

```bash
vol2 -f mem.dmp --profile=LinuxUbuntu_4_15_0-184-generic_profilex64 linux_psaux
```

The last process running is `configure`  
![image](https://user-images.githubusercontent.com/80063008/198266748-09e373a0-0556-4db7-88b3-c82019744bc9.png)

### 3. Provide the md5sum of the ransomware file.  
Answer: `7c2ff873ce6b022663a1f133383194cc` 

We can extract `pygaming-dev-13.37.tar.gz` from the capture file and unarchive it. In Wireshark, we go to File - Export Objects - HTTP.

![image](https://user-images.githubusercontent.com/80063008/198267150-1c788b2b-6d6f-4440-aa70-6ac424f2309b.png)

The archive contains the `configure` binary file which we can md5sum to get the answer.

![image](https://user-images.githubusercontent.com/80063008/198267334-48953418-8765-4522-9f4d-04c9fc7fbf54.png)  
![image](https://user-images.githubusercontent.com/80063008/198267857-bb87c457-948a-4551-ab0c-db1c8e824d50.png)

NOTE: This md5 value may have changed after I did the challenge because  I think they reuploaded it. The process to get it would be the same though.

### 4. Which programming language was used to develop the ransomware? (for example: nim)  
Answer: `python`

Using strings on the configure file we notice a lot of entries starting with PY so that points to python:

![image](https://user-images.githubusercontent.com/80063008/198268107-8155cc07-4e7d-41eb-9bf0-a296dcf96f6f.png)
![image](https://user-images.githubusercontent.com/80063008/198268137-72d308b3-e3bd-4d3c-8ca3-17ad3021d233.png)


### 5. After decompiling the ransomware, what is the name of the function used for encryption? (for example: encryption)  
Answer: `mv18jiVh6TJI9lzY`

This is the question where I spent the majority of my time for this challenge. I had some difficulty extracting the pyc file from the binary properly. I thought about leaving the struggle out from the writeup to make it clearer but I believe it may help and the process might work in future challenges (unless I screwed something up in this process as well).

At first we notice that Python3.6 shows up in strings so I have to install it first.

![image](https://user-images.githubusercontent.com/80063008/198269088-3461a498-4e48-412c-bd3b-dbf762d99c39.png)

```bash
wget https://www.python.org/ftp/python/3.6.9/Python-3.6.9.tgz
tar xzvf Python-3.6.9.tgz
cd Python-3.6.9
./configure
make
sudo make install
```

I can set up python version using update-alternatives and switch between python versions. Number 3 at the end is there because I already had python 3.10 and 2.7 set up this way.

```bash
update-alternatives --install /usr/bin/python python /usr/local/bin/python3.6 3
````

Use the command below to switch to the desired python version

```bash
update-alternatives --config python
```

I tried to take out the pyc file from the binary:

```bash
pyi-archive_viewer configure
```
`X configure`  
`conf.pyc`

![image](https://user-images.githubusercontent.com/80063008/198269498-b294bc97-1e66-4e8b-b3c6-ece952f50209.png)

This gives me what seemed like a valid .pyc file as I could see some function names using strings. But I kept getting an error "Unknown magic number 227" when trying to use uncompyle6 on the pyc file. 

![image](https://user-images.githubusercontent.com/80063008/198269539-1482a9c7-98d1-41a3-96a3-1c4122587a48.png)

It supposedly is happening because of a bad python3 magic header which I'm missing. I can try to get it using the syntax below.

```bash
python -c "import imp;print(imp.get_magic().hex())"
```

Then prepend bytes to pyc file:

```bash
printf "\x33\x0d\x0d\x0a" | cat - configure.pyc  > conf2.pyc
```

As I said earlier, none of this worked. I kept getting different errors. At this point I took a step back and switched tactics trying to find other ways to extract and decompyle pyc file. I found and downloaded the latest .exe release from this tool:

https://github.com/pyinstxtractor/pyinstxtractor-ng

Ran it in Windows just in case:

![image](https://user-images.githubusercontent.com/80063008/198269977-e4873563-3cdf-487a-9eaa-dd86155364b0.png)

It extracted the .pyc file and a lot of different ones as well in a dedicated folder. I then moved the entire folder contents to my linux box and ran `uncompyle6` on it.

```bash
uncompyle6 configure.pyc > decompiled.py
````

![image](https://user-images.githubusercontent.com/80063008/198270108-19c48ca3-8a96-4882-91e0-54245ddff6a8.png)

Now that we can properly read the source code, we see the name of the function that does the encryption.

![image](https://user-images.githubusercontent.com/80063008/198270195-b5ffe22a-406b-480f-a28c-4e7279336038.png)  
![image](https://user-images.githubusercontent.com/80063008/198270241-96e00c70-ad91-43f7-a5da-73489c0112f0.png)

### 6. Decrypt the given file, and provide its md5sum.
Answer: `3bc9f072f5a7ed4620f57e6aa8d7e1a1`

Based on the source code, we can make our own little script to decrypt the provided encrypted file that we saw earlier, the one with the strange extension `candy_dungeon.pdf.boo`.

```python
from Crypto.Cipher import AES
import random, string, time, os

filename = 'candy_dungeon.pdf.boo'

def Pkrr1fe0qmDD9nKx(filename: str, data: bytes) -> None:
    open(filename, 'wb').write(data)
    os.rename(filename, f"{filename}.boo")

data = open(filename, 'rb').read()
key = 'vN0nb7ZshjAWiCzv'
iv = b'ffTC776Wt59Qawe1'
cipher = AES.new(key.encode('utf-8'), AES.MODE_CFB, iv)
ct = cipher.decrypt(data)
Pkrr1fe0qmDD9nKx(filename, ct)
```

We get a PDF file, calculate its md5sum and answer the last question to get the flag.

![image](https://user-images.githubusercontent.com/80063008/198270566-0ca32314-b5a3-4d7a-8d09-92e7f08b5359.png)  

![image](https://user-images.githubusercontent.com/80063008/198270643-d95f0268-a6b8-486f-86f4-a4677a2eb948.png)

![image](https://user-images.githubusercontent.com/80063008/198270613-a70d2eb2-87cc-406d-ba22-d249dc581261.png)

HTB{n3v3r_tru5t_4ny0n3_3sp3c14lly_dur1ng_h4ll0w33n}
