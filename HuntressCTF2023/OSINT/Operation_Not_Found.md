# Operation Not Found

### Challenge Description
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/0602316f-bcf3-4d63-9d73-655d0cb9a1df)

### Solution
Accessing the provided link, we can see a building and the name of a company:
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/7fc69a62-5409-44c0-a749-b89e945da88a)

After wasting a lot of time looking around for different office buildings where this company would be, I decided to take a cropped screenshot of the building all zoomed out. I uploaded it into the russian site https://yandex.com:
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/df70504c-b2cb-4eca-9d23-bae767e319b0)


The very first result shows a very similar building and indicates this is the Georgia Tech Library:   
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/948d27e6-277a-48ef-a759-5872a7e84c25)

But that's quite a big place. Taking a closer look at the picture that Yandex found, we can see the building sign is still on it. In our picture it was taken down. It says it's the `Crosland Tower` which helps narrow it down even further.

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/db5e45ba-6291-4da3-bed4-72441e79a086)

We find that in the challenge map and get our flag:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/8b10803a-dacb-40e0-8305-1d95ed15127f)


flag{c46b7183c9810ec4ddb31b2fdc6a914c}
