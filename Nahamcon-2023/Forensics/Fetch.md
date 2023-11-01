# Fetch

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/81f3d65d-ec8d-4e40-b01b-31deadfd6508)

For this challenge we get a file I haven't seen before. A Windows imaging image:

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/876185c6-113f-4bb2-9244-07c925fa495d)

After some research with Google, we find that there are tools we can use to parse these in Linux and in Windows. Initially I install `wimtools`.

```bash
sudo apt-get install wimtools
```
After that I mounted it to a folder and found a bunch of prefetch files:

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/2e676c67-295f-4fad-9bd7-332e957c137e)

I read some articles trying to find some easy ways of parsing the information in these files as there were quite a few, a real "needle in a haystack" situation.

https://www.hackingarticles.in/forensic-investigation-prefetch-file/

Eventually I found this Windows tool as it was easier for me to have a GUI in this instance:
https://www.nirsoft.net/utils/win_prefetch_view.html

My aim was to look into the prefetch files of stuff that had user input like, notepad, cmd, powershell and eventually I found wordpad:

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/a6a290f1-a776-4c5e-9101-2ac88c297995)

I used cyberchef to quickly convert it to lowercase:

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/f8c11c07-5aa0-481b-8ce2-d21765726706)

flag{97f33c9783c21df85d79d613b0b258bd}
