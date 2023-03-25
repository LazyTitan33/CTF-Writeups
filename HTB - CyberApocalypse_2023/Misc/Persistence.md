For this particular challenge, the description was very helpful:

<i>"Thousands of years ago, sending a GET request to /flag would grant immense power and wisdom. Now it's broken and usually returns random data, but keep trying, and you might get lucky... Legends say it works once every 1000 tries."</i>

Just doing a curl request on the `/flag` endpoint of the provided IP and port, we get garbage:

![image](https://user-images.githubusercontent.com/80063008/227533457-d5150e3d-0144-4e98-a4b8-0ace111bd81c.png)

However, the description says it works once on every 1000 tries, so let's do 1000 tries and see if we get the flag:

```bash
for i in {1..1000};do curl -s http://167.172.50.208:31200/flag|grep HTB;done
```

I added the `-s` flag for curl to be silent. After a short bit, we get the flag:

![image](https://user-images.githubusercontent.com/80063008/227535247-987f73a6-9e85-46de-ab70-d7d3f9c64ce6.png)

HTB{y0u_h4v3_p0w3rfuL_sCr1pt1ng_ab1lit13S!}