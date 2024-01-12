# Frosteau Busy with Vim

This SideQuest can be found here: https://tryhackme.com/room/busyvimfrosteau

## 1. What is the value of the first flag?

A quick port scan shows us a bunch of ports open:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/0ab43371-9395-4657-b571-4c6ca88677d8)

On port 80, we see that we can't make a GET request:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/98b523c8-c9b8-4e95-baf4-5748f0c7a5ad)

A POST request doesn't work either and we notice the server banner indicates this is a python websocket:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/fc1e60cd-e47c-4adc-855f-ca97136a4e40)

Couldn't get much out of this, other than some errors which were pointing to a VNC service. Moving on to port 8075 we find an FTP server which has anonymous access enabled:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/7e958c8c-d819-4dc1-8777-2f732cbba62b)

And here we find our first flag:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/57c00872-7f4c-4029-8cd6-afb8f0439cf4)

`THM{Let.the.game.begin}`

## 2. What is the value of the second flag? + Unintended Solution to the entire challenge

Connecting to port 8085 via netcat, we see that we get directed into the Vim editor:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/4fe2b222-1103-449c-9478-51bcb52ff078)

From the FTP server, we know that the second flag is in an environment variable called FLAG2:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/fa521fb4-b171-449e-804f-da1d6e93a736)

In Vim, we can issue this command to get the value of a specific environment variable:  
```bash
:echo $FLAG2
```

Or, a very nice solution I found on [stackoverflow](https://stackoverflow.com/questions/11175842/how-to-obtain-the-list-of-all-environment-variables-in-vim) to list all environment variables.

```bash
:put=reduce(items(environ()), {a,e->a..e[0]..'='..e[1]..nr2char(10)}, '')
```
And we can see the flag as well as other information that could be helpful:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/25348542-40b6-412e-ae0b-b37f5368efb0)

`THM{Seems.like.we.are.getting.busy}`

## 3. What is the value of the third flag?

I struggled for a bit to get a stable shell into the machine. At this point I was still using netcat to connect to the port which made the Vim a bit unstable, I couldn't really use up and down arrows. But then [william-barros-costa](https://github.com/william-barros-costa) correctly pointed out that connecting to the port via telnet gives us a better connection in which I could use up and down arrows.

This allowed me to enumerate the environment a lot easier. For example, in Vim, we can use this syntax to list contents of folders using the Netrw which is Vim's builting file explorer:  

```bash
:Ex /tmp/ftp
```
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/12cd3b35-bb19-4f9f-84f0-6fc1c2dfd493)

I then adjusted my approach and treated this as having a form of directory listing and LFI vulnerability and as is my usual process, I wanted to see if I can read the /proc/sched_debug file in Linux to list the running processes:  
```bash
:e /proc/sched_debug
```
A very interesting process jumped out at me:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/9f0ae56a-8a83-4c58-9015-1acef0bea45e)

Again, using the `:Ex` command, we could list what is in this PID via /proc:  

```bash
:Ex /proc/1541
```
When I saw that the cwd points to the user home folder, I was a bit excited:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/b12dc09c-7a34-4a45-9398-e95a859fba56)

That excitement escalated when I enumerated the /proc/1541/cwd and saw that in fact, we have access to the user folder outside the docker we were in. We have direct access to the host.

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/b4a18bd3-3c3d-4d49-aa31-63e7935c0c1b)

This was very surprising as this provided a way to break out of the docker without actually needing to even get a foothold into it. I wrote my SSH public key into `/proc/1541/cwd/.ssh/authorized_keys` and then SSHed as user ubuntu and to my absolute pleasure, this user has ALL the privileges:  

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/42eb39de-9131-495c-8ce0-f95405fc9be9)

I got root and read the 4th and 5th flag:  

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/a4bc7a60-d039-4c25-a042-15d52ee8a3a8)

Then I went back into the /home folder on the host and recursively grepped for the flag to find the 3rd one:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/1ad59f90-edff-4b92-8894-6b38a2c2731d)

`THM{Not.all.roots.and.routes.are.equal}`

As it turns out, this is possible because the docker is built with the Privileged mode enabled:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/9bbeb475-db47-40d5-bcfa-6e9b210e4aa3)

## 4. What is the value of the fourth flag?
`THM{Frosteau.would.be.both.proud.and.disappointed}`

## 5. What is the value of the third Yetikey that has been placed in the root directory to verify the compromise?
`3-d2dc6a02db03401177f0511a6c99007e945d9cb9b96b8c6294f8c5a2c8e01f60`

# Intended Solution

The intended solution required us to find another sh file that is writable and executable. We could do this by enumerating with `:Ex` as exemplified above and edit it using `:e /usr/frosty/sh`. This is the content I wrote into it. /etc/busybox was already on the machine:

```bash
#!/etc/busybox sh
/etc/busybox sh
```
Now, once we start another telnet session into the Vim port, we get a shell as root (in the docker) and can read the 3rd flag from the /root directory inside the docker. We can read the 4th and 5th flag via the 1st proc:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/992050a8-4fe0-42d0-888c-23bd29f1ad74)
