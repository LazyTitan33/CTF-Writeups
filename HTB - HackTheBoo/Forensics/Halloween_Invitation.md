This took me a bit of time but only because I chose to do it manually. I was too lazy to try to change the code to get it to run just right to spit out the flag.

Let's start by opening the file in a VM that's segreggated from our host. We go to View - View Macros:

![image](https://user-images.githubusercontent.com/80063008/198263734-89303b48-df12-445d-9db8-018d8d022bce.png)

Reading through the macro code, we can figure out that the `secret` is what we are interested in. It is broken up in pieces and hexed. I selected a piece at the end just to try to unhex it and see what it says. Also, usually flags are at the end or in the middle in these kinds of payloads.

![image](https://user-images.githubusercontent.com/80063008/198263958-3eb005f8-059f-4861-a239-db6c69547736.png)

After we unhex it, we notice that CyberChef no longer detects what the next encoding is, but we can tell it is Decimal. A keen eye would observe though that one of the digits is "stuck together". That should be a `65 72` and `65 99`, there is no ASCII value in Decimal for 6572 or 6599. 

![image](https://user-images.githubusercontent.com/80063008/198264519-f6926c64-66bf-44bb-9451-4ab41ee66543.png)

We copy that and put it up top and change the values accordingly. Then we need to convert from Decimal and Base64 decode it.

![image](https://user-images.githubusercontent.com/80063008/198264899-7dd90301-dbb8-4085-a025-025d3f6878ad.png)

We seem to have gotten nothing, but remember that we only copied a part of the hex so we must have invalid output because the input is invalid. Let's start deleting some Decimal values from the beginning. As we slowly start deleting, we can see the output changing until we eventually get this.

![image](https://user-images.githubusercontent.com/80063008/198265105-bbffdd23-5562-4473-aa92-64cf51bea26e.png)

Because of Windows encoding, let's convert from UTF-8 to UTF-16LE and we get our flag:

![image](https://user-images.githubusercontent.com/80063008/198265257-087facf9-98bd-48c8-84c4-e68f39f304b9.png)

HTB{5up3r_345y_m4cr05}
