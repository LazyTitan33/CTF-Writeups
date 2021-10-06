# Browser Preview


We are given a page that says it will preview a website we give it:

![image](https://user-images.githubusercontent.com/80063008/136173770-19b6a22f-d603-462c-b8af-c74feddf748a.png)


And indeed if we go to google.com it takes a screenshot of it.

![image](https://user-images.githubusercontent.com/80063008/136173795-c1dec5a1-4503-4375-a1bd-b1eeba21d13a.png)


However if we try to go to localhost, it says it's an invalid URL.

![image](https://user-images.githubusercontent.com/80063008/136173812-ca49db65-3182-4d81-b26c-62a1be338de2.png)


So we have to bypass that somehow. Let's look at the files we were given.

App.java, DebugServer.java, PreviewHandler.java, PreviewServer.java

The DebugServer.java mentions something interesting, a port being opened and a path, /flag.

![image](https://user-images.githubusercontent.com/80063008/136173822-6e0d33ec-82c9-417f-8fc5-1c949539a0fa.png)


The PreviewHandler.java shows that it's doing some pattern recognition so we need to give it a full URL and we need to bypass the localhost, go on port 7654 to /flag endpoint.

![image](https://user-images.githubusercontent.com/80063008/136173827-1516deb5-eb70-45fe-ac3d-2b8584fbd632.png)


On the page below we have a few suggestions we can try to bypass using DNS

https://book.hacktricks.xyz/pentesting-web/ssrf-server-side-request-forgery

The second one in the list worked for me:

![image](https://user-images.githubusercontent.com/80063008/136173847-c5260f42-b739-4094-99c5-c00e846323d2.png)


Flag: SNYK{7a1c7e791e5650a3b631ba7c78fe8319ef87ba640f739ae2887582d36bfe92c6}

