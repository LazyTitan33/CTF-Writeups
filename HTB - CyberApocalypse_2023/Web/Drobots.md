We have a login screen:

![image](https://user-images.githubusercontent.com/80063008/227565559-a92252df-97d9-48dd-8c3f-f58b3658a5e0.png)

The first thing we try on a login screen is SQL injection. I tried `' or 1=1-- -` but that didn't work, so let's try double quotes instead of single quotes: `" or 1=1-- -`

![image](https://user-images.githubusercontent.com/80063008/227565836-c9078718-9819-4987-a1cb-46eb644b2981.png)

HTB{p4r4m3t3r1z4t10n_1s_1mp0rt4nt!!!}