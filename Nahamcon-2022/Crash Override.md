![image](https://user-images.githubusercontent.com/80063008/166219643-55c3b9e8-2cde-4e75-8656-7a6c7b7f9d0d.png)

We get the source code of the binary that run on the server.

![image](https://user-images.githubusercontent.com/80063008/166219799-a147b426-68d2-42b9-9c3f-c471d2d9bfa6.png)

This takes an input buffer of 2048 bytes and on a segfault it goes to the win function spitting out the flag. We can pass it more than that, for example 2100 A letters using python and can see the flag.

`python3 -c "print('A' * 2100)"|nc challenge.nahamcon.com 32129`

![image](https://user-images.githubusercontent.com/80063008/166219908-77eb78b3-4034-4a73-b9f5-38e1226c0b75.png)
