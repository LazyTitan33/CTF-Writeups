![image](https://user-images.githubusercontent.com/80063008/169348211-d0175dde-a608-4603-8d67-7acf3c7c11b3.png)

We get a lot of files from Event Viewer and we are tasked to find the flag. We read through them, filtering for errors and warnings. We come across one that's interesting.

![image](https://user-images.githubusercontent.com/80063008/169348312-871b934c-3b7b-4a01-bcce-db0c8cbb7969.png)

Definitely looks malicious. We have two stages in the picture above. Further down in the code we can see that stage two is reversed:

![image](https://user-images.githubusercontent.com/80063008/169348491-3d4d8a30-1826-4c03-8ac9-75f06509a3d2.png)

Then there is some XOR-ing action going on.

![image](https://user-images.githubusercontent.com/80063008/169348833-7ad0780a-71a9-4311-95e4-b4b9a7080f2b.png)

If we pass the 1st stage to Cyberchef, decode from hex and XOR it using the value found in the code we get half of the flag.

![image](https://user-images.githubusercontent.com/80063008/169348570-5db0f02a-efd1-4b33-9693-8b5f21016ba7.png)

We repeat the process with the 2nd stage but reverse it at the end and we get the second part of the flag.

![image](https://user-images.githubusercontent.com/80063008/169348700-83e3bc9f-d20c-4b44-a2eb-dfdb1b1a5d69.png)

HTB{b3wh4r3_0f_th3_b00t5_0f_just1c3...}
