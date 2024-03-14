# PackedAway

## Solution 
Running strings on the provided binary, we can tell it is [UPX](https://upx.github.io/) packed:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/7b77e2ef-1713-4621-b4d6-5ce98a7241a0)

We can use upx to also unpack it:  
```bash
upx -d packed
```
Now that the binary is unpacked we can run strings on it and grep the flag:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/36a0dcf8-c46f-4618-86b6-da36fab71f4f)

`HTB{unp4ck3d_th3_s3cr3t_0f_th3_p455w0rd}`
