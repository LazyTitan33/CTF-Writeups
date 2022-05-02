![image](https://user-images.githubusercontent.com/80063008/166220640-885ce522-4863-42be-b548-be492481e0ef.png)

The home page looks like this. When I see XML, I immediately think XXE.

![image](https://user-images.githubusercontent.com/80063008/166220669-54f5bd9f-6d23-472b-91d8-3b9bbba1b2ab.png)

On the /trial endpoint we can upload a file.

![image](https://user-images.githubusercontent.com/80063008/166220746-b6a9b679-4bb5-43b9-acc3-d03d02408a44.png)

And on the /view endpoint we can view the file we uploaded.

![image](https://user-images.githubusercontent.com/80063008/166220792-6c40e49a-50c3-47b4-8f1f-eeae545a3438.png)

To make experimentation easier, I intercepted requests using Burpsuite.

I first uploaded a standard XXE payload to read a file.

![image](https://user-images.githubusercontent.com/80063008/166220858-55272441-120c-45d0-9418-9769ed09cf13.png)

The request to view the file was successful and we have the passwd file. As the description states, the flag is in /var/www so we change our payload to read that file.

![image](https://user-images.githubusercontent.com/80063008/166220991-a8abd195-24e5-446f-883d-5cacb8d3bf8e.png)

And we get the flag.

![image](https://user-images.githubusercontent.com/80063008/166221008-e3945ae4-1037-4c3f-8e4b-cee91e369843.png)
