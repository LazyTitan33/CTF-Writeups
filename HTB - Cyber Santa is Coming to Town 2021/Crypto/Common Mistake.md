![image](https://user-images.githubusercontent.com/80063008/144765586-9e19ac74-2fff-426a-a2c5-e0e11b959543.png)

Unzipped the provided file and got an encrypted.txt file

![image](https://user-images.githubusercontent.com/80063008/144765593-9421227b-65ef-4bf3-91bd-4487eb600105.png)

Considering we have the same ```n``` and two different ```e``` and ```c``` means this should be a Common Modulus attack. The title of the challenge hints at it as well.

I converted the hex strings into int using python.

![image](https://user-images.githubusercontent.com/80063008/144765666-0e6b1ce4-ce06-4472-b282-f94a37ece97d.png)
![image](https://user-images.githubusercontent.com/80063008/144765698-e7cdf502-ee1d-4390-99d0-c0ef8e4c7a00.png)

I'm not great at scripting crypto stuff but I did find this script.

https://raw.githubusercontent.com/a0xnirudh/Exploits-and-Scripts/master/RSA%20Attacks/RSA%3A%20Common%20modulus%20attack.py

After fixing the identation issues, I pasted the n, c1,c2, e1 and e2 and I ran the script and I got a decimal value.
![image](https://user-images.githubusercontent.com/80063008/144765747-81a0958a-b79f-4197-a6f1-7bc5f9a36aeb.png)

I modified the script some more to convert the decimal value to hex and then to ASCII.

![image](https://user-images.githubusercontent.com/80063008/144765780-8e063b66-b085-475b-b452-2eae79305ea5.png)

![image](https://user-images.githubusercontent.com/80063008/144765790-a187751a-9b54-4653-8e5f-2ffe6a77df68.png)


HTB{c0mm0n_m0d_4774ck_15_4n07h3r_cl4ss1c}
