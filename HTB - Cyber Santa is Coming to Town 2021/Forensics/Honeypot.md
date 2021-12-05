![image](https://user-images.githubusercontent.com/80063008/144763622-6315707a-32f5-423b-8ae1-a98bff33e16d.png)

```bash
vol.py -f honeypot.raw imageinfo
```

After finding out what kind of image we are dealing with, I usually first check to see what processes were running.
```bash
vol.py -f honeypot.raw --profile=Win7SP1x86_23418 pslist
```
![image](https://user-images.githubusercontent.com/80063008/144763758-f39a1a80-e8a0-4da6-92d8-86d9eb9fe266.png)

We can see some iexplore.exe processes. To be expected considering there was a URL used to download a malware. I also see powershell and whoami being run. Will make a note of that.

Let's see what ports and connections we have listening or established. Especially in this case since the description asks us to find a process PID.
```bash
vol.py -f honeypot.raw --profile=Win7SP1x86_23418 netscan
```
![image](https://user-images.githubusercontent.com/80063008/144763807-640ee76b-7039-4b1e-af7a-3102eb5ccae4.png)

Made a note of a strange quad 4 port.

Since Santa downloaded a malware and the challenges asks us to find a URL, let's check the Internet Exploder history as well.
```bash
vol.py -f honeypot.raw --profile=Win7SP1x86_23418 iehistory
```
![image](https://user-images.githubusercontent.com/80063008/144763823-ddc9fe67-e83b-4473-93bf-041be9d265ae.png)

I'm always wary of .hta files so this jumped out at me.

So we know iexplore.exe was used with PID 3344 to download an hta file.

Let's try to find the file

```bash
vol.py -f honeypot.raw --profile=Win7SP1x86_23418 filescan|grep -i .hta 
```
![image](https://user-images.githubusercontent.com/80063008/144763854-ca0f7fa4-15d7-40c2-b395-d74d5b0a432c.png)

We find it so let's dump its contents

```bash
vol.py -f honeypot.raw --profile=Win7SP1x86_23418 dumpfiles -Q 0x3f4d4348 -n "christmas_update[1].hta"
```
![image](https://user-images.githubusercontent.com/80063008/144763862-034e64e1-14c6-40a8-92a3-bd1d825a81ab.png)

Would you look at that. That looks like a powershell reverse shell. We are on the right track.

Base64 decoding the string, we find it is downloading and executing a file called update.ps1

![image](https://user-images.githubusercontent.com/80063008/144763913-d6a1e280-7d8d-4408-bcd1-134006e8bf34.png)

We can't find the file in memory.
```bash
vol.py -f honeypot.raw --profile=Win7SP1x86_23418 filescan|grep -i update.ps1
```

Back to netscan we notice a lot of powershell.exe processes with PID 2700. Because a ps1 reverse shell was downloaded, it would be running with powershell which has PID 2700.  So I dumped the memory of that PID.
![image](https://user-images.githubusercontent.com/80063008/144763973-bcd5e1e3-8cde-40bb-9e26-7e4e8bf4640c.png)

```bash
vol.py -f honeypot.raw --profile=Win7SP1x86_23418 memdump -p 2700 -D .
```
And we can see the actual content of the script that was run by powershell.
![image](https://user-images.githubusercontent.com/80063008/144763946-36d9d048-30ff-4fff-a00f-bfa849e08f09.png)

We have our IP: 147.182.172.189

Putting all this information together as the challenge requires us.

The URL used to download the malware: https://windowsliveupdater.com/christmas_update.hta
The malicious process PID: 2700
The attacker's IP: 147.182.172.189

Putting it all together it looks like this: https://windowsliveupdater.com/christmas_update.hta_2700_147.182.172.189

However the flag is supposed to be the md5sum of that.

```bash
echo "https://windowsliveupdater.com/christmas_update.hta_2700_147.182.172.189"|md5sum
```

HTB{432fd3de8e42875dee4cef3dc6b1a766}

