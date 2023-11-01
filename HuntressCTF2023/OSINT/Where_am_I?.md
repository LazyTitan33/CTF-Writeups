# Where am I?

### Challenge Description
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/c274f7bf-a8c1-495e-a974-8434e4fc4369)

### Solution
This one seemed closer to Stego than OSINT but indeed, for OSINT situations where you have some pictures to analyze, you would look at the metadata first. There was a lot of metadata in this picture, including GPS coordinates which I wasted some time on.

But then I scrolled up and saw the `Image Description`:

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/45b0f7d2-c18b-422c-8d31-b4237e47fe09)

Now we can get the flag:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/d8ef451d-47e1-420a-b4f3-85b5efefc369)

A bash oneliner like this would do it:

```bash
exiftool -ImageDescription PXL_*.jpg|awk '{print $4}'|base64 -d
```
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/45674d5e-8397-4cee-8ed6-5c19b3eebedb)

flag{b11a3f0ef4bc170ba9409c077355bba2)
