### Challenge Description
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/1e2979b0-b386-4a12-b0e5-a920c76606da)

This is the first challenge in the Web category and we get the source code.

The first page greets us with a SF looking picture and subject:
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/45466d64-111a-453e-834a-5af3be38c0ca)

We even have a login page on /login:
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/938b26f5-f015-44f5-b563-6ef7f4933348)

Going to the source code, from the `database.js` file we can see that the flag is read into the Database:
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/c62c760f-c3c5-4a5e-b596-982560158f76)

From the `entrypoint.sh` file we know it is using a NoSQL database called CouchDB:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/ca883896-2ccc-4c6a-9484-57721942afc8)

Furthermore, the login process doesn't seem to be all that safe either as it is not sanitizing or checking user input.
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/35478158-c97f-4b31-8d0b-9e77f7f71712)

In this case, we can intercept the login process using Burpsuite or your proxy of choice and modify it with a standard NoSQL injection, setting the password to `$ne` (not equal) "a" so the statement will be true and we get logged in.
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/ee336fc9-198e-4274-b95c-1cf2696a2b71)

After we do that, we will get redirected to the /dashboard page where we can see the content of the database:
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/640659e4-a9e9-4ea0-b4e4-e0253ac832bb)

That means that somewhere here, we should also see the flag. It's going to be on a random page but if you are like me and are intercepting all pages on Web challenges, then you should see it in the response and can look for HTB:
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/2c4fe7af-1d18-40b6-8cc7-5b12fe68961d)

HTB{c0rrupt3d_c0uch_b4ll0t}

