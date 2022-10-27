In this challenge we see a website with some cards that we can click on.

![image](https://user-images.githubusercontent.com/80063008/198007212-69ecbdd8-7bb0-4135-ac13-dde897e7d58a.png)

In the source code provided, we notice that there is an exec() function which executes code. It is taking the integers of the current_health and attack_power however the `operator` is taken directly from the user input.

![image](https://user-images.githubusercontent.com/80063008/198007296-86cecbc7-14db-4439-88c2-c55332bb012c.png)

This is how a normal POST request looks like when we click on a card.

![image](https://user-images.githubusercontent.com/80063008/198008086-8a6e51ac-9a17-4738-930e-3e53754acd34.png)

Since there is no input sanitation, we can inject python code into the `operator` key and get a reverse shell:

![image](https://user-images.githubusercontent.com/80063008/198008340-0da1a18c-172f-4a11-9dc8-2961f509d0b5.png)

![image](https://user-images.githubusercontent.com/80063008/198008388-7242063d-ac5d-4685-b2c8-dca6be0f7143.png)

Alternatively, we can simply read the flag directly in the Response with the payload below:

```;f = open('/flag.txt', 'r'); result = f.read();```

HTB{c0d3_1nj3ct10ns_4r3_Gr3at!!}