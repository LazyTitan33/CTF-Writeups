This was a very fun and yet frustrating challenge to do. Mainly frustrating because I was going down a rabbit hole with me trying to use Volatility2.

We get the following files:

![image](https://user-images.githubusercontent.com/80063008/227514791-6eed696b-121d-4b16-8d61-fe56895e56b7.png)

The flag encrypted in a file with a weird extension, a memory dump, a linux image json file that was zipped up and a wireshark capture.

Thankfully, we only have one HTTP stream in the pcap file:

![image](https://user-images.githubusercontent.com/80063008/227515166-6eb8afbd-1188-4b86-8214-85b9c6cbab20.png)

Which contains Base64 encoded data:

![image](https://user-images.githubusercontent.com/80063008/227515238-440d706d-45e5-41a4-9086-19f823a97eca.png)

Decoding this, we see a script that seems to be preparing some variables with some values and uses `eval` on them at the end:

![image](https://user-images.githubusercontent.com/80063008/227515561-370ccc49-5776-4720-b05c-e02a9d2d009f.png)

Again, we replace the eval with an echo and run the bash script:

We get another stage that seems to be reversing a payload then base64 decoding it:

![image](https://user-images.githubusercontent.com/80063008/227515662-e6b044d8-35b3-4b0c-867f-945a89c124a6.png)

We like to live dangerously (but no seriously, be careful when doing dynamic analysis) and pipe that over to bash:

![image](https://user-images.githubusercontent.com/80063008/227515742-cd2ad7b1-4160-4c9b-8535-946544a3c6e1.png)

We open this up and clean up the naming convention to make it easier to read and understand:

![image](https://user-images.githubusercontent.com/80063008/227515940-ea59b4f5-72fa-4fb4-8420-fcd98d69e47e.png)

The attacker has defined a function which I called PublicKeyFunc that sets up a gpg public key. There is also a function meant to create the flag file we received. The important part to note in this function is that although the flag is encrypted with a 16 character passphrase, that is passed in the bash terminal as an argument via the echo and `--passphrase-fd 0`

![image](https://user-images.githubusercontent.com/80063008/227517347-9a468cb2-d6c0-422b-8457-cdd9e4777269.png)

This means that, if we find the passphrase in the memory dump, we can use the gpg public key and decrypt the flag.

This is where I went off the rails. In my previous experiences with Volatility, version 3 is much more limited so I didn't pay it too much mind. I looked at the .json file we received and understood it was a conversion made with dwarf2json so we know the Linux kernel. Short story is I tried to create a Linux profile with the same kernel for use with Volatility2 and failed.

I went back on my strategy and did some more research on this json file and found that it can actually be used with Volatility3. It's a symbols table: https://volatility3.readthedocs.io/en/latest/symbol-tables.html I just needed to copy it in `volatility3/framework/symbols/linux`.

Now I can use volatility3 and check out the bash history:

```bash
vol.py -f forensics.mem linux.bash
```
![image](https://user-images.githubusercontent.com/80063008/227518029-8c80a525-b425-420b-9f8e-1f1d43bd05a5.png)

Turns out this was a dead end but a nice rick roll from the creator anyway.

After a while I got annoyed, I went back and tried my trusty tools, the old `strings` and `grep`. I knew now what I was looking for, I just needed to find it.

The original name of the variable that contained the passphrase started with `$DhQ52b6`, I was specifically looking for the section where that was echoed. I found it and I used `-A` to look for specific number of lines after my match. On the fourth line, I found it:

![image](https://user-images.githubusercontent.com/80063008/227518576-25545759-a101-4f5f-bc8c-d6081dabb4e5.png)

passphrase: wJ5kENwyu8amx2RM

I imported the public key:

![image](https://user-images.githubusercontent.com/80063008/227518612-e89f643a-ec02-4501-a3ed-4b594ac9ef6b.png)

Then decoded the flag and entered the passphrase when it prompted me for it:

![image](https://user-images.githubusercontent.com/80063008/227518674-2249c35e-a8bd-4e86-9864-553d2fe8b393.png)

HTB{n0_n33d_t0_r3turn_th3_r3l1c_1_gu3ss}

### Alternative solution

The above was my dumb solution. In hindsight, I could've searched for 3rd party plugins for Volatility3. I had used 3rd party plugins before, however this time I just forgot that's a thing.

![image](https://user-images.githubusercontent.com/80063008/227519026-aa2902b9-c9c9-4583-bd05-5ffff85fcf4e.png)

Apparently there's a very helpful plugin that just straight up extracts gpg passphrases from memory:

https://github.com/kudelskisecurity/volatility-gpg

```bash
wget https://raw.githubusercontent.com/kudelskisecurity/volatility-gpg/main/linux/gpg_full.py
vol.py -f forensics.mem -p . gpg_full
```
![image](https://user-images.githubusercontent.com/80063008/227520411-7afce053-c1af-4d11-98b6-09d37f9be08b.png)


