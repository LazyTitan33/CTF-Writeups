# something-happened

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/1afedf86-2ae9-43f6-af5c-d8b4d28b6a69)

# Solution

This challenge generates a Kibana instance for us where we can sift through some logs. We can start to discover by clicking on the menu button in the top left and then `Discover`:  

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/93280116-41d7-4293-8d9e-b2d80dc5f9e6)

Now, from the right side, we change the time filter to go as far back as we can:  

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/1a47d584-de65-46bc-ac6d-7c691496c055)

We need to change the index pattern to the one we are interested in and luckily this one bears the name of the challenge so it is easy to identify:

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/fb36bd71-0a28-4854-afc1-9f1e1786908b)

We can now see the logs including over 80.000 hits:

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/3506ac2c-4c95-41f7-9c22-5109443191e6)

Looking through the filters on the left side, we can soon see something that catches our eye in the `user_agent`:  

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/9caa2e8d-6039-48ee-a65e-024c406aae29)

A `log4j` payload on destination_ip: `198.71.247.91` so we have our answers to the first 2 questions. 

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/7ff2eb94-53df-40f2-9bc0-7d4fbae8ba66)

The answer to the last question was horrible. I've lost a lot of my time and accuracy percentage here. It was a really bad choice from the creator to make the answer a lowercase word: `mozilla`.

This made the challenge a huge time waster and very unsatisfying to complete. Again, we had to guess the last answer because it's not logical to actually enter "mozilla". What is more logical is to apply common sense, and put in the log4j payload that we can actually see in the `user_agent` field, or at the very least, the full Mozilla user agent that is found most often after filtering based on the victim IP:  

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/4f21c54c-3eff-4394-84b2-335a3e97f3a7)

In any forensics/DFIR investigation, a report will be made with complete and detailed information. Questions will be asked in full. If these CTF challenges are supposed to emulate that, then it is unacceptable to abbreviate something that neededn't be abbreviated.

Also, the way the question was formulated didn't help either. All in all, a bad challenge in my book. On the bright side, it does give an opportunity to learn to parse Elastic/Kibana logs if you haven't before.
