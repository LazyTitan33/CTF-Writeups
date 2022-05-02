![image](https://user-images.githubusercontent.com/80063008/166218504-93323106-89e3-4cf9-b33e-b35eed252209.png)

After we download the file, we can read it and see a potential link in it.

![image](https://user-images.githubusercontent.com/80063008/166218543-ab1fd4b6-d3f0-4ee1-beaa-570e62463799.png)

It seems to be rotated and after some experimentation, we can see that if we use caesar to rotate it 11 times, we get  proper link.

`cat theballoon|caesar 11`

![image](https://user-images.githubusercontent.com/80063008/166218614-57fe8ba7-faba-4105-a573-1f886b1a2d2f.png)

We can curl that down and see a strange string.

`curl https://pastebin.com/eLBePZEy`

![image](https://user-images.githubusercontent.com/80063008/166218694-f19da111-c9d5-4866-aa70-6ff641b68bf1.png)

It took me a while to figure out what this string is since it's not something I saw often until now. However the repeated mentions of the word 'inflate' made me experiment with Cyberchef and found that using raw inflate gets us the flag.

![image](https://user-images.githubusercontent.com/80063008/166218885-54272117-4285-4974-93e2-fad4fd4b2a02.png)
