# Under The Bridge

### Challenge Description
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/57b335af-f547-4ac3-9e68-0046697f3205)

### Solution
Accessing the provided link, we can see a bridge:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/6a707d37-7c3b-4c4a-b2b0-29cf71b0cf67)

After looking around for street signs, shop signs and other indicators, I decided to take a cropped screenshot of the bridge all zoomed out like this:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/ab053840-9296-43ad-9308-177fbee05a9b)

I uploaded this into the russian site https://yandex.com which is much better at recognizing landscapes than google is in my experience:
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/e2c132fe-2052-41af-8b5d-ea3b703ab4f7)

The very first result looks the same and indicates to us that this is the `Rick Astley Bridge`:   
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/a9bedbbe-10f2-4ea1-9620-40f2373d78a4)

Clicking on the link, we get the exact GPS coordinates where the picture was taken:
https://commons.m.wikimedia.org/wiki/File:Rick_Astley_bridge.jpg

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/05edb7ab-bd9a-4cc9-b39d-382e7b56ce16)

The map even clearely indicates the road nearby:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/65a58ed6-b955-4cde-98bb-b2a8beadabd5)

We find that in the challenge map and get our flag:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/1530b1ba-dcbc-48b3-ad19-dc706fe5274a)

flag{fdc8cd4cff2c19e0d1022e78481ddf36}
