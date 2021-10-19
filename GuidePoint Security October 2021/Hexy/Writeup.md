We are given just a single zip file.

![image](https://user-images.githubusercontent.com/80063008/137869702-cc3ac824-9533-4f14-ae0d-70a3fc5ccb8c.png)


It seems to be corrupted.

![image](https://user-images.githubusercontent.com/80063008/137869728-e9874955-607d-46a8-a38f-0dcfcb8df436.png)

But if we open it in hexeditor, we can see a wrong header so we can fix that. Replace the 7 with a 5 since the correct header for a zip file is 
`70480304`.

![image](https://user-images.githubusercontent.com/80063008/137869748-747fd4c9-b310-47d0-ad1b-127425d93a41.png)

We can then try to unzip it but is password protected. So we can use zip2john to get the hash.

```bash
zip2john hexy.zip > hash.txt
```

I first passed it to hashcat to crack in my Windows machine to use the GPU as it's way faster:

```cmd
hashcat.exe -m 17210 hash.txt rockyou.txt --username
```

It failed to crack it. So I added the best64 rule and that helped crack the password: forgetfulness

```cmd
hashcat.exe -m 17210 hash.txt rockyou.txt --username -r rules\best64.rule
```

Unzipped the file and got the flag:

GPSCTF{871daf25893451d1ea8ba3b6736cce52}
