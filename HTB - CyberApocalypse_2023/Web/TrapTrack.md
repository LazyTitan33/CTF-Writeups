TrapTrack starts off with a login screen as well:

![image](https://user-images.githubusercontent.com/80063008/227711190-46c80b07-178f-4321-9886-7449019a8818.png)

Surprisingly enough, we can log into this one with admin:admin and get this screen:

![image](https://user-images.githubusercontent.com/80063008/227711221-07f853c0-9476-4e34-bb47-d968d1a552f3.png)

Let's have a look at the source code. We can already tell we'll be dealing with Redis... probably SSRF because Redis is infamous for being vulnerable to SSRF.

![image](https://user-images.githubusercontent.com/80063008/227711288-616fd62c-7e3d-4dc1-805b-2de00845da08.png)

In `application/templates/cache.py` we notice that there is also some Python unpickling being done. So we'll have to do some deserialization as well:

![image](https://user-images.githubusercontent.com/80063008/227711374-a749b463-308a-4fb8-8aa2-8fcfaa207597.png)

Using these 3 indicators, I did a quick Google search to see if there are any articles with more information and the first result was the goldmine I needed:

![image](https://user-images.githubusercontent.com/80063008/227711446-4cf84ddb-6b20-402d-b499-04b12a5650ad.png)

https://infosecwriteups.com/exploiting-redis-through-ssrf-attack-be625682461b

The article also provides a very helfpul vulnerable lab that we could play with: https://github.com/rhamaa/Web-Hacking-Lab. This labs also contains a [payload_redis.py](https://raw.githubusercontent.com/rhamaa/Web-Hacking-Lab/master/SSRF_REDIS_LAB/payload_redis.py) which will provide some payloads.

Let's try to figure out how we will be sending these payloads. Back at the source code in `application/blueprints/routes.py` we can see the option to add a track.

![image](https://user-images.githubusercontent.com/80063008/227711576-2d480754-0489-4fca-9b70-19ad83481c00.png)

However, in order to understand how the track is sent in Redis, we need to go back to the cache.py code where we see this function:

![image](https://user-images.githubusercontent.com/80063008/227711689-8527d38c-5370-4406-83e2-04ff82553df0.png)

It is basically sending `hset jobs id pickledData`. The pickled data is the one we control via the TrapURL which allows the SSRF. Before moving forward, the SSRF can be confirmed by sending a webhook in the TrapURL parameter.

![image](https://user-images.githubusercontent.com/80063008/227711801-e727f9f0-9052-4d02-85f8-7d1a0b60668b.png)

We have our callback confirming SSRF:

![image](https://user-images.githubusercontent.com/80063008/227711809-92e4a411-0746-4578-b803-d9f1a46f22d6.png)

The jobs start from 100 and increment from there one by one.

![image](https://user-images.githubusercontent.com/80063008/227711977-f57055b5-008e-470a-88f4-3463317cc6ed.png)

Loading the mainpage, also does GET requests to all the tracks so you can see at which number you are.

![image](https://user-images.githubusercontent.com/80063008/227712061-00daf84e-462b-4138-8aef-450972abdfe8.png)

Once the pickled data is sent, it is stored in the job_id and when the specific track corresponding with the job_id is listed, the payload gets loaded and triggered.

### Recap:
What we need to do to get RCE (we need RCE to read the flag using the readflag binary) is send a trapURL with an SSRF payload containing the Redis commands 'hset jobs id pickledData'. Then reload the mainpage to trigger it.

# Exploit chain:

The `payload_redis.py` file gives the option to SSRF using pickle but it sends a `set` command and using HTTP.

![image](https://user-images.githubusercontent.com/80063008/227712389-dc4ad7a9-b9f9-4447-8c80-eb978534fecc.png)

I replaced the "set" command with our needed `hset jobs` and then passing the job_id and pickled data. It was originally replacing gopher with http but http didn't work for me so I removed the replacing so it will leave the payload with gopher.

![image](https://user-images.githubusercontent.com/80063008/227712445-8d4a54e8-2f45-4feb-9448-2d56a0739938.png)

I also modified the PickleExploit class to execute what I wanted. I curled and executed a bash reverse shell on my ngrok TCP listener to get a reverse shell.

![image](https://user-images.githubusercontent.com/80063008/227712521-64389df7-e469-419b-8dd0-1002e36853ca.png)

This is a bit of an older exploit script so it needs to be run with python2 if you don't want to spend the time to replace some things to make it run with python3:

![image](https://user-images.githubusercontent.com/80063008/227712585-b05fb5de-c9fd-4c34-904c-56ce446b3353.png)

At the time I had sent a lot of different tracks so I was at 110, you have to keep count of where you are and send the appropriate job_id. I then sent a POST request adding the track with my gopher SSRF payload.

![image](https://user-images.githubusercontent.com/80063008/227712616-ca97aa3f-7286-4a85-b1bc-fe28a492827d.png)

Reload the mainpage or just do a GET request on the track you specified and I got a reverse shell:

![image](https://user-images.githubusercontent.com/80063008/227712697-2a506691-41a5-47a4-bb10-726ae6e1a134.png)

Which now allows me to run the SUID readflag binary:

![image](https://user-images.githubusercontent.com/80063008/227712707-6c0ef417-a60c-4e60-9938-5f11f8ad5d9b.png)

HTB{tr4p_qu3u3d_t0_rc3!}
