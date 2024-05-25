## Kitty Kitty Bang Bang

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/ea47c22f-ddb6-4d03-a501-16327e4bd7fa)

## Enumeration

We can use `jadx` to decompile the provided apk file.  

```bash
jadx -d ~/LAB/CTFs/NahamCon-2024/mobile/decompiled ~/LAB/CTFs/NahamCon-2024/mobile/com.nahamcon2024.kittykittybangbang.apk
```

From the source code we can see that it is outputting the flag into the log when tapping the screen:  

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/15184cfd-7d95-48ed-9b6b-2818d068d59a)

## Solution

So I used [this](https://appetize.io/) website, made an account with a 10 minute mail, turned ON the ADB Tunnel:  

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/adf9414a-08dd-4319-b957-ebaecd02851d)

Then locally, on my kali machine I started `adb logcat` grepping for the flag while clicking in the application to have the cat go bang a bunch of time.

```bash
adb logcat | grep -oE 'flag{.*}'
```

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/d071114a-b623-436c-bd57-b3bce45eb4da)

After a few taps, we've found the flag:  

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/9eaa0ffd-bb1a-4dd0-b74f-d49e0350cc5c)

`flag{f9028245dd46eedbf9b4f8861d73ae0f}`
