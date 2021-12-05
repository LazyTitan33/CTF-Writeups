![image](https://user-images.githubusercontent.com/80063008/144764183-dece4eea-e2b4-4369-b774-fe274eb4b806.png)


Got a persist.raw file
```bash
vol.py -f persist.raw imageinfo 
```
![image](https://user-images.githubusercontent.com/80063008/144764191-f56c19e7-8f2b-44e7-b26f-fda6968d2737.png)

Based on the challenge description, I was looking for something running at startup. I wasted a lot of time trying to manually find the startup programs, either in folders or registry keys manually.

I was not very successfull so I googled the words "windows persistence volatility" to see if there are other ways to look for these things using the many functions of the volatility tool.

![image](https://user-images.githubusercontent.com/80063008/144764194-e2d846c9-76b7-4b92-ae8e-306a730a10a5.png)

My first search result got me a video which was the key to this challenge.

https://www.youtube.com/watch?v=shF8hAprD4g

They were using a plugin for volatility called winesap. I was not able to find it in the link they mentioned but I found it on github.

https://github.com/reverseame/winesap

I copied it over to my machine in the folder of the challenge and made sure to follow their instructions to provide this argument first.

![image](https://user-images.githubusercontent.com/80063008/144764274-a34b027b-c181-4399-bb95-a5967a77a2d0.png)

I first ran it using the --match flag shown in the video but didn't get any results. So then I removed it in order to show all.

```bash
vol.py --plugins winesap/ -f persist.raw --profile Win7SP1x86_23418 winesap 
```

The first result was exactly what I was looking for. What seems to be a powershell script that has a base64 encoded payload.

![image](https://user-images.githubusercontent.com/80063008/144764279-28d617d4-c5ca-4bc7-aeb5-499f7d632e7d.png)

The flag was hiding in that payload:
![image](https://user-images.githubusercontent.com/80063008/144764343-0a2513ab-f29f-4294-b3d5-6dff64a505ba.png)


HTB{Th3s3_3lv3s_4r3_r34lly_m4l1c10us}
