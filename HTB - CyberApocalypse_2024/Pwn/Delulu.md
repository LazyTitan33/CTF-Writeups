# Delulu

## Solution 
Based on this code, it looks like the program calls `printf` directly on the user input with no sanitization. This usually means there's a format string vulnerability here.

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/42a35290-a820-48d7-8f9c-94f4fb8316bd)

Which is confirmed when we see we can read environment variables.  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/e749fb7d-61a1-4532-b158-3b40eb3c67a7)

But, given that the flag is not in an environment variable, and we need to pass the if condition, it means we need to abuse arbitrary write which is also possible with format string using `$n`. However, we need to write a word, not a dword and for that, we have `$hn`.

Now we just have to figure out how much to write and where. `0xbeef` is what we need to write to make the if condition true. Where is easy to figure out, because we are dealing with a 64bit binary, the first 5 are registries and the first argument isn't taken into consideration by format string. So we need to write in the 7th positional argument which we can do with `%7$hn`

Converting `0xbeef` to Decimal we get `48879`:  

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/1b66f61b-6c90-48e3-ae7a-5b434c0ca958)

We also add a `c` after the decimal as the format specifier for printing characters and we get this payload which writes our "id" as the expected one and thus making the if condition true.

```
%48879c%7$hn
```

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/36cf5451-421f-409b-9afd-31f801460753)

`HTB{m45t3r_0f_d3c3pt10n}`
