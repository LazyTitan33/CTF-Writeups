## The Davinci Code

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/0149e9f4-5e0b-40dd-9407-053dd387be52)

## Enumeration

The first page that loads seems very basic and in fact only has one endpoint:  

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/6a1b7565-c8a0-4165-b4f6-f30b0bce2b0b)

However, accessing that endpoint shows us a Flask Debug error.  

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/8891a55f-d223-4543-a244-32ee564da678)

For a while we thought the challenge was broken, but the challenge description does mention that the website is broken, so it must be intentional. Taking a closer look at the debug error, we see it leaks that the root supports another HTTP request method other than GET.  

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/be4d7957-ae47-474a-ac91-f7a5fb1a1d0c)

PROPFIND is used to retrieve properties, stored as XML, from a web resource, usually associated with WebDav servers. This explains the sneaky DAVinci from the challenge title so we must be on the correct path. We can use this HTTP request method to enumerate the web app directory and can see another directory.

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/012826b2-1d40-4d49-a86b-224a9c317027)

In that directory, we can see the flag.txt file.  

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/331c7915-de94-4e33-b944-d358d02a4686)

The question for the longest time was how can we read the flag, because it's in a folder that isn't defined as a route in Flask so we can't access it from the webpage directly. Looking around some more, we find a backup of the app in the /static directory:  

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/96002bb5-fb19-4076-99d2-0a4db7984ccc)

We can download files from the static directory because that's what it's there for.  To serve static files to the app.

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/f3500d18-5ca4-4133-a219-34e988e105d4)

Now that we have the source code, we can play around with it locally to better understand it. After we do more research on WebDav we find that there is another HTTP method we can abuse.  

https://learn.microsoft.com/en-us/previous-versions/office/developer/exchange-server-2003/aa142926(v=exchg.65)

## Solution

We can use the MOVE method to move the flag.txt from the endpoint into the static directory:  

```bash
curl -X MOVE --header 'Destination:static/flag.txt' 'http://challenge.nahamcon.com:31144/the_secret_dav_inci_code/flag.txt'
```

Now we can access it directly and score some points:  

```bash
curl http://challenge.nahamcon.com:31144/static/flag.txt
```

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/361b5333-76e8-44e9-9580-e68839f52526)

`flag{2bc76964262b3a1bbd5bc610c6918438}`
