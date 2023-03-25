For the next challenge in the Crypto space, we can simply connect with netcat to the provided IP and port and we get an Encrypted flag. The public key seems to have a small exponent.

![image](https://user-images.githubusercontent.com/80063008/227491185-410343e3-4f62-4d43-8f2e-0a229424274a.png)

This means we can use our good old friend, `RsaCtfTool.py` which you can get from here https://github.com/RsaCtfTool/RsaCtfTool. We can either leave it running and it will eventually spit out the flag.

Please note that sagemath has to be installed for this attack to be done. You can simply to `sudo dnf install sagemath;pip install -r optional-requirements.txt` from the RsaCtfTool directory. If you get errors about building gmpy, do `sudo apt install libgmp3-dev` and try again. If you get error about sage binary not being installed, make sure to get it from here https://www.sagemath.org/download.html

```bash
RsaCtfTool.py -n 6561831657788149425694861301661479746323090591021707282323926588779254530106072593657744854168880717731602676903001378433383937484930939128266885943288847 -e 3 --uncipher 70407336670535933819674104208890254240063781538460394662998902860952366439176467447947737680952277637330523818962104685553250402512989897886053
```
Now you can go and have a coffee, take a break, or focus on a different challenge. After a while, we get our flag:

![image](https://user-images.githubusercontent.com/80063008/227500656-a3562617-ff7c-425f-b5ca-7611059cc57a.png)

HTB{5ma1l_E-xp0n3nt}