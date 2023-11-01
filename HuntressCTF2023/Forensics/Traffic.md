# Traffic

### Challenge Description
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/7e0c5469-f06c-4319-a60a-2fc6f2d8d6f6)

### Solution
After we unzip all of the files, we get down to some logs:
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/4d8da37a-1a29-470d-87f7-dac9d30dc01f)

At first I used `cat` to read each category of logs: capture*, conn*, ssl*. After that, I read the challenge description more carefully and grepped for the word `sketchy`.

```bash
strings *|grep sketchy
```
We can indeed find a sketchy website being accessed more than once:
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/d5786289-2178-4b9d-b577-8df1460d49ec)

Accessing the website ourselves, we can find the flag:
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/ca625ed4-46cf-4607-bbec-31142478ce46)

We can also run this command directly:
```bash
curl -s -L sketchysite.github.io|grep flag
```
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/1bf7b950-ec0c-46a3-b187-b55ca46d31d5)


flag{8626fe7dcd8d412a80d0b3f0e36afd4a}
