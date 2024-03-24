# easy-hide

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/28fb1cdb-c22a-482b-a9b9-eae825f719fe)

# Solution

Running [foremost](https://github.com/korczis/foremost) on this PNG, we notice there's a `JPG` hiding inside and the tool extracts it for us:  

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/29a7a3d1-aa8d-4a21-b417-209f0d5762bd)

In the output directory, we find a `.zip` that we can decompress and get the .jpg:  

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/bc910e6f-adef-4696-a6a7-ac5085558ae4)

However, if we open it with [ghex](https://wiki.gnome.org/Apps/Ghex), we can notice that it has a broken header:  

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/0573d073-3e1c-416e-9a1a-6cd29bf1fe7d)

From within kali, I just opened a known good .jpeg with a proper header to use as an example:  

```bash
ghex /usr/lib/python3/dist-packages/docx/templates/default-docx-template/docProps/thumbnail.jpeg
```
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/8109fb9f-b24e-4cb8-9f06-2d490f5c2bbb)

Modified the first line of bytes to fix the jpeg header and then I could open the picture and get the flag:  

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/1c09fd23-f032-4d26-a3e1-6fdc204f093f)

`UNR{sunIZZsunshine}`

Note: It's a bit annoying when the flag format changes unexpectedly in the middle of the CTF but it makes sense for this challenge since we don't want to manually copy a lot of characters. However, it would've been nice if any CTF format changes are specified in the challenge description.
