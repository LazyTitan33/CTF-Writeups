### Challenge description

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/8967d207-47c6-4c62-a0d6-2998ee9f337d)

We start off this challenge with a simple email file:

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/be55af36-0a6c-4443-aad8-f4f2a357221c)

However, something jumped out at me. There is an attachment with a double extension, `.pdf.html` with a large Base64 blob.

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/0368de9d-0c2f-413a-acab-b9327b8193cb)

DISCLAIMER: _The following few steps are a bit dangerous if you don't know what you are doing or are doing it in an insecured environment as it involves some dynamic forensics._

I first saved this HTML file locally:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/155b39e8-d338-44db-ac77-a964f41d0e6f)

And hosted it using a python webserver. When accessed, the browser immediately downloads the next stage which is an apparent .zip file.  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/216917f4-dfd1-48ca-8239-a4578ef92beb)

Indeed it is a zip file which we can decompress and find another stage. Another file with a double extension of .pdf.js.  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/c911d771-bc39-4678-b99f-3624979bac82)

The javascript file contains a lot of comments/garbage and obfuscated variables.  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/667472c8-b38f-44c1-8456-66ebc4a037f3)

I cleaned it up a bit by removing the comments and renaming some variables until it made more sense to me and realised what it is doing.  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/8491a4b5-dce7-490b-8439-e90cc9a9d528)

The next stage is concatenating all the parts, then replacing the `s` with nothing, the `V` with nothing and the `sV` with nothing. I did that manually using `sed` and noticed that the resulted blob looked like hex so I hex decoded it using this oneliner:

```bash
cat stage4|sed 's/s//g'|sed 's/V//g'|sed 's/sV//g'|xxd -r -p > stage5
```

This stage has a lot of variables. By a lot, I mean a lot.

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/5e33844a-817b-46bf-baa6-df946857ec7f)

Thanks to the preview window in Sublime, I noticed some larger blobs which turns out are base64 blobs that are concatenated.  

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/81336a7b-ce9b-4aa0-80d2-5f3831122fbc)

I put them all together and decoded them in Cyberchef to find a Powershell command execution.

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/f34d62bc-b8e5-413c-bdc7-9bedf86ca9bc)

It was piping everything to IEX to detonate so I replaced IEX with a harmless `echo` and ran it which revealed yet another stage. I lost track of stages at this point.  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/2f31429f-0a28-428a-9c4e-3f9500802dba)

I stared at this code for a while trying to understand it. A closer look shows that it is doing some XOR operations on some HEX bytes:
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/ffc0731c-2d92-42e9-845e-cb1d825be2bf)

Realising this I took each byte array, unhexed it and XORed it with the specified Decimal using Cyberchef until I found the one hiding the flag:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/828ab456-a338-4abd-95b7-4525ea3760e7)

HTB{l0ts_of_l4Y3rs_iN_th4t_1}




