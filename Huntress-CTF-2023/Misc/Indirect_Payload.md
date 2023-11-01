# Indirect Payload

### Challenge Description
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/784bf2ce-599f-43f3-9a73-bc9c869577ea)

### Solution

Accessing the generated link, we have a webpage where we can retrieve a payload:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/f8009b4c-9430-40e3-8488-6d4262053293)

We have Burpsuite intercepting in the background and we can see a lot of 302 Redirects as soon as we pressed the button:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/a04ee012-b411-4bf9-a753-b7333e929862)

Looking through each one, we can see that some have a body. One of them says that character 0 of the payload is `f`:  

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/381a558a-123d-449d-85ce-ce7299e32712)

Then we have an `l`:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/1cc7237b-6ba5-45ac-b6ee-1ed7894bd00c)

And an `a`:  

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/c581abfd-da2d-41b2-b692-a27754372de4)

And a `g`:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/909d969f-f0f9-478f-97d3-e0771481403f)

These are not consecutive. There are some empty redirects in between so we can't simply click through and transcribe the flag. Or we could, but we can think of an easier way. Let's use `wget` to follow a lot of requests and get a detailed body into an output.txt file:

```bash
wget --debug --max-redirect=150 http://chal.ctf.games:31453/site/flag.php -o output.txt
```
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/4f7543fb-fd3f-4d7c-b5c4-0b93a341e217)

After a while, we can read the content of the output.txt file and parse it out to print the flag:  

```bash
cat output.txt|grep payload|awk '{print $12}' ORS=
```
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/e3b81097-3a64-44b6-8364-7131cf812052)

flag{448c05ab3e3a7d68e3509eb85e87206f} 
