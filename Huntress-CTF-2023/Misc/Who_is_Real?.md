# Who is Real?

### Challenge Description
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/8e44f69e-1228-4208-ad28-a7008dc78d41)

### Solution
When we access the website we see two faces and we have to decide which one is real:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/abbba3e8-a944-487d-b841-497294da585c)

If we intercept the request with Burpsuite though, we can see it's setting up a Flask cookie.  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/4b5da9b5-1d43-4c3b-b33d-5b061402e0ba)

Using `flask-unsign` which you can install with `pip install flask-unsign` we can see that it reveals the correct answer:  

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/3fad70cc-6f41-4e3b-a2c1-9ee1a934263f)

We just need to hover our mouse over the images and see which one has the specified GUID and then click on it. We can repeat this until we get the streak that we need:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/45adeaf3-df91-438b-9622-76cacc3fc3a3)

Once we hit the streak of 5/5 we get our flag:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/45841514-5c2f-44e5-a275-75e9109e8634)

This was a nice and easy challenge. What would've made it better would've been a longer streak to encourage scripting these steps.

flag{10c0e4ed5fcc3259a1b0229264961590} 

