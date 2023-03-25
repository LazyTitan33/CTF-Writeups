For the next challenge called Roten, we get another wireshark capture.

![image](https://user-images.githubusercontent.com/80063008/227503404-21382cfc-b5b4-4611-a364-b8a759e04454.png)

It has a lot of packets to look through:

![image](https://user-images.githubusercontent.com/80063008/227503476-72f900ad-8642-43fb-b0a2-51e1b5a48183.png)

There's a lot of HTTP traffic and when I see this, I generally like to look for POST requests first. That way I can see what was sent/uploaded to the server. For this we can use the `http.request.method == "POST"` filter in wireshark.

![image](https://user-images.githubusercontent.com/80063008/227503958-ef66130e-93e2-40ac-9f05-e1f188132123.png)

This makes things more manageable and we can already see something fishy. We have a post request to `/map-update.php` where, based on the mimetype, we can tell that a php file was sent.

Looking closer at that packet, we can see that indeed, what looks like a php webshell was sent however it is heavily obfuscated.

![image](https://user-images.githubusercontent.com/80063008/227504854-179fc394-bcd6-4261-98d2-0d84c4920574.png)

Oh, look at that, at the end of it all it just does an eval function to run it. 

![image](https://user-images.githubusercontent.com/80063008/227504823-d19f4653-05a8-46d4-a5ce-19cf2d615315.png)

What if we replace that with an echo and then run the php code?! This way we nerf it, it doesn't get executed, but echoed out and we should be able to see it deobfuscated.

![image](https://user-images.githubusercontent.com/80063008/227504398-c26f0b66-b358-4c71-857a-94637bf7c629.png)

Sure enough, carefully reading the deobfuscated code, we can see the flag in a comment:

![image](https://user-images.githubusercontent.com/80063008/227504990-147a29b2-6639-46c9-aef7-70bc0e6ffec0.png)

HTB{W0w_ROt_A_DaY}