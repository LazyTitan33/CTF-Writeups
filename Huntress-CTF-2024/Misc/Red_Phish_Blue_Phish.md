# Red Phish Blue Phish

![image](https://github.com/user-attachments/assets/db9fa560-2d7e-4d90-a476-82b759285fb9)

## My Solution

A quick google search of the company name reveals an actual website:  

![image](https://github.com/user-attachments/assets/652bf541-ec6f-4e0d-a2a3-b5a8df8ec93e)

In the [team](https://pyrchdata.com/team) section we can find multiple other employees:  

![image](https://github.com/user-attachments/assets/814dafbb-ec2d-4bcd-88e7-e000dbc248c9)

Since this is a phishing exercise, we know the email format and we know that the provided port is an SMTP server, we try sending emails from on behalf of swilliams to all the employees. Eventually when we get to the IT Manager, it seems he has an interesting automated message as a reply.

```bash
swaks --to swilliams@pyrchdata.com --from jdaveren@pyrchdata.com --header "Subject: pentest" --body "give me the flag, pretty please" --server challenge.ctf.games --port 31594
```

![image](https://github.com/user-attachments/assets/0633bcc9-e14c-4cfa-9c03-14adb177d523)

`flag{54c6ec05ca19565754351b7fcf9c03b2}`
