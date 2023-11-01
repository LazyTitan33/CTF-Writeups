# Online Chatroom

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/250d063c-9781-4609-a39d-ab83e43d2a1f)

For this challenge, we get the source code of a Go binary. We notice some chat messages going on and the flag is within the chat history of user 5.

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/211730c1-8070-4b84-9fd9-6cc1ace0c115)

Sending a simple message in the web application:

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/fb992564-1a32-4de9-8c18-b2dfe236ac10)

And intercepting it with Burpsuite, we notice it is using websockets:

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/58b00757-2dfd-4ed4-87e8-8f6b96b9632c)

In the source code, we notice another command other than `!write`. We notice we can query the chat history using `!history`. After sending the request to Repeater, we see we need to provide an index from 1 to 7.

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/c85a6b86-7c69-4915-bee7-c71f62b77653)

Well, what happens if we query outside of that range?

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/d2255c17-256e-4bc3-80a7-12229e5cb36e)

We get the flag: flag{c398112ed498fa2cacc41433a3e3190b}
