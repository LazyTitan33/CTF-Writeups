## What's in the Box?

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/995b2656-72fd-4206-99c4-d46827c290e9)

## Solution

This challenge provides us a Makeself self extracting bash script:  

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/cb72e5eb-617f-46e4-8384-ef91e0d401dc)

For such scripts, we can carve out the archive itself skipping the first 715 lines because we can see the bytes starting from line 716.  

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/b7ccbc78-68eb-4743-863f-c9cd221b9e89)

```bash
 tail -n +715 thebox > archive
```
And now we've taken it ou manually. I had to do this because I kept getting python related errors and I was too lazy to resolve them. But we confirmed we extracted the archive:  

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/fd40f0e4-d6fd-4c67-b388-0491b63a3584)

The archive contains a python script that starts with a lot of flags:  

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/55de4c1b-981a-445f-8c1d-68cae5819beb)

Then ends with some more, but based on the code, we don't need to do anything other than run it, give it the hardcoded pin code and it should spit out the correct flag:  

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/5c9c92aa-4714-4a96-aed8-0da34be485f3)

And we are correct:  

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/81cd2352-5713-4183-bd26-6c937c05b47e)

`flag{da0a0a25f5b35fbf99e3351997bfc4c8}`
