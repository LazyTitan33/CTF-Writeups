### Challenge Description

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/2f8cb80a-a44a-4979-bd76-fcaf342a008a)

## Enumeration

For this challenge, we get a bunch of Windows EventViewer logs in their standard form of `evtx` files. 

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/18588261-df28-48e2-82ce-4ca6576f4c14)

I like converting them to a human readable format as they are easier to strings and grep through.

```bash
sudo apt install python3-evtx
mkdir converted
for file in ./*.evtx;do evtx_dump.py "$file" > converted/"${file%.evtx}.xml";done
```
I started by looking for powershell scripts being run:  

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/e97df80c-6021-41a6-8b20-5386159130fe)

## Solution

I opened the Windows Powershell Operational file and looked at the content of the `h.ps1` file and my eyes landed on the `SFRC` which is the Base64 encoded HTB string. I've done a lot of challenges on HTB so I recognize it immediately:  

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/4dcefb42-0d23-4809-b94c-faf248732e69)

We decode it and get the flag:  

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/df155627-68a7-4617-8700-6d8598f93e4c)

`HTB{1ntruS10n_d3t3ct3d_!!!}`

