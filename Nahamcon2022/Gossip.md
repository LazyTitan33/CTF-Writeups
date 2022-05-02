![image](https://user-images.githubusercontent.com/80063008/166217583-6342ae9a-579d-4446-9c7e-cae2da7d6f06.png)

After SSH-ing into the box, a standard enumeration process is to look for SUID binaries. We can do that with:

`find / -perm -4000 -ls 2>/dev/null`

The results show some standard SUID binaries but also one that I haven't seen before:

![image](https://user-images.githubusercontent.com/80063008/166217838-db8fa781-d6e7-4b1c-9497-96658dd4a1cb.png)

Looking it up on [GTFObins](https://gtfobins.github.io/gtfobins/dialog/), we see it can be exploited to read privileged files.

![image](https://user-images.githubusercontent.com/80063008/166217925-55b1f076-afe5-4097-8c44-9e43ae8fbcef.png)

But we can't read /root/flag.txt because it doesn't exist as per the challenge description. Let's see if an id_rsa key exists for root in order to escalate our privileges.

`/usr/bin/dialog --textbox "/root/.ssh/id_rsa" 0 0`

It seems root does have a private key that we can steal:
![image](https://user-images.githubusercontent.com/80063008/166218216-081e13f6-bbb6-4ba5-95a3-16502abe9059.png)

We can copy and paste it making sure we have a new line at the bottom and no unwanted spaces. We use `chmod 600 id_rsa` for the file to have the correct permissions then use it to SSH as root.

![image](https://user-images.githubusercontent.com/80063008/166218322-1977544e-8bc0-45de-92b0-82da9c641ce0.png)

We see only a **get_flag** binary in the root folder and when we run it, we get our flag.

![image](https://user-images.githubusercontent.com/80063008/166218352-93578898-eb21-473d-8b6a-cc43ab0354c6.png)
