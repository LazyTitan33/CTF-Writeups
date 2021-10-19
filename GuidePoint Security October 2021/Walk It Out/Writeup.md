
We are given a hint in the description. It refers to the bad habit of users called "password walking". It is the process of creating a password through a pattern on the keyboard.

![image](https://user-images.githubusercontent.com/80063008/137868186-fce46bdc-0cb9-4e7f-9ae5-97f271706875.png)


Using 7z2john I got the hash of the 7z file.

```bash
/usr/share/john/7z2johnpl Walk_it_out.7z
```
![image](https://user-images.githubusercontent.com/80063008/137868210-1192dfde-f55c-4f7e-a8a9-16b74563c57a.png)


Now I need to generate a password walking pattern and feed it to hashcat. This tool is very helpful in that regard: https://github.com/hashcat/kwprocessor

Hashcat’s keymap walking tool, “KwProcessor”, quickly and easily generates password lists based on keymap walking techniques.

```bash
./kwp -s 1-0 basechars/full.base keymaps/en.keymap routes/2-to-16-max-3-direction-changes.route -o potential_passwords.txt
```
-s= Include characters reachable by holding shift

-0=include all keyboard walking directions

Arguments have boolean values so 1 means ON in case you want to enable only specific ones.

![image](https://user-images.githubusercontent.com/80063008/137868248-07fa31d2-bff8-4ff9-b623-d8bdad476cc4.png)


I enabled all keywalk routes so this generated a text file of 13995209 potential passwords which I passed to hashcat since it's faster. After a short while a password was cracked.

Password: (*&^%$#@!@#$%^&*

After getting the password, we use 7z to decompress the archive:

```bash
7z e Walk_it_out.7z 
```
And we get a flag.txt which contains the flag.

StormCTF{Misc1:27BFcA6050f4054e1fBD4CB0c451b9a7}

