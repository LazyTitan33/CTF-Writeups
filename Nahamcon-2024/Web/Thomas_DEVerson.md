## Thomas DEVerson
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/902fd379-56ba-4402-b5ba-a2e61b902b51)

## Enumeration

At first glance we just get a website with very few options:  

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/43e06237-ceee-413d-bae6-3dbc59a484d9)

Typing anything in the Username box get's us this message:  

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/12182f63-0957-48a3-b781-d8c5ec75be10)

On the /status endpoint we get an incredible uptime for the webserver:  

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/1ae35a01-44f3-4781-aa37-2d11c6a66493)

The source code seems to be hiding another endpoint:  

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/38d57413-5f72-4b76-b228-f30821769408)

If we access it, we get only the first 10 lines of the source code. But it is enough to show us a few valid users and the Flask application secret key used to sign the session cookie:  

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/1bbb67a3-eef6-4cfe-9817-6b8f88733072)

If we try to log in using one of the valid users, we still can't log in because they are protected:  

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/165c238c-55d5-47c4-b71d-656baa129dc6)

When trying to log in, we also get a session cookie assigned that looks like this:  

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/77ba3d51-6758-4484-9211-b3339c19f6db)

So let's try to forge a cookie ourselves. As per the source code, part of the secret key is the epoch time from when the server started, which we know based on the /status endpoint. After a while, I learned the hard way that we also need to keep in mind the timezone. 

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/81e3d24b-e403-4b48-907a-383d1788615d)

## Solution

After we access the /status endpoint one more time, we fill out this script to do some quick math:  

```python
from datetime import datetime, timedelta, timezone

# Current time in GMT
c = datetime.now(timezone.utc)

uptime = timedelta(days=82817, hours=2, minutes=29)
uptime_datetime = c - uptime

f = uptime_datetime.strftime("%Y%m%d%H%M")

print(f)
```

With the correct epoch time, we can use flask-unsign to sign our cookie:  

```bash
flask-unsign -s --secret 'THE_REYNOLDS_PAMPHLET-179708250845' -c '{"name":"Jefferson"}'
```

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/6347703d-7b8e-49a9-8114-b5d706197ab2)

With it set in our browser, we access login and get the flag:  

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/e58a8b5f-1435-4e24-b11c-82e324ce8398)

`flag{f69f2c087b291b9da9c9fe9219ee130f}`
