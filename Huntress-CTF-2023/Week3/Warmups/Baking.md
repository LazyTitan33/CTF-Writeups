# Baking

### Challenge Description
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/5d1039ad-af74-4ccb-9e47-859df2b6fdf8)

### Solution
Accessing the web page we see we can bake some cookies. The Magic Cookies however seem to take 7200 minutes which is forever... not someting we have time for:  

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/1c7ec7a6-4b24-4e5a-b213-40ad5c486f5a)

We also see that a cookie is set when baking the cookie:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/8a50dc79-5d4c-4cac-98be-a57543e87a2f)

```bash
echo 'eyJyZWNpcGUiOiAiTWFnaWMgQ29va2llcyIsICJ0aW1lIjogIjEwLzE0LzIwMjMsIDE1OjUzOjUwIn0='|base64 -d
```
Decoding this cookie, we can see it's a JSON object which includes the time for when the cookie would be done.  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/c212758e-5049-475f-bff9-3151b590ad46)

```bash
echo -n '{"recipe": "Magic Cookies", "time": "10/14/2022, 15:53:50"}'|base64 -w0
```

We changed the year to put it in the past:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/fe203bbd-b62b-4020-9285-c5b964aa8b75)

Now that we have a new cookie, we replace it in the browser and refresh to get the flag:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/b2ae3a8b-0910-483d-b5a2-3aca77b211a6)

flag{c36fb6ebdbc2c44e6198bf4154d94ed4} 
