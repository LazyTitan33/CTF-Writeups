We are given two files.  A trace.pcap file and a binary file called `securetransfer`. There are very few lines in the pcap file.

![image](https://user-images.githubusercontent.com/80063008/198258233-e8fdaebf-b15e-4be0-9d5d-6c7f4783793d.png)

If we follow the TCP stream, we have some content that looks like garbage for now.

![image](https://user-images.githubusercontent.com/80063008/198258277-deab8254-4056-46f0-96b0-027e7055b4de.png)

To copy that content locally I use Wireshark to convert the data to RAW and we get the hex string. 

![image](https://user-images.githubusercontent.com/80063008/198258327-b29db47e-e273-4d6a-b4a1-b14c787c1a33.png)

I copied and saved it in a file I called flag.txt.

![image](https://user-images.githubusercontent.com/80063008/198258344-ad6d567f-93b2-4f7f-a490-c9679a0465a3.png)

I opened the binary file in ghidra and looked through the functions. In this function we notice we have a Decrypt function:

![image](https://user-images.githubusercontent.com/80063008/198258384-000d21be-f845-4723-97c4-e14eafc7fa41.png)![image](https://user-images.githubusercontent.com/80063008/198258411-47d567b2-5c79-4f4c-b97f-d86f719c6504.png)

In the next function we can also see that the binary opens a port on 1337. This can also be noticed by checking the Wireshark capture or using netstat after executing the binary.

![image](https://user-images.githubusercontent.com/80063008/198258444-56384986-c34f-4110-9d03-e5f06c7271e4.png)![image](https://user-images.githubusercontent.com/80063008/198258477-7619b14a-e950-47e2-b90e-bc83e0056878.png)

After gathering this information we read the flag.txt, decode the hex and pipe it to netcat while we have the binary "listening".

```bash
cat flag.txt|xxd -r -p|nc localhost 1337
```

![image](https://user-images.githubusercontent.com/80063008/198258516-96cf1c7c-cab7-479d-9607-f63694d4508f.png)

As it can be seen, it automatically decrypts the content and we get our flag. A oneliner like the one below can also be used while the securetransfer binary is running:

```bash
./securetransfer& \
tshark -r trace.pcap -T fields -e 'data.data'|xxd -r -p|nc localhost 1337
```

![image](https://user-images.githubusercontent.com/80063008/198258575-69bcfd8a-4d2b-43c2-889f-502881d3fc29.png)

HTB{vryS3CuR3_F1L3_TR4nsf3r}
