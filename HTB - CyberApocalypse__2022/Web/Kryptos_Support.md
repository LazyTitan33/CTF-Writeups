![image](https://user-images.githubusercontent.com/80063008/169328654-c1368352-ac15-4a27-b8ae-8261d5572df4.png)

We land on a page where we can report an issue.

![image](https://user-images.githubusercontent.com/80063008/169328738-acfebd9f-dc14-4bc2-921e-2e635d795711.png)

Intercepting the POST request in burp we can try an XSS payload to steal the cookie of whoever checks the issue tickets.

![image](https://user-images.githubusercontent.com/80063008/169328925-696d758e-33e6-4992-84fe-4ec0f0698e00.png)
![image](https://user-images.githubusercontent.com/80063008/169329219-3a76d19f-4a7a-4b91-9606-d36c0083c689.png)

We do in fact get a cookie. Let's use it:

![image](https://user-images.githubusercontent.com/80063008/169331769-e27d1e45-6bb4-43ce-8248-43a5d1cea169.png)

We seem to be a moderator and going to the settings page we have the option to change the password. We also see a `uid` field of 100 for the moderator.

![image](https://user-images.githubusercontent.com/80063008/169329963-d106ad44-e48f-4ae0-834d-e13e475d52d8.png)

We can abuse an IDOR vulnerability here and change the `uid` from 100 to 1 as that is generally presumed to be the admin.

![image](https://user-images.githubusercontent.com/80063008/169330150-5ce56714-156a-4dd4-9161-8b0605dac573.png)

We are succesful in changing the admin password. Now we can use the /api/login endpoint to log in as the admin and get a cookie.

![image](https://user-images.githubusercontent.com/80063008/169330859-c0d35409-7a79-4f1e-8366-02c3c828b93f.png)

We pass that cookie to the /admin endpoint and get our flag.

![image](https://user-images.githubusercontent.com/80063008/169331312-75afa986-d2d4-4f82-9208-5c57c6a28dc1.png)

HTB{x55_4nd_id0rs_ar3_fun!!}
