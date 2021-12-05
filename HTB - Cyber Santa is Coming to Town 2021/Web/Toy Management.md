![image](https://user-images.githubusercontent.com/80063008/144764992-42912af2-3133-430c-95b9-db02b3d64343.png)

We are greeted with a login screen.

![image](https://user-images.githubusercontent.com/80063008/144764999-e95f7520-5ba3-42ad-a14d-d076078a131a.png)


Flag is in the database so at first I thought I would need to do some SQL injection to get the flag from the table.

![image](https://user-images.githubusercontent.com/80063008/144765001-aade9949-c45e-4149-93a8-4419d006bfdc.png)


We have credentials from the database.sql file

![image](https://user-images.githubusercontent.com/80063008/144765015-67ff25d3-adcd-47f9-aa33-324de1622233.png)

![image](https://user-images.githubusercontent.com/80063008/144765016-eb539ba6-1d3b-46b2-8223-94cfc925779c.png)

Logged in with admin on my local instance and immediately saw the flag. Is it that easy?

![image](https://user-images.githubusercontent.com/80063008/144765019-5e3864c3-621e-4674-9a20-7ec0bba92754.png)

No, on the remote website we get an invalid password. However it seems we have SQL injection directly on the login screen. With the standard sql injection ```' or 1=1-- -``` we get logged in as manager.

We do get a JWT token however the secret is random.

With this SQL injection, we were able to get on as admin:

```
admin'-- -
```
![image](https://user-images.githubusercontent.com/80063008/144765091-8d7e8d60-d16e-4eec-a7cd-dc3ef0f68579.png)

HTB{1nj3cti0n_1s_in3v1t4bl3}

