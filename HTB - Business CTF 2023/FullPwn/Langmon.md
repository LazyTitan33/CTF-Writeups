### Challenge description
FullPwn challenges don't have a description. We just get an IP address and are supposed to get user and root flag.

A port scan shows only ports 22 and 80 open, we also see it resolved to `langmon.htb` so we add that to your hosts file.
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/c271e8fd-4ddb-4b23-aacb-61459c2d7b6c)

The mainpage reveals a good looking website:
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/2c8382eb-9bb1-4255-9d48-5e78bce231cc)

Thankfully we are able to register a user on this website:
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/1e9cf5af-f131-47a9-8666-ac87e616fe1a)

From the nmap scan which shows `wp-admin` we know this is a Wordpress website so we use wpscan to scan it for users and vulnerable templates. We use the aggressive method and pass in our API token for more details:
```bash
wpscan --url http://langmon.htb/ -e vp,u --plugins-detection aggressive --api-token <redacted>
```

After a short while, the scanner finds that `php-everywhere` is a vulnerable plugin presently used on the website:
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/4aac0b90-8342-48ca-88d0-6665be556c33)

After a bit of research, we find this youtube video clearly showing the way to trigger code execution.

[![IMAGE ALT TEXT](http://img.youtube.com/vi/NJl64f9Ohp8/0.jpg)](http://www.youtube.com/watch?v=NJl64f9Ohp8 "PHP Everywhere RCE")

We just follow that video creating a post with a php block in it and get a reverse shell:
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/1da1fe84-b4a4-4151-9a02-d86263280d24)

The first thing that needs to be done for a wordpress website is to read the `wp-config.php` file to read database credentials:
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/d9639225-ef98-41c9-941d-7fa8dd6e1d17)

We find the password `SNJQvwWHCK` which turns out is being reused by the user `developer`:
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/cdd8ca2b-f527-4129-9d48-5af0255059ca)

And we get the user flag:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/22db4596-fe50-439b-bece-e49452036257)  

HTB{4lw4y5_upd473_y0ur_plu61n5}

## Privilege Escalation

Checking the sudo permissions we can see that user developer is allowed to run a specific python script:
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/609e9be2-e71e-4ae6-8b44-6df5b357ab2a)

```python
#!/usr/bin/python3
import sys
from langchain.prompts import load_prompt

def load(file):
        try:
                load_prompt(file)
        except:
                print("There is something wrong with the prompt file.")
if __name__ = "__main__":
        if len(sys.argv) != 2:
                print("Usage: prompt_loader.py <prompt_file_path>")
        else:
                file = sys.argv[1]
                load(file)
```

I wasn't familiar with the langchain library however quick google search for langchain exploits we find that it is vulnerable to code injection:
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/f7d9c104-8e58-4764-a879-dc6074caa201)

We can copy the script from this github issue: https://github.com/hwchase17/langchain/issues/4849. Saved it to a file called getroot.py and we execute it to read the flag:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/22fe8c21-a5e6-45a5-904b-89182ad7a631)

HTB{7h3_m4ch1n35_5p34k_w3_h34r}




