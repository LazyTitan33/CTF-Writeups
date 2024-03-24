# improper-configuration

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/3740cbd5-6aad-469c-845e-5201d5a61722)

# Solution

We can do some dynamic analysis on APK files by running the application in an emulator. An online one that I used is [appetize.io](https://appetize.io/upload) which allows us to see what the app does and if we create an account (I used a temporary email), we can also get network logs and more. For now, we just see the app saying to "check the rest in strings":

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/aa3c9420-52a7-4e30-b45a-6b0f1b8cd9e1)

I've used [this](http://www.javadecompilers.com/apk) online APK decompiler that gets me the decompiled JAVA code, saved it locally and grepped for that initial weird string and found the app name. I could also see the app name in the list of apps in the emulator so I didn't really need to check the strings:   

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/2600c45c-5e09-474f-a946-e49792a826c0)

That's it, that's the flag: `wlwkfwo2-3cscase-wdc`

Note: This was extremely annoying and frustrating as there was no indication in the challenge description that the flag is in a non-standard format. This was an absolute guess game. Incredibly horrible challenge.
