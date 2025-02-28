# Weblog 
![image](https://github.com/user-attachments/assets/9f22e50c-d953-431d-8507-0936eeff49d7)


Attachment: [challenge.zip](https://github.com/LazyTitan33/CTF-Writeups/raw/refs/heads/main/SnykCon2025/attachments/weblog.zip)

## Writeup

I can quickly see a SQL Injection vulnerability in the source code on the `/search` endpoint:  

![image](https://github.com/user-attachments/assets/cd7d7908-332a-420b-89c0-5a24c8f055f3)

Using the following syntax, I can get the admin password hash:  

```text
' union select 1,2,3,4, group_concat(username,password) from users#
```

![image](https://github.com/user-attachments/assets/705da9ec-1673-4b2c-9759-d2845d9baf65)

Luckily the hash is crackable and we get the admin password:  

![image](https://github.com/user-attachments/assets/73d0d6ce-e838-4564-9015-12dea91287c5)

In the source code, I can see that the admin can execute a command, there's an attempt at a filter in the DISALLOWED_CHARS:  

![image](https://github.com/user-attachments/assets/bd48e98b-6033-4dea-980b-5e2f9c883475)

It is, as expected, insuficient to prevent command injection:  

![image](https://github.com/user-attachments/assets/376ecd78-5271-4ab7-a396-d019082347aa)

And I have the flag:  

![image](https://github.com/user-attachments/assets/ea6f1f2e-e925-43f6-bb0c-b53b2a9dcfaa)

flag{b06fbe98752ab13d0fb8414fb55940f3}
