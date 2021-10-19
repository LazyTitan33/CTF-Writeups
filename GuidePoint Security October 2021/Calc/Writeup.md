This one took me longer than I care to admit. I kept overthinking and overcomplicating things.

We just get a page to visit:

![image](https://user-images.githubusercontent.com/80063008/137874431-bf115ab7-b688-4266-bc7a-58fcf2eb8d2a.png)

We can see it is allowing us to enter letters and numbers and it is doing some math.

![image](https://user-images.githubusercontent.com/80063008/137874512-ba7f4715-4169-4e2c-834c-17d72b8f0244.png)
![image](https://user-images.githubusercontent.com/80063008/137874533-d5f93df7-781d-4883-8827-e098cc309d3a.png)

Checking with various symbols in the values to try and break the syntax, we see that inserting a `;` breaks the syntax. So if we break the syntax, put in our command, then put the `;` back to repair the syntax, we get command injection.

`;id;`

![image](https://user-images.githubusercontent.com/80063008/137874578-5ba4f228-19ca-4c48-8fb9-312e2d08a49d.png)

`;ls;`

![image](https://user-images.githubusercontent.com/80063008/137874598-0ea22606-1ba5-4f5e-a374-452678a540ba.png)

`;cat+calchdeyenbdw7wjh281y1hd771ujs718hq.txt;`

Or just because it's in the root folder of the web application, just go directly on the page

![image](https://user-images.githubusercontent.com/80063008/137874633-eb421f91-1f21-4f9e-8373-addd67de82f7.png)

GPSCTF{89dcce9621fb7181cab196b592116c1a}
