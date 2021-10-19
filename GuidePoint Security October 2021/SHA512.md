
We are given a flag called secret.tc


![image](https://user-images.githubusercontent.com/80063008/137866702-c422ec5d-cb2c-4802-a562-6917e2f01559.png)


Some Google-fu research shows that it is a TrueCrypt file. I installed TrueCrypt and it required a password to mount the file as a volume.

![image](https://user-images.githubusercontent.com/80063008/137867198-43aaa0e5-36ee-44d7-8bb1-98bddb14bdc1.png)

Did some more Google-fu and found there's a linux tool called TrueCrack which can crack the password for such files.

The help section of the tool mentioned a key type as an option and Sha512 was one of the options. Which rings back to the title of the challenge.

![image](https://user-images.githubusercontent.com/80063008/137866772-59ea0389-57ae-4450-a917-924c0f3c892d.png)

Ran the syntax below to crack the password:

```bash
truecrack -t secret.tc -w /usr/share/wordlists/rockyou.txt -k 512
```

![image](https://user-images.githubusercontent.com/80063008/137866792-bc5c14cd-90ec-43a6-856b-051ddc92f36a.png)

Got the password, and used it to mount the file. Then opened it in Notepad++.

![image](https://user-images.githubusercontent.com/80063008/137866842-b93c2426-8a11-486e-8be9-ef5d4fda9ffb.png)

StormCTF{Misc4:c7B645DDa98414f7a7D0a23EeA36eFa1}
