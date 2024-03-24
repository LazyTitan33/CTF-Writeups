# sided-curl

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/3753de14-03ac-438a-8bee-71b8e923ea9c)

# Solution
We start the challenge with a hint stating that there's an admin panel on localhost:8000 and we can fetch content by entering a URL in the box:  

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/4bfb2192-94bd-45a7-b728-24f6ceba91f8)

Trying a test link with google, we see that it is accessing google but then adds a `.png` to our endpoint:  

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/3a585ee5-1c1c-4112-a8e0-5f1ec90947d4)

Trying localhost directly obviously doesn't work and in fact, anything we have at the beginning that isn't `http://google.com` would present with the same `Invalid URL` error message:  

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/7a33ecb0-dc9f-4f36-a64e-3121afbae395)

Inspired by [this](https://bugs.xdavidhu.me/google/2021/12/31/fixing-the-unfixable-story-of-a-google-cloud-ssrf/) blog as well as other `SSRF` related cheatsheets, we eventually reach this sort of payload. Notice the `#` at the end that we use to break the URL and stop it from adding the `.png`:

`http://google.com@127.0.0.1:8000/admin#`

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/da155058-40d1-47d3-9540-4f16e59006fd)

We can see that it requires a GET request with username and password as parameters however, we quickly hit another filter regarding length restriction.

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/daaea8e5-7e89-4bf8-8bb6-10184f550324)

However, luckily for us, there are numerous ways to say `localhost` and we can shorten the payload to get the flag:  

`http://google.com@0:8000/admin.php?username=admin&password=admin#`

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/759d22be-1914-4dd7-ace1-b0e2e6c5ba1f)

`CTF{36555d5ff86de7b5a572f4c01cbfc8c677b1c1287d9c043618442d248d940b65}`
