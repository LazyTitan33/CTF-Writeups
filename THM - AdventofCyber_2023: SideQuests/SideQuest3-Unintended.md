# Frosteau Busy with Vim

This SideQuest can be found here: https://tryhackme.com/room/busyvimfrosteau

## 1. What is the value of the first flag?

A quick port scan shows us a bunch of ports open:  
![image](https://github-production-user-asset-6210df.s3.amazonaws.com/80063008/292660426-69bf51af-09f3-4449-9346-f57f82420f5f.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAIWNJYAX4CSVEH53A%2F20231228%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20231228T091738Z&X-Amz-Expires=300&X-Amz-Signature=92d1d31a1a0a02e4c8dad14ba4f8e374b4e7af95c7c74a8d4e9c63edd95a3210&X-Amz-SignedHeaders=host&actor_id=80063008&key_id=0&repo_id=600841946)

On port 80, we see that we can't make a GET request:  
![image](https://github-production-user-asset-6210df.s3.amazonaws.com/80063008/292660440-8f5f73f1-963d-4fda-ae5d-2d69ac7c82f1.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAIWNJYAX4CSVEH53A%2F20231228%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20231228T091746Z&X-Amz-Expires=300&X-Amz-Signature=85ddad8257052850f90bfaa21a68ee461939c6c855ea82697468aa6a6014a986&X-Amz-SignedHeaders=host&actor_id=80063008&key_id=0&repo_id=600841946)

A POST request doesn't work either and we notice the server banner indicates this is a python websocket:  
![image](https://github-production-user-asset-6210df.s3.amazonaws.com/80063008/292660469-d60c943b-c4e0-4ab6-a92f-80498573f052.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAIWNJYAX4CSVEH53A%2F20231228%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20231228T091755Z&X-Amz-Expires=300&X-Amz-Signature=1b04ce75b6ced6f73787a30ecc825539133db635e5f4de01629376a5c42bdd3e&X-Amz-SignedHeaders=host&actor_id=80063008&key_id=0&repo_id=600841946)

Couldn't get much out of this, other than some errors which were pointing to a VNC service. Moving on to port 8075 we find an FTP server which has anonymous access enabled:  
![image](https://github-production-user-asset-6210df.s3.amazonaws.com/80063008/292660490-ea6ad334-1488-43e1-87bd-793a294a1ce1.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAIWNJYAX4CSVEH53A%2F20231228%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20231228T091805Z&X-Amz-Expires=300&X-Amz-Signature=7d74c45d599d14b157b9c3e25e91578447dbe83269d9eb2336c31e9763eae856&X-Amz-SignedHeaders=host&actor_id=80063008&key_id=0&repo_id=600841946)

And here we find our first flag:  
![image](https://github-production-user-asset-6210df.s3.amazonaws.com/80063008/292660496-934bbd68-8b49-4139-a1f8-7b77b6fcda01.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAIWNJYAX4CSVEH53A%2F20231228%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20231228T091823Z&X-Amz-Expires=300&X-Amz-Signature=aeb40caac1d2794268bbb5e27ed374db0771c2defc461a217d0cb436e7d7fa93&X-Amz-SignedHeaders=host&actor_id=80063008&key_id=0&repo_id=600841946)

`THM{Let.the.game.begin}`

## 2. What is the value of the second flag? + Unintended Solution to the entire challenge

Connecting to port 8085 via netcat, we see that we get directed into the Vim editor:  
![image](https://github-production-user-asset-6210df.s3.amazonaws.com/80063008/292660526-77f8f656-06ba-4813-a648-f8f15dd445c5.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAIWNJYAX4CSVEH53A%2F20231228%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20231228T091834Z&X-Amz-Expires=300&X-Amz-Signature=bfe01f862b63f1a338281bbabf8f5a475484f3cea824a7ea27e3e83af02cdde2&X-Amz-SignedHeaders=host&actor_id=80063008&key_id=0&repo_id=600841946)

From the FTP server, we know that the second flag is in an environment variable called FLAG2:  
![image](https://github-production-user-asset-6210df.s3.amazonaws.com/80063008/292660542-66b65d9b-fcc3-43cd-9596-0fc1b02e944e.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAIWNJYAX4CSVEH53A%2F20231228%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20231228T091842Z&X-Amz-Expires=300&X-Amz-Signature=f0c51b1cabd4240eb62eec16b64f50b088f87b61e330ec38290aa0d64b535e39&X-Amz-SignedHeaders=host&actor_id=80063008&key_id=0&repo_id=600841946)

In Vim, we can issue this command to get the value of a specific environment variable:  
```bash
:echo $FLAG2
```

Or, a very nice solution I found on [stackoverflow](https://stackoverflow.com/questions/11175842/how-to-obtain-the-list-of-all-environment-variables-in-vim) to list all environment variables.

```bash
:put=reduce(items(environ()), {a,e->a..e[0]..'='..e[1]..nr2char(10)}, '')
```
And we can see the flag as well as other information that could be helpful:  
![image](https://github-production-user-asset-6210df.s3.amazonaws.com/80063008/292660592-712b2f5f-d52a-4b3a-ad2c-627bd0c79cde.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAIWNJYAX4CSVEH53A%2F20231228%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20231228T091851Z&X-Amz-Expires=300&X-Amz-Signature=86df9dd5fa5a82d98d4285cb515f5d43dbf97c46350d343b8d1cfc5c0f7dae90&X-Amz-SignedHeaders=host&actor_id=80063008&key_id=0&repo_id=600841946)

`THM{Seems.like.we.are.getting.busy}`

## 3. What is the value of the third flag?

I struggled for a bit to get a stable shell into the machine. At this point I was still using netcat to connect to the port which made the Vim a bit unstable, I couldn't really use up and down arrows. But then [william-barros-costa](https://github.com/william-barros-costa) correctly pointed out that connecting to the port via telnet gives us a better connection in which I could use up and down arrows.

This allowed me to enumerate the environment a lot easier. For example, in Vim, we can use this syntax to list contents of folders using the Netrw which is Vim's builting file explorer:  

```bash
:Ex /tmp/ftp
```
![image](https://github-production-user-asset-6210df.s3.amazonaws.com/80063008/292660693-a11dd280-2e64-4d08-a407-2abd741b86cb.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAIWNJYAX4CSVEH53A%2F20231228%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20231228T091900Z&X-Amz-Expires=300&X-Amz-Signature=c20061a456940dd02e2f507e9538d231f6c8a98ff75ab9af11a380b6f5f6b8be&X-Amz-SignedHeaders=host&actor_id=80063008&key_id=0&repo_id=600841946)

I then adjusted my approach and treated this as having a form of directory listing and LFI vulnerability and as is my usual process, I wanted to see if I can read the /proc/sched_debug file in Linux to list the running processes:  
```bash
:e /proc/sched_debug
```
A very interesting process jumped out at me:  
![image](https://github-production-user-asset-6210df.s3.amazonaws.com/80063008/292660777-cc5a6216-fa71-4e05-bbba-3187f200fade.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAIWNJYAX4CSVEH53A%2F20231228%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20231228T091909Z&X-Amz-Expires=300&X-Amz-Signature=35fadd1fbcfdf0b67b261901a681e0bb110c6e6cb488f9ab68338bd804308340&X-Amz-SignedHeaders=host&actor_id=80063008&key_id=0&repo_id=600841946)

Again, using the `:Ex` command, we could list what is in this PID via /proc:  

```bash
:Ex /proc/1541
```
When I saw that the cwd points to the user home folder, I was a bit excited:  
![image](https://github-production-user-asset-6210df.s3.amazonaws.com/80063008/292660813-9db158c4-2d47-49ab-a76f-429261ebcce7.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAIWNJYAX4CSVEH53A%2F20231228%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20231228T091916Z&X-Amz-Expires=300&X-Amz-Signature=3dfdb0da3ad201245b5b17658b4416c0baee0776d5dcf48fddabc9b1681bd8b1&X-Amz-SignedHeaders=host&actor_id=80063008&key_id=0&repo_id=600841946)

That excitement escalated when I enumerated the /proc/1541/cwd and saw that in fact, we have access to the user folder outside the docker we were in. We have direct access to the host.

![image](https://github-production-user-asset-6210df.s3.amazonaws.com/80063008/292660831-cadc4651-7230-420e-8a07-8e847383b522.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAIWNJYAX4CSVEH53A%2F20231228%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20231228T091925Z&X-Amz-Expires=300&X-Amz-Signature=eb7a9b69b0b536263440f997c7f7b9c9f6b8ff8ebf6f373b0e8f929d90ce912b&X-Amz-SignedHeaders=host&actor_id=80063008&key_id=0&repo_id=600841946)

This was very surprising as this provided a way to break out of the docker without actually needing to even get a foothold into it. I wrote my SSH public key into `/proc/1541/cwd/.ssh/authorized_keys` and then SSHed as user ubuntu and to my absolute pleasure, this user has ALL the privileges:  

![image](https://github-production-user-asset-6210df.s3.amazonaws.com/80063008/292660901-edc57e33-cbda-4c23-ab2a-6841dda6a7da.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAIWNJYAX4CSVEH53A%2F20231228%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20231228T091932Z&X-Amz-Expires=300&X-Amz-Signature=c421268be30b51ac84dfc4d79084f41d75c0d0c24b969c01cde0997a0bc0c1c7&X-Amz-SignedHeaders=host&actor_id=80063008&key_id=0&repo_id=600841946)

I got root and read the 4th and 5th flag:  

![image](https://github-production-user-asset-6210df.s3.amazonaws.com/80063008/292660924-d5779cb4-6543-4414-a832-14a7e131d3b9.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAIWNJYAX4CSVEH53A%2F20231228%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20231228T091941Z&X-Amz-Expires=300&X-Amz-Signature=0a24dcbd2505085aebfe3799186b3f21d9f664a8e0c824387790821d5ef19691&X-Amz-SignedHeaders=host&actor_id=80063008&key_id=0&repo_id=600841946)

Then I went back into the /home folder on the host and recursively grepped for the flag to find the 3rd one:  
![image](https://github-production-user-asset-6210df.s3.amazonaws.com/80063008/292660949-97f01c63-d1f8-480e-bd1f-89f939fc51a6.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAIWNJYAX4CSVEH53A%2F20231228%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20231228T091950Z&X-Amz-Expires=300&X-Amz-Signature=bbc818440b276cd58e2c8443874074be250049c4876d36010d29d28ab790ec86&X-Amz-SignedHeaders=host&actor_id=80063008&key_id=0&repo_id=600841946)

`THM{Not.all.roots.and.routes.are.equal}`

As it turns out, this is possible because the docker is built with the Privileged mode enabled:  
![image](https://github-production-user-asset-6210df.s3.amazonaws.com/80063008/292661113-c0f343eb-875f-4268-add0-e97102e23954.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAIWNJYAX4CSVEH53A%2F20231228%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20231228T091959Z&X-Amz-Expires=300&X-Amz-Signature=4806660e41b1ca7b23e40ac3589c92bffac34b7e53199d855c6ca17efdee84a3&X-Amz-SignedHeaders=host&actor_id=80063008&key_id=0&repo_id=600841946)

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
![image](https://github-production-user-asset-6210df.s3.amazonaws.com/80063008/292661054-4e891b72-b981-47cb-ac00-fd9489bd7e74.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAIWNJYAX4CSVEH53A%2F20231228%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20231228T092010Z&X-Amz-Expires=300&X-Amz-Signature=b2b3f4c9b07e1be0c039777e2872908ceedc74fa7a8c389f5913128236b28c38&X-Amz-SignedHeaders=host&actor_id=80063008&key_id=0&repo_id=600841946)
