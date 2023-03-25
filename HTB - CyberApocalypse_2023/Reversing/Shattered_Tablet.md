For this challenge, I opened the provided binary in Ghidra and saw how the flag is printed. This is the order of the variables:

![image](https://user-images.githubusercontent.com/80063008/227557469-27867564-fd9f-420f-a346-cc4b0d8a7466.png)

We can see each character associated with each variable. We just need to put them in the right order: local_48 -> local_48_1_1 -> local_48_2_1 etc.

![image](https://user-images.githubusercontent.com/80063008/227557623-f3577982-0c6c-48e5-9f79-9b7c1b6a5202.png)

I did it manually and got the flag but I'm sure there are easier ways:

HTB{br0k3n_4p4rt,n3ver_t0_b3_r3p41r3d}