![image](https://user-images.githubusercontent.com/80063008/166223740-61c99cee-1616-4ea9-a880-5df99d6df6fe.png)

Trying to unzip the file, we are prompted for a password. We can use zip2john to extract the hash and then pass it to john to be cracked.

`zip2john gpx.zip >hash`  
`john hash --wordlist=/usr/share/wordlists/rockyou.txt`

![image](https://user-images.githubusercontent.com/80063008/166223937-6e28b0a5-daba-4b25-8ec6-1b4036cc5e88.png)

After we crack the password we are able to unzip it and we get a lot of .gpx files. 252 to be exact.

![image](https://user-images.githubusercontent.com/80063008/166223983-e60380b4-754f-46f1-aee3-2b605e3cf015.png)

After a bit of research on what this file type is, we come across a website called https://gpx.studio/. We can simply drag and drop all of the files at once and it will process the data from them.

![image](https://user-images.githubusercontent.com/80063008/166224066-65b5fd92-e0ec-4ce9-81d0-1ba4c79113db.png)

Zooming in and out for a bit allows us to see the flag.

![image](https://user-images.githubusercontent.com/80063008/166224174-de211a3f-9e21-4971-a0e2-64a927d41321.png)

flag{gpx_is_cool}
