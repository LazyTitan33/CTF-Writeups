![image](https://user-images.githubusercontent.com/80063008/169344428-a0460c09-b243-4252-b60d-d40ba48bd167.png)

When running the app, nothing seems to happen. So we load the app in Ghidra, look for strings and can see a lot of strange names.

![image](https://user-images.githubusercontent.com/80063008/169344715-deb6e745-6ed6-4174-9c40-3b78c1f033b7.png)

Looking closely, some of these names are also in the provided output.txt file. Looked up each word one by one from the provided output.txt file and figured out that they represent specific letters, numbers and characters. We filled out the chars one by one. I'm sure there are better ways but I wasn't in a rush.

Here is an example:

![image](https://user-images.githubusercontent.com/80063008/169345005-afb7920e-2623-4dd7-a26d-83c069151ed5.png)

Eventually we get all the required characters:

![image](https://user-images.githubusercontent.com/80063008/169345371-0f8d2d63-43fe-4288-9d17-9d8f1ec68bcc.png)

HTB{l1n34r_t1m3_but_pr3tty_sl0w!}
