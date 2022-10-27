On the mainpage, we have a login screen and the option to register a new user.

![image](https://user-images.githubusercontent.com/80063008/198249799-a27dd90d-f934-438c-bfec-c5da32f5a64b.png)

We see in the source that there is already an admin user with a hash that we can't crack. I tried.

![image](https://user-images.githubusercontent.com/80063008/198249904-2291f82f-b008-449d-b4a9-336a2245dd59.png)

Looking further however, we notice some unsanitized user input into the SQL query so we should be able to inject it.

![image](https://user-images.githubusercontent.com/80063008/198250033-4ffba2d8-f3de-4244-b159-34ff5aec9589.png)

I registered a user with a password I know and see what it looks like in the database. To be able to see that, I just built the docker and went into it using.

```bash
sudo docker exec -ti horror_feeds sh
```

Accessed the mysql database and listed the users to see my new user's hash.

![image](https://user-images.githubusercontent.com/80063008/198250326-af433b35-383d-4f48-a1e4-288f1d06b5c0.png)

I tried to overwrite the password for the admin user with my user's password hash. Got an error that there's a duplicate entry.

![image](https://user-images.githubusercontent.com/80063008/198250376-ee8b6516-16cb-4140-ba18-cae7f0436179.png)

I Googled how to overwrite that entry.

![image](https://user-images.githubusercontent.com/80063008/198250403-bd7cf1c6-f1a8-4c72-aeeb-f68cef181c33.png)

Stack overflow provides an answer.

https://stackoverflow.com/questions/7206822/inserting-into-a-mysql-table-and-overwritng-any-current-data

![image](https://user-images.githubusercontent.com/80063008/198250444-ffbf0540-6861-423d-b046-ff265ae0e67e.png)

`Insert into` apparently has a `On Duplicate Key Update` which I can use to overwrite the entry.

```json
{"username":"admin\",\"$2b$12$4UaEV/.A9Ne7aVKWDcWNBexvPO9VAk9niboRcji5jamknEXWws.BW\") ON DUPLICATE KEY UPDATE username=\"admin\", password=\"$2b$12$4UaEV/.A9Ne7aVKWDcWNBexvPO9VAk9niboRcji5jamknEXWws.BW\"#","password":"test"}
```

![image](https://user-images.githubusercontent.com/80063008/198250499-1a2f8668-ef8b-45c6-8d04-a778fe468855.png)

Now I can log in with admin and see the flag:

![image](https://user-images.githubusercontent.com/80063008/198250566-08bf2f68-0498-4ed9-9141-ea50c6c55bec.png)

HTB{N3ST3D_QU3R1E5_AR3_5CARY!!!}
