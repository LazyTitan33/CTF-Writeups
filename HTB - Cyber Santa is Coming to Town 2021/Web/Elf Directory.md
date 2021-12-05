![image](https://user-images.githubusercontent.com/80063008/144763321-f4299aa3-a2d5-4bd2-84b4-e69c97190465.png)

Homepage greets us with a login screen.

![image](https://user-images.githubusercontent.com/80063008/144763330-7e94df29-c0ff-47cd-97d0-07917152eed1.png)

We can create an account and then login in.

![image](https://user-images.githubusercontent.com/80063008/144763338-2022210f-69be-4162-9a5a-5ca53f8a3f15.png)

It says we don't have permissions to edit our profile but if we look at the cookie, we can see it's simply base64 encoded so we can decode it, edit it and base64 encode it.

We now have an Admin approved cookie

eyJ1c2VybmFtZSI6ImFkbWluIiwiYXBwcm92ZWQiOnRydWV9

![image](https://user-images.githubusercontent.com/80063008/144763371-547b1aa7-0565-4725-ad39-783d6e1cf2b4.png)

With some experimentation, we notice we also have Reflected XSS with the username field.

![image](https://user-images.githubusercontent.com/80063008/144763572-2a1f3a93-36f9-4920-b5be-a874e80e18a9.png)

XSS cookie

eyJ1c2VybmFtZSI6IjxzY3JpcHQ+YWxlcnQoZG9jdW1lbnQuZG9tYWluKTwvc2NyaXB0PiIsImFwcHJvdmVkIjp0cnVlfQ==

However this is a rabbit hole because XSS can't get us a foothold as stated in the challenge description.

The profile picture didn't change when I changed the cookie with Admin and True. So I went back to leaving it on my username but approved set to true.

![image](https://user-images.githubusercontent.com/80063008/144763416-36578163-9bc0-4663-bd54-94010c0d2b32.png)

eyJ1c2VybmFtZSI6ImxhenkiLCJhcHByb3ZlZCI6dHJ1ZX0=

This now allows for the profile picture to change. However we can still only upload PNG files. We need to bypass that.

Added a double extension, and the PNG header along with some content from a png file. Then added a php shell. I listed files in root and saw the flag so I read it using cat.

![image](https://user-images.githubusercontent.com/80063008/144763419-b4c24e73-fdef-4b6b-b2c2-22a39c2bf228.png)
![image](https://user-images.githubusercontent.com/80063008/144763421-c410e4be-af5b-4b2d-aa70-6a5e6d7075d6.png)



HTB{br4k3_au7hs_g3t_5h3lls}

With the payload below, I could also get a shell on the box even if one isn't really required once you have command execution.

![image](https://user-images.githubusercontent.com/80063008/144763429-d2a951d6-6085-47d4-a3c0-19023d95f4b2.png)
![image](https://user-images.githubusercontent.com/80063008/144763432-82d217b7-98ed-4be0-ae6f-46d38049b8f6.png)
