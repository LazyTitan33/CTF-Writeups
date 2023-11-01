# Bad Memory

### Challenge Description
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/d4ae052c-6769-49c4-9c1c-0c4b58d97d03)

### Solution
After downloading the provided file, we get an image.bin. As indicated by the challenge description, we're looking for a password in a memory dump. I started with `Volatility 2` first as that's usually my go to as it has more options. I immediatelly wanted to dump the hashes on the machine and crack the NTLM hash of the user. I have `vol2` aliased to my vol.py in order to run it within a python2 virtualenv. After it identifies the image profile I list the hives. 

```bash
vol2 -f image.bin --profile=Win10x64_19041 hivelist
```
I've identified the SAM and SYSTEM hives:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/f0e1f5b4-8ff7-427b-8361-f79acf2f5f63)

Now I can do a directed hashdump using their addresses:  

```bash
vol2 -f image.bin --profile=Win10x64_19041 hashdump -y 0xffff860c29e69000 -s 0xffff860c2d591000
```
I get the NTLM hashes:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/93b54a88-349f-438c-a6f5-e61455b49671)

But sadly they do no crack. I could've dumped the hashes without specifying the addresses as well but I got the same hashes. After looking around for a while, using strings and grep in all sorts of ways, I decided to give `Volatility 3` a try. I use it more rarely as it has fewer options. I tried a lot of different things but then I decided to try and dump the hashes with this tool as well thinking that there might be other users that I didn't see/get yet.

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/445aa031-85b5-42a1-9691-2f477fe59a53)

Imagine my surprise when I see the same users but if you take a closer look, the NTLM hash for the congo user looks different. Turns out Volatility 3 works a bit differently when dumping hashes and it allowed me to crack this NTLM using the [crackstation](https://crackstation.net).  

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/2bfd8be3-1028-4987-88c6-71d7df39256e)

Now that we have the password, we have to follow the instructions in the challenge description and md5sum it and put it inside the flag format. This bash command does it all for me quickly. Note that I'm using the `-n` flag with echo in order to not include the trailing newline otherwise I would get the wrong md5sum:  

```bash
echo "flag{$(echo -n 'goldfish#'|md5sum|cut -d ' ' -f1)}"
```
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/43d1cf69-2688-45b2-b0a9-806129440095)

flag{2eb53da441962150ae7d3840444dfdde}


