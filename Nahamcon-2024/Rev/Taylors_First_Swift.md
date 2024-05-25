## Taylors_First_Swift

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/947512d8-cdcf-4831-b997-2aa5031fca91)

## Solution

The provided file is not one that I can run however, being an easy one, I don't expect that we need to.

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/67742cd8-e7a2-4ec6-a455-e3cd25d28e13)

I opened it in Ghidra and noticed some hex strings in the "flagchecky" function:  

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/eafc31b8-749e-4ce9-ac6c-fc358f1f1283)

I copied them into a temporary file called test:  

```text
  *puVar7 = 0x73;
  puVar7[1] = 0x77;
  puVar7[2] = 0x69;
  puVar7[3] = 0x66;
  puVar7[4] = 0x74;
  puVar7[5] = 0x69;
  puVar7[6] = 0x65;
  puVar7[7] = 0x73;
  puVar7[8] = 0x21;
```
And then converted them to ASCII with this one liner:  

```bash
cat test|awk '{print $3}'|tr -d ';' |xxd -r -p
```
It turns out it is the word `swifties!`:  

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/d25e6c7d-7981-449c-823e-5f9de8199c44)

Below that there is a longer one which gets converted similarly to a base64 encoded string:  

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/62fa6586-f35e-430b-a635-3ab9ea6ed967)

I noticed a mention of some `XOR` in some other functions:  

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/24f0bcaf-f804-4b4a-9a2b-eaaacc7ac812)

So I made an educated guess that the longer string is XORed with the smaller one and tried it in [CyberChef](https://gchq.github.io/CyberChef/#recipe=From_Base64('A-Za-z0-9%2B/%3D',true,false)XOR(%7B'option':'UTF8','string':'swifties!'%7D,'Standard',false)&input=RlJzSUFROFBWQlVWRVJFSVZFUmJCa1VSRmtVSUJ4VlFWa0FZRnhKZlYwRllWa0lWUWdvPQ&ieol=CRLF):  

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/59a4e220-b2a0-4516-b6b3-8e6884bbc534)

And we got the flag:  

`flag{f1f4bfa202c60e2aaa9339de61513141}`
