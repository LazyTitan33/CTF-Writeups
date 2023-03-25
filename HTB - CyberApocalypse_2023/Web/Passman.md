We have a login screen:

![image](https://user-images.githubusercontent.com/80063008/227706284-355a1656-be3b-4962-8547-7b5adfe65b56.png)

We create an account and log in.

![image](https://user-images.githubusercontent.com/80063008/227706323-7aca3f7b-7371-4c78-8535-10ab5b71eeb0.png)

From the source code provided we can see that the admin has the flag as a note in his account. So we have to somehow escalate our privileges inside the app.

![image](https://user-images.githubusercontent.com/80063008/227706435-09977f9d-1052-4cab-919c-d64cd632a662.png)

From the `database.js` source code we can also see that SQL injection is not an option as there are protections in place:

![image](https://user-images.githubusercontent.com/80063008/227706483-312c6f9f-3d64-448f-9d9b-fd1671bf774f.png)

The `routes.js` does reveal to us that we are dealing with `GraphQL`:

![image](https://user-images.githubusercontent.com/80063008/227706522-9c626f50-af21-4e71-afad-1e833e3b450a.png)

In the `GraphqlHelper.js` source code we see the GraphQL schema, including the Mutations. 

![image](https://user-images.githubusercontent.com/80063008/227706644-35bfe59a-1767-4f30-bd5a-c51f47ff16b0.png)

The first one is the register mutation which we can also see in BurpSuite from when we registered our account.

![image](https://user-images.githubusercontent.com/80063008/227706694-5da55de6-4d8c-48c9-9365-dbe76b4ecde8.png)

However, scrolling down in this code, we notice another very interesting mutation, an `UpdatePassword` mutation which requires the username and password as arguments:

![image](https://user-images.githubusercontent.com/80063008/227706825-5be2afa8-98a6-410f-b03a-3ba285143065.png)

It's actually the same as the `LoginUser` mutation which was sent when we logged in:

![image](https://user-images.githubusercontent.com/80063008/227706932-ec801308-3e31-4dfa-adaf-e1c6fba7f9b7.png)

Let's send the Login POST request to our Repeater tab and replace LoginUser with UpdatePassword. Also change the username to admin and set whatever password we want. Make sure to also add the cookie that was assigned after you logged in.

![image](https://user-images.githubusercontent.com/80063008/227706995-235c41c4-b9d5-4c05-86ef-a35645f21e04.png)

The response confirmed that we've updated the admin password. We log in and get the flag, a nice example of IDOR vulnerability:

![image](https://user-images.githubusercontent.com/80063008/227707013-7264a57a-167e-492b-9919-17637e20f220.png)

HTB{1d0r5_4r3_s1mpl3_4nd_1mp4ctful!!}


