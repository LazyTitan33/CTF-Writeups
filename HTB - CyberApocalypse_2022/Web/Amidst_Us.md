![image](https://user-images.githubusercontent.com/80063008/169337064-9710e9b0-af8f-4605-8e8a-3ca6ce1c3b7e.png)

We get on a dark page that seems to only have one functionality. We can upload an image when clicking somewhere in the center and it will modify it a bit.

![image](https://user-images.githubusercontent.com/80063008/169337150-b75a9828-5a31-41d7-bda0-d9b54b340b6c.png)

It seems to be using Pillow 8.4.0 according to the source code.

![image](https://user-images.githubusercontent.com/80063008/169337250-f7550c1f-32d9-472b-a1f2-365a561bcb36.png)

The code below is the one applied to the given picture.

![image](https://user-images.githubusercontent.com/80063008/169337375-a3f5feb5-8dd0-4151-a940-444f0a724a4b.png)

After some research we can find an interesting CVE that applies here. Specifically CVE-2022-22817. ImageMath.eval allows for arbitrary expressions, such as ones that use the Python exec method. From the code above, we can see that our injection point is in the Background.

![image](https://user-images.githubusercontent.com/80063008/169337604-ebba90d9-9514-4a86-8520-3de60a3c1b3c.png)

We could've used a payload to get RCE but in the interest of speed, we can just exfiltrate it using a HTTP request.

![image](https://user-images.githubusercontent.com/80063008/169337886-171cac90-aa9d-446f-bf76-a8d78ec8d014.png)

![image](https://user-images.githubusercontent.com/80063008/169337904-4fe7c745-5358-42de-a2ec-a259e6cf4400.png)

HTB{i_slept_my_way_to_rce}
