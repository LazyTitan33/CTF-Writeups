# Frosteau Busy with Vim

This SideQuest can be found here: https://tryhackme.com/room/busyvimfrosteau

## 1. What is the value of the first flag?

A quick port scan shows us a bunch of ports open:  
![image](https://github.com/LazyTitan33/myCreations/assets/80063008/69bf51af-09f3-4449-9346-f57f82420f5f)

On port 80, we see that we can't make a GET request:  
![image](https://github.com/LazyTitan33/myCreations/assets/80063008/8f5f73f1-963d-4fda-ae5d-2d69ac7c82f1)

A POST request doesn't work either and we notice the server banner indicates this is a python websocket:  
![image](https://github.com/LazyTitan33/myCreations/assets/80063008/d60c943b-c4e0-4ab6-a92f-80498573f052)

Couldn't get much out of this, other than some errors which were pointing to a VNC service. Moving on to port 8075 we find an FTP server which has anonymous access enabled:  
![image](https://github.com/LazyTitan33/myCreations/assets/80063008/ea6ad334-1488-43e1-87bd-793a294a1ce1)

And here we find our first flag:  
![image](https://github.com/LazyTitan33/myCreations/assets/80063008/934bbd68-8b49-4139-a1f8-7b77b6fcda01)

`THM{Let.the.game.begin}`

## 2. What is the value of the second flag? + Unintended Solution to the entire challenge

Connecting to port 8085 via netcat, we see that we get directed into the Vim editor:  
![image](https://github.com/LazyTitan33/myCreations/assets/80063008/77f8f656-06ba-4813-a648-f8f15dd445c5)

From the FTP server, we know that the second flag is in an environment variable called FLAG2:  
![image](https://github.com/LazyTitan33/myCreations/assets/80063008/66b65d9b-fcc3-43cd-9596-0fc1b02e944e)

In Vim, we can issue this command to get the value of a specific environment variable:  
```bash
:echo $FLAG2
```

Or, a very nice solution I found on [stackoverflow](https://stackoverflow.com/questions/11175842/how-to-obtain-the-list-of-all-environment-variables-in-vim) to list all environment variables.

```bash
:put=reduce(items(environ()), {a,e->a..e[0]..'='..e[1]..nr2char(10)}, '')
```
And we can see the flag as well as other information that could be helpful:  
![image](https://github.com/LazyTitan33/myCreations/assets/80063008/712b2f5f-d52a-4b3a-ad2c-627bd0c79cde)

`THM{Seems.like.we.are.getting.busy}`

## 3. What is the value of the third flag?

I struggled for a bit to get a stable shell into the machine. At this point I was still using netcat to connect to the port which made the Vim a bit unstable, I couldn't really use up and down arrows. But then [william-barros-costa](https://github.com/william-barros-costa) correctly pointed out that connecting to the port via telnet gives us a better connection in which I could use up and down arrows.

This allowed me to enumerate the environment a lot easier. For example, in Vim, we can use this syntax to list contents of folders using the Netrw which is Vim's builting file explorer:  

```bash
:Ex /tmp/ftp
```
![image](https://github.com/LazyTitan33/myCreations/assets/80063008/a11dd280-2e64-4d08-a407-2abd741b86cb)

I then adjusted my approach and treated this as having a form of directory listing and LFI vulnerability and as is my usual process, I wanted to see if I can read the /proc/sched_debug file in Linux to list the running processes:  
```bash
:e /proc/sched_debug
```
A very interesting process jumped out at me:  
![image](https://github.com/LazyTitan33/myCreations/assets/80063008/cc5a6216-fa71-4e05-bbba-3187f200fade)

Again, using the `:Ex` command, we could list what is in this PID via /proc:  

```bash
:Ex /proc/1541
```
When I saw that the cwd points to the user home folder, I was a bit excited:  
![image](https://github.com/LazyTitan33/myCreations/assets/80063008/9db158c4-2d47-49ab-a76f-429261ebcce7)

That excitement escalated when I enumerated the /proc/1541/cwd and saw that in fact, we have access to the user folder outside the docker we were in. We have direct access to the host.

![image](https://github.com/LazyTitan33/myCreations/assets/80063008/cadc4651-7230-420e-8a07-8e847383b522)

This was very surprising as this provided a way to break out of the docker without actually needing to even get a foothold into it. I wrote my SSH public key into `/proc/1541/cwd/.ssh/authorized_keys` and then SSHed as user ubuntu and to my absolute pleasure, this user has ALL the privileges:  

![image](https://github.com/LazyTitan33/myCreations/assets/80063008/edc57e33-cbda-4c23-ab2a-6841dda6a7da)

I got root and read the 4th and 5th flag:  

![image](https://github.com/LazyTitan33/myCreations/assets/80063008/d5779cb4-6543-4414-a832-14a7e131d3b9)

Then I went back into the /home folder on the host and recursively grepped for the flag to find the 3rd one:  
![image](https://github.com/LazyTitan33/myCreations/assets/80063008/97f01c63-d1f8-480e-bd1f-89f939fc51a6)

`THM{Not.all.roots.and.routes.are.equal}`

As it turns out, this is possible because the docker is built with the Privileged mode enabled:  
![image](https://github.com/LazyTitan33/myCreations/assets/80063008/c0f343eb-875f-4268-add0-e97102e23954)

## 4. What is the value of the fourth flag?
`THM{Frosteau.would.be.both.proud.and.disappointed}`

## 5. What is the value of the third Yetikey that has been placed in the root directory to verify the compromise?
`3-d2dc6a02db03401177f0511a6c99007e945d9cb9b96b8c6294f8c5a2c8e01f60`

# Intended Solution

The intended solution required us to find another sh file that is writable and executable. We could do this by enumerating with `:Ex` as exemplified above and edit it using `:e /usr/frosty/sh`. This is the content I wrote into it:

```bash
#!/etc/busybox sh
/etc/busybox sh
```
Now, once we start another telnet session into the Vim port, we get a shell as root (in the docker) and can read the 3rd flag from the /root directory inside the docker. We can read the 4th and 5th flag via the 1st proc:  

![image](https://github.com/LazyTitan33/myCreations/assets/80063008/4e891b72-b981-47cb-ac00-fd9489bd7e74)
