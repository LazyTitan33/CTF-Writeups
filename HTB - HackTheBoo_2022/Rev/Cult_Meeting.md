Running the binary with `ltrace`, we can see it doing a string compare where the passphrase is leaked. 

![image](https://user-images.githubusercontent.com/80063008/198257408-bdd4e192-efa3-421f-bb45-958fb414a9bd.png)

Connect to the challenge using netcat, give it the passphrase and get the flag.

![image](https://user-images.githubusercontent.com/80063008/198257515-a2ef9387-926b-42a4-8382-55f8613b9bea.png)

HTB{1nf1ltr4t1ng_4_cul7_0f_str1ng5}