# No need for Brutus

![image](https://github.com/user-attachments/assets/282ccb11-f7bd-4ea4-b882-f80bfad01710)

## My Solution

The title is a clear reference to Caesar and the Caesar Cipher also known as ROT13. However, in this case, using [cyberchef](https://gchq.github.io/CyberChef/#recipe=ROT13(true,true,false,10)&input=c3F1aXFoeWlpeWNmYnVkZWR1dXR2ZWhyaGtqa2k) we just need to rotate 10 times to find a readable string:  

![image](https://github.com/user-attachments/assets/6fe3f1fe-8665-4a9d-b211-e1cae59b59b8)

And then MD5 sum it using [cyberchef](https://gchq.github.io/CyberChef/#recipe=ROT13(true,true,false,10)MD5()&input=c3F1aXFoeWlpeWNmYnVkZWR1dXR2ZWhyaGtqa2k) since we are already in it, to get the correct hash for the flag:  

![image](https://github.com/user-attachments/assets/89e713f8-4748-42d5-bb32-3ed718b30ef8)

flag{c945bb2173e7da5a292527bbbc825d3f}
