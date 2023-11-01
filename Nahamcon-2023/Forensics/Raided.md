# Raided

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/9d39a10d-1e33-495d-9aa0-f00f21eaba5b)

This was a fun challenge to begin with in the Forensics category but I was a bit dissapointed at the end. 

The memory dump is from a Linux operating system. We can use strings to find the kernel version and it seems to be a Kali kernel.

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/ebe3b139-e9a2-4ee3-988a-db929f4d63d4)

My first idea was to build a profile for Volatility2 as that's the one I'm mostly used to using. We can search the release history to find the one we need:

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/79adde56-f21e-4cf5-83a2-f2132b7543c0)

The release history gives us the file we need right away as it is clearly dated in May.

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/2816c29a-c526-4d69-80cb-e11646575750)

The version for various platforms can be found here:

https://cdimage.kali.org/kali-2023.2

I downloaded the VM, ran it in VMWare, booted up and installed Volatility to make the module.dwarf file and create a Profile:

```bash
git clone https://github.com/volatilityfoundation/volatility
cd volatility/tools/linux/
make
sudo zip $(lsb_release -i -s)_$(uname -r)_profile.zip ./volatility/tools/linux/module.dwarf /boot/System.map-$(uname -r)
```

The first issue I encountered was during the `make` process but googling the error I was able to quickly fix it:

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/ba739d67-13a8-43c6-8a94-40f1150d7276)

I got my profile but sadly it didn't work. It wasn't even detected by Volatility. I spent quite some time on this as it involved some research and downloading some big files.

I got frustrated and reverted to using `strings`. I found some information this way. Knowing we are dealing with Kali, I grepped for the zshell to find the name of the user:

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/95fb77cd-a653-4d99-a8f7-d4814853e1da)

I then looked for other stuff where the user `l33t` name comes up. One of them was him using an SSH key to connect to an IP address.

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/a207d6b1-a168-46f8-8322-edca7cdbc00f)

I made a screenshot and put it to the side. I figured maybe we need to get the file dumped from memory somehow, with Volatility. So, I switched to Volatility3. I had the idea to create a symbols table for it since I already had the VM with the proper kernel running.

```bash
sudo apt install linux-image-amd64 linux-image-amd64-dbg
git clone https://github.com/volatilityfoundation/dwarf2json
cd dwarf2json
go build
./dwarf2json linux --elf /usr/lib/debug/boot/vmlinux-6.1.0-kali9-amd64 >kaliprofile.json
```
The process killed itself a couple of times and then I increased the VM RAM to 8GB. It seems it is required to have at least 8GB of RAM for dwarf2json to complete. I was finally able to create the symbols table, copied the resulted json file in `/opt/volatility3/volatility3/framework/symbols/linux` and now we can run commands and list processes running at the time of the memory dump:

```bash
vol3 -f raided-challenge-dump-vmem linux.psaux.PsAux
```
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/39c26e3b-061d-40d0-a6b8-06daebc2a984)

Again we see the use of the RSA key to SSH into that IP address. I kept looking for ways to enumerate files in Volatility3 like you can with Volatility2 but gave up and reverted back to `strings`.

I grepped for the `BEGIN OPENSS PRIVATE KEY` that is within the RSA key and added the `-A 10` flag for grep to show 10 lines after the match and I found the key.

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/8fd5ebd3-4f24-4f22-a58d-d76e4528a4ac)

When I saw this, I facepalmed. I could've been done within 5 minutes with two strings + grep commands. I enjoy memory forensics but this one left me with a sour taste, even though at least I learned how to build the symbols table for Volatility3.

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/17d886ee-4d35-490f-9f1b-354b67dd0340)

Anyway, we SSH in just like the user and it turns out that the IP is valid and live and we get the flag:

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/0d29a325-2d3a-4fd5-8bb1-49ff58991765)


flag{654e9dc4c424e25423c19c5e64fffb27}

