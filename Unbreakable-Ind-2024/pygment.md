# pygment

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/c448d22f-aa87-43b8-b03b-234ccc0b70aa)

# Solution
As soon as we try to reach the given target, we are met with an error message which seem to indicate that we are not giving some required parameters, but also that the `pygmentize` binary doesn't actually exist on the box:  

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/21b8136b-885a-4ffc-9b28-c1ee414ef697)

Fuzzing the target we find a `flag.php` as well but there's nothing interesting here yet:  

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/70a9cc82-c348-41ce-8052-ee23555ddaeb)

I spent quite some time on the error message above because I thought the box was broken. Given the challenge name, I actually expected to get a functional website but it seems that that was too much to ask and it turns out that it's just a simple command injection. Not even a blind one because we can clearly see the error message. If the `pygmentize` binary was on the box, we would've at least gotten a more interesting challenge.  

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/d4b9070b-1949-4ba2-8df2-576fc2bdcbcb)

We can read the flag.php file and pipe our command to `base64` with `-w0` argument to make sure we get it all on one line:  

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/a4497a85-35b6-4681-8ba5-19fbfc42271d)

It can even be done with a bash oneliner:

```bash
curl -s 'http://34.107.126.69:30516/?a=lazy&b=titan;`cat%20flag.php|base64+-w0`'|grep -Eo '\b[A-Za-z0-9+/]{20,}{0,2}\b'|base64 -d 2>/dev/null|grep -io CTF{.*} --color=none|sed 's/ctf/CTF/g'
```
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/1c9d65d5-9000-4c97-8239-d0c7767c8982)

`CTF{2ae4644b1e4cbc1f560c52f3ee0985043d3e0acf0f766851382974646578ec39}`

Note: I had to replace the lowercase ctf with upper case because the flag wasn't originally accepted. All in all this challenge felt lackluster with the most minimum of efforts from the creator. It boggles the mind why this was considered "medium". [sided-curl]() was much more difficult and interesting and with some thought actually put behind it.
