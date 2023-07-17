### Challenge description

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/5ef17f55-73c9-44e4-a152-5aa51a1fc7d2)

For this forensics challenge, we get the following files.

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/3acc4b16-989d-4e3c-a5ad-858b0703cb8b)

Running strings on the shortcut file we can see powershell being used:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/d1938cb0-01c6-45a2-b983-c77016102956)

The invoice.vbs file contains what we would expect, obfuscated malicious code.

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/0dbaad70-e371-4111-a4db-778a63a8969a)

The logs.zip contains evtx files. I used [evtx_dump.py](https://github.com/williballenthin/python-evtx/blob/master/scripts/evtx_dump.py) to convert these into readable format for linux so I can easily grep through them.

```bash
for file in ./*.evtx;do evtx_dump.py "$file" > converted/"${file%.evtx}.xml";done
```

Because we already know powershell was used, after converting all the event viewer logs, we can run strings on everything and grep for powershell:

```bash
strings *|grep powershell
```
We quickly find some interesting stuff. We see a powershell command was run with a base64 string:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/476157f7-9a2b-44e7-844b-9e5230f0e6b6)

Decoding that string, we can see a Google Sheets URL:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/0c60cf4d-c63e-413c-a8f7-fbea75b4496c)

However, we can't seem to access this URL so this is as far as we go for now:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/5f1ffab9-ee0d-4f46-b0e3-2005eb88ea5d)

We've collected quite a lot of information so far. Let's spawn the docker and connect to the provided IP and port using netcat. We are informed that in order to get the flag, we have to answer some questions.

Question 1:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/f8196305-a8de-4d3e-a934-e7a4bcd29c60)

When we grep for powershell, we can also see this line which gives us the answer we are looking for:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/6ac36f0c-d04d-4ae2-b9cd-320dabd0364a)
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/a31c2ea2-ce96-455c-8a76-ee71d70f4507)

Question 2:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/5358244d-38f1-4f90-9777-29b783f1c35a)

There are only two functions in the script. Easy answer even by trial/error. While the first one builds the payload, the second one does the deobfuscation.  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/d33dd942-49db-429e-81f6-b55d983b7daa)

Question 3:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/f50ea40b-2463-42f1-ad2a-e6455b4784ff)

From our grepping we already know this... it's powershell.

Question 4:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/bcf3ff85-0541-42d6-aedc-482dcd93f587)

We already found this out through our grepping. Even though we can't access the Google Sheets page, we have the URL which contains the Spreadsheet ID.

Question 5:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/ed1e029a-7335-44b0-a955-5edf33ee6abb)

We have this information in the same Google Sheets URL we uncovered:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/e2370135-f266-4d2f-b8e1-09f8863e4f36)

Question 6:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/efa316f5-eec7-40fa-83a7-1cbc1363912a)

To find this, we need to open the Event Viewer log where we found the powershell command that was executing the base64. We can find what file that is by adding the `-rn` flags to our grep.  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/46ccbea4-30c8-488b-97a9-1445e3162099)

We open this file in our file editor of choice, Sublime, and can see the EventID:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/820a8d84-d866-43ff-9208-e4f03cf95a37)
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/c4857609-24bf-46e7-8f4a-f67452cb6dbd)

Question 7:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/6f6d829c-9ef5-4513-9d8a-c2f9b96e0783)

If we were to continue reading the file we just opened for Question 6, a bit further down we can see the XOR operation:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/7d9fb247-0097-414e-a249-0ae8b01ce340)

And we finally get our flag:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/12e0afde-7e91-411a-8d42-5183d72cc130)

HTB{GSH33ts_4nd_str4ng3_f0rmula3_byp4ss1ng_f1r3w4lls!!}


