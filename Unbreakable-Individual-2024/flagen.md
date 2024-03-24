# flagen

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/b15326af-4818-44bc-8b7b-f4eed86694ef)

# Solution

For this challenge, we can use the online emulator [appetize.io](https://appetize.io/) to do some dynamic analysis. I've made an account using a temp email and can now turn on Network Logs:

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/94ae69e6-5939-466f-bbb5-19165d30fec1)

After adding the generated IP and Port, I hit connect:  

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/3756a4c1-831b-4c1b-abd0-caa2937bc3f3)

Then I make a GET request and can see it in the network logs:  

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/34a49f26-a99c-4f06-9294-f5739da33184)

To make it easier for myself to enumerate this, I've replicated it in Burp Suite, making sure to add the endpoint and the `X-API-KEY` header which seems to be used for authentication:  

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/6ee08424-61d9-4965-966d-f9a1a333b2d8)

Considering this is an API, I've decided to fuzz it with an appropriate wordlist:  

```bash
ffuf -c -t 100 -u http://34.107.126.69:31241/FUZZ -w /usr/share/seclists/Discovery/Web-Content/api/api-endpoints.txt
```

And I quickly found that the swagger documentation is exposed on the `/swagger` endpoint:  

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/846feb0c-c158-409d-a2b7-f2745a7f74bd)

After we access the swagger documentation we find that there is a second endpoint on `/api/v1/getfl`:  

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/a2c3f7df-49ad-4d95-82d1-3d75c270e940)

We access that endpoint with the `X-API-KEY` header and we get our flag:  

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/d014a6ec-3722-4d3d-9823-7ef5dea9987d)

`CTF{21fb574397e3c49950511c5f1a9dd413ffc5986a0a15b36878434e21782877f0}`
