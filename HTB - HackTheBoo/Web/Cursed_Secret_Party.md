The main page asks us to RSVP to a sweet Halloween party.

![image](https://user-images.githubusercontent.com/80063008/198255329-26b36f59-138b-4cb0-9569-33a9f2601a35.png)

We RSVP because it sounds fun and we intercept the POST request.

![image](https://user-images.githubusercontent.com/80063008/198255372-492a9be9-3617-4afa-8d3f-2dacf325ee42.png)

The response says our request will be reviewed. This smells like XSS. Looking through the provided source code, we see a `bot.js` file which reads the flag.txt file.

![image](https://user-images.githubusercontent.com/80063008/198255413-bbfaf347-1771-4fe5-a651-0416994ca12c.png)

The visit function opens a browser page and sets a JWT token as a cookie. The flag is passed in said token. So we obviously need to steal the bot's cookie to get the flag.

![image](https://user-images.githubusercontent.com/80063008/198255491-5bcdf9db-574e-4366-ad4a-61ddc87725e1.png)

After the bot sets the cookie, it visits the `/admin` endpoint, waits 5 seconds, then deletes all the content.

![image](https://user-images.githubusercontent.com/80063008/198255531-87199e44-019d-46b2-8db2-f70814ed67ad.png)

In the index.js file we notice that we have some definitions set for the CSP.

![image](https://user-images.githubusercontent.com/80063008/198255575-9466b691-1dd0-425c-8657-575e07511a4f.png)

We noticed this earlier in our Response as well:

![image](https://user-images.githubusercontent.com/80063008/198255610-896a77ba-52ca-4d5b-8e3f-739ca6fab33c.png)

In the `JWTHelper.js` file we see how the JWT token is signed. It uses HS256 with a big random hex string so it is not crackable. We can't fake our JWT token nor will it help us if we did. Remember that the flag is passed in the JWT token when the bot gets activated.

![image](https://user-images.githubusercontent.com/80063008/198255697-fe5ee93b-c4d6-458d-a915-0142d6a90407.png)

That being said, it would help us to change how this APP_SECRET is created in order for us to experiment locally and turn what would normally be a Blind XSS into a normal XSS. Let's change the APP_SECRET to a static value:

![image](https://user-images.githubusercontent.com/80063008/198255718-9bd43889-26c2-4d0c-b950-15ca90728158.png)

We also need to comment out the `bot.visit()` from the `routes/index.js` file. This is to prevent the bot from accessing and deleting the local payloads. We want to do that manually.

![image](https://user-images.githubusercontent.com/80063008/198255778-d167cee3-8dea-4a23-a4a4-5e7c50ddd881.png)

We relaunch our docker with the new modifications. We launch ngrok and set up a netcat listener then pass a simple XSS payload to have the bot access our ngrok page in all the fields to see what happens.

`<img src=http://80ee-188-24-132-65.ngrok.io>`

Now we need to access `/admin` but we can't do that without a session cookie. Based on the source code, we know what keys and values we need so we can pass those to www.jwt.io

![image](https://user-images.githubusercontent.com/80063008/198255859-eaabf8d6-eda8-4c63-aee7-f26ef72cccca.png)

In our browser, we create a cookie called session and paste the JWT token.

![image](https://user-images.githubusercontent.com/80063008/198256017-d4a5f6ba-0949-4f5f-8ae9-d9212a59de97.png)

Now when we access `/admin`, we notice that only the `halloween_name` key was interpreted and not the rest. So that is our injection point.

![image](https://user-images.githubusercontent.com/80063008/198256089-3d21ddaf-ddda-4897-ae5c-658e3708f634.png)

If we look in the browser console though, we notice CSP is blocking us and we don't get a hit in ngrok.

![image](https://user-images.githubusercontent.com/80063008/198256120-f0402e2f-8c4d-493f-8113-89996ecc87f5.png)

So this is where I started googling. The CSP is set pretty strictly, we don't have any unsafe-eval or unsafe-inline, no wildcards. I experimented with a lot of different payloads but I'll save you the time and follow the direct path.

Scripts are only allowed from self and from `cdn.jsdelivr.net`. We can't pass any js from self but let's look into the cdn. Time for some Googling.

![image](https://user-images.githubusercontent.com/80063008/198256213-44ef19e2-a101-45fa-a1a7-eafc90cb2c4c.png)

The second link turned out to be very helpful.  
https://dev.to/pirateducky/csp-porfavor-aji 

It shows various ways to bypass CSP, a particular one was very interesting to me and I learned something new this day.

![image](https://user-images.githubusercontent.com/80063008/198256266-664a3583-3862-48b0-95d6-b9b200a9fd18.png)

It would seem that we can simply pass our own js script from our github into jsdelivr. Such a handy feature.

![image](https://user-images.githubusercontent.com/80063008/198256307-969478ba-6b09-4230-9c8e-9ba333932977.png)

It will then create a link for us that will come from the domain that is part of the target CSP so it should allow us to execute javascript.

https://www.jsdelivr.com/github

![image](https://user-images.githubusercontent.com/80063008/198256362-12df7012-0977-4209-8909-6d38d60a86b3.png)

I created a simple XSS cookie stealer in my github page, pasted the link into jsdelivr.net and I received a link.

![image](https://user-images.githubusercontent.com/80063008/198256408-633ff226-3210-4bf6-9f98-a0af0882a12d.png)

We send a simple script src XSS payload in the halloween_name.

![image](https://user-images.githubusercontent.com/80063008/198256443-cc87682d-4bd4-4347-9b86-204b7cd91d17.png)

Remember we have ngrok and netcat listening so when the bot accesses the page, the script src will trigger and it will load our javascript file which triggers the XSS cookie stealer and netcat grabs it.

![image](https://user-images.githubusercontent.com/80063008/198256481-98fcd5ab-d3e3-4832-98a9-a228ba30c3dd.png)

Now that we have the JWT token, we can decode it in jwt.io or base64 decode it in the linux terminal and we get our flag.

![image](https://user-images.githubusercontent.com/80063008/198256536-94226bd6-7442-496e-b27c-933776946b5a.png)

HTB{cdn_c4n_byp4ss_c5p!!}
