# secrets-of-winter

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/cca5799a-4e08-4043-8ec3-b31157c41562)

# Solution

At least on this challenge, we know that the flag is not in the usual format:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/cd8bba95-aa95-498f-9fbe-70dc05588198)

Running `exiftool` on the image, we can find two base64 strings:  

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/7eac7fe8-736b-4727-a319-4852f8e4043c)

```bash
echo Y2g0bDF9|base64 -d
```

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/a7e5d7cd-907c-4983-9f72-ee4331522858)

```bash
echo ZjFuaSRoLXRoMy0=|base64 -d
```
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/4722a2b6-2463-4c57-aad3-6a2f0acba2d2)

So it looks like we have the last 3 words for now. I also ran [stegoveritas](https://github.com/bannsec/stegoVeritas) on the picture and it extracted all the different colored layers of the picture in a folder. I went through them several times looking for hidden characters/words, zooming in and out, until I found the beginning of the flag on a building off in the distance with very small font:  

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/66baea36-9452-4ef3-92e0-f09f4e36783e)

It's very difficult to see but we eventually build our full flag: `ctf{g3t-3xiftool-to-f1ni$h-th3-ch4l1}`
