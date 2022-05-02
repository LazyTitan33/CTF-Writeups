![image](https://user-images.githubusercontent.com/80063008/166224704-210f794b-bf43-4981-9ef6-48a9857f3509.png)

Runing the file command on this we can see it is an archive.

![image](https://user-images.githubusercontent.com/80063008/166225133-2598d379-7f3c-41d5-ad3a-fe987cfc556d.png)

We unarchive it and get a few other files. The meta.json file contains a lot of data that we don't need to parse through. Doing a file on the .bin files only gives us data which doens't help. 

![image](https://user-images.githubusercontent.com/80063008/166225184-3f841175-89e2-4682-9a85-6d5ae3637191.png)

However if we try to read one of the .bin files, we can see a strange file header.  
![image](https://user-images.githubusercontent.com/80063008/166225361-30784b88-55f3-47e3-bd56-4f85ca007fad.png)

We can google it and find a software called Logic Analyzer.
![image](https://user-images.githubusercontent.com/80063008/166225545-9a492aea-63c4-47d8-9010-226ad71e2a9d.png)

I was lucky to be familiar with this file type as I have encountered it in a past CTF. I already had the software installed so we can go ahead and open the .sal file using [Logic Analyzer](https://www.saleae.com/downloads/) from Saleae.

![image](https://user-images.githubusercontent.com/80063008/166225706-fba7cd57-9d31-4f82-a28f-665afefe32e0.png)

There's a little something extra after the flag which I'll let you discover on your own :))

flag{5c4596b35aeb122209b34cccfcdb56c1}
