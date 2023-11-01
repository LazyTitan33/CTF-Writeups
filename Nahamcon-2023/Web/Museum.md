# Museum

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/95afae1a-bf0a-4a74-b447-ec5ddba97e65)

When we access the webpage, we have the option to view some images:

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/2391c28e-176f-4bd1-a04f-20af3ec44683)

The link is interesting. What else can we browse other than artifacts?

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/10be666d-6e93-4690-83bb-61766c6b66b2)

I fuzzed it with my favorite wordlist for LFI, `LFI-Jhaddix.txt` from seclists.

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/4c139d2c-4eb3-4246-9c06-1e505a79849e)

We can read files which is great because it turns a blackbox approach into a whitebox one:

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/4932d894-a0d9-4235-afc1-3c33c442f4be)

We can't read the flag though.. so sad:

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/20c22430-3680-4598-a7fd-c46c7e049b8a)

Abusing the `/proc/self/cmdline` path, we can see where the app is running from:

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/6f70bff7-0b8f-4634-82f9-d3185ce9f637)

And we can grab the source code to better understand the application and experiment locally.

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/4952f5e5-2adb-45d3-b0df-9da4e90c0544)

We find two interesting endpoints. A `/private_submission_fetch` and a `/private_submission`. The latter seems to only be accessible from `127.0.0.1`. This will become important later.

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/4982bca9-6bf5-4e56-804c-bb01315231c9)

From the source code we can see that from the /browse endpoint we won't be able to read the flag.txt because it is filtered:

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/f0756069-569d-4583-864f-af23f4728e42)

Several hours of experimentation later, we reach a syntax that allows us to actually write abritrary files locally, even overwrite them. The URL encoding was crucial as well. Even when putting the link in the browser. Letting the browser do its own encoding for some reason didn't work for me and the payload wasn't triggering. Same with using localhost instead of 127.0.0.1 (see above).

http://challenge.nahamcon.com:31631/private_submission_fetch?url=http%3a//127.0.0.1%3a5000/private_submission%3furl%3dhttp://127.0.0.1:1337/test.txt%26filename%3dfile.txt

I had saved the source code locally so the link above reflects me accessing another endpoint where I'm downloading test.txt from and writing it to file.txt.. into the /public folder according to the source code, however path traversal is possible there so it could be written anywhere the user running the app has access to.

The problem I was facing for the longest time is what to do with it because this Flask application was running with Debug set to `False`. This means that the application will run in the state it was when it was started. Any changes to its code won't apply unless the app is restarted. 

I even experimented with the `file:///` protocol on the /private_submission_fetch endpoint and I wasn't able to get anything out of it.

Then in the last leg of the race, literally 15 minutes before the CTF ended, I was nudged towards a different angle. I was made to realise that I failed to try the file protocol in the /private_submission endpoint. It clicked into place in my mind and then I ended up with the URL below:

http://challenge.nahamcon.com:31631/private_submission_fetch?url=http%3a//127.0.0.1%3a5000/private_submission%3furl%3dfile:///flag.txt%26filename%3dfile.txt

This copies the flag in the /public directory with the name file.txt and I can read it.

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/70da526b-dab5-4b7a-984a-00dc02a33c05)

flag{c3d727275bee25a40fae2d2d2fba9d70}






