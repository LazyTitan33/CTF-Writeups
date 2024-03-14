# Unbreakable

## Solution
This challenge comes with a flag.txt and a main.py containing the source code of the application.  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/cf7ca9f7-e141-4245-bf57-71c9bc67bc2e)

I've copied the source code below taking out the cool ASCII artwork to make it fit better here:

```python3
#!/usr/bin/python3

banner1 = '''cool ascii art 1'''
banner2 = '''cool ascii art 2'''
blacklist = [ ';', '"', 'os', '_', '\\', '/', '`',
              ' ', '-', '!', '[', ']', '*', 'import',
              'eval', 'banner', 'echo', 'cat', '%', 
              '&', '>', '<', '+', '1', '2', '3', '4',
              '5', '6', '7', '8', '9', '0', 'b', 's', 
              'lower', 'upper', 'system', '}', '{' ]
while True:
  ans = input('Break me, shake me!\n\n$ ').strip()
    if any(char in ans for char in blacklist):
    print(f'\n{banner1}\nNaughty naughty..\n')
  else:
    try:
      eval(ans + '()')
      print('WHAT WAS THAT?!\n')
    except:
      print(f"\n{banner2}\nI'm UNBREAKABLE!\n")
```

So it is obvious from the source code, that we need to break out of a python jail while bypassing or skirting around some well placed filters. I spent more time than I care to admit on this one experimenting locally. I was overcomplicating matters as I tend to do until I caught myself doing something dumb...

I was trying to do `open('flag.txt').read` because it adds the `()` by itself, but kept getting:  

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/4ea4c585-13a7-4a40-a6c6-970f7dbdb9de)

I kept looking to see what characters are triggering the blacklist but none were.. it was actually evaluating correct, just not outputting anything.. which is normal given the code. So I told it to print:  

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/7dbd4f67-cdb7-4e2e-b648-7be6f08c15e6)

Easy peasy. This is a lesson I keep learning. The more challenges I do, the more techniques or tools I learn about, the more I tend to overthink things. Also.. I need to manage my time better during these CTFs and sleep more. 

PSA: Don't do CTF challenges while sleep deprived, you won't get anywhere.

`HTB{3v4l_0r_3vuln??}`
