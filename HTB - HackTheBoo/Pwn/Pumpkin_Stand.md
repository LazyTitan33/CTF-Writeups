When launching the given binary, we see some cool pumpking ASCII art, a current wallet of 1337 pumpcoins and the option to buy a shovel or a laser.

![image](https://user-images.githubusercontent.com/80063008/198273526-fb1ac366-7461-429b-b4fa-1721010bc173.png)

I experimented by giving it various numbers I thought it wouldn't expect. I noticed that when inputing a number starting with a 0, the current pumpcoins goes to a large number in the negative.

This behaviour points to an Integer Overflow type of vulnerability. So I tried to buy a laser but when asking me how many I want, I gave it a large number like 999. I repeated the step and then the flag was revealed.

![image](https://user-images.githubusercontent.com/80063008/198273561-2d26f8f1-43b4-46c3-9897-c5fec4db2f56.png)

HTB{1nt3g3R_0v3rfl0w_101_0r_0v3R_9000!}