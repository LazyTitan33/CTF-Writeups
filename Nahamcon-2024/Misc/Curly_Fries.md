## Curly Fries

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/8ff70bb4-4694-4e0b-81ee-c81f343c43ff)

## Enumeration

After we SSH into the box, we find that the user is allowed to run a very specific curl command as user `fry`:  

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/f4ea1179-5a66-41b9-b3e1-1f9040ca019b)

However, while enumerating we also find that he is allowed to enter the `fry` user home directory and read the `.bash_history` in which we find a password:  

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/cee0cdd9-8ebc-402e-8f4e-2ea5fd344ba4)

```text
iLoveCurlyFriesYumYumInMyTumTum
```

We can use this to switch to `fry` and can see that he also is allowed to run curl but as root and with a wildcard at the end. This is the important part:  

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/dd5c3685-f0bd-4b48-822a-0bd68cbc85c3)

## Solution

Abusing the wildcard we can read files as root:  

```bash
sudo curl 127.0.0.1:8000/health-check file:///etc/shadow
```
We don't even need a valid localhost on port 8000 to curl to. While trying to crack the root hash in the background. We can save this shadow file to a file called `health-check`. However, we've modified it so that the root hash is known to us. I simply copied fry's hash over to root so we can reuse his password.

In a different shell, we use python to host the file on port 8000 and then use the curl command below to grab it and overwrite the /etc/shadow file:  

```bash
sudo curl 127.0.0.1:8000/health-check -o /etc/shadow
```

Now we can switch to root and get the flag:  

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/b9417a8b-53ef-4e63-be07-b17b7f48bf3e)

`flag{36fa4a94c4c3806b19c496a31859eff0}`
