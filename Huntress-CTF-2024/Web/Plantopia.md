# Plantopia

![image](https://github.com/user-attachments/assets/cc6dd8d7-7100-41f9-b73e-31e8a5b3a114)

## My Solution

We login on the webpage using the provided credentials and notice that the cookie is just a base64 string.

![image](https://github.com/user-attachments/assets/1755895a-c2ca-478e-8c27-286f080685a3)

It consists of the user, 0 and an epoch time.

As you might imagine, just changing the 0 to a 1 gives us access to the admin panel:  

![image](https://github.com/user-attachments/assets/0f59389f-3848-4063-9a2e-452fd598be97)

The app also allows us to see the API endpoints so we know there's a an option to see the logs, to send mail and to update the settings.  

![image](https://github.com/user-attachments/assets/3e5dc645-9422-47eb-95f8-1da9599b153b)

We start by updating the settings of the alert to test for command injection:  

![image](https://github.com/user-attachments/assets/864bff77-70f1-4860-b24f-0cd1d27801ff)

Then we trigger the sendmail function:  

![image](https://github.com/user-attachments/assets/26287167-41e9-4efc-9a02-deebe1329290)

And then check the logs to get our flag:  

![image](https://github.com/user-attachments/assets/1ffe547a-975f-4640-859d-6ef14e514d8e)

`flag{c29c4d53fc432f7caeb573a9f6eae6c6}`
