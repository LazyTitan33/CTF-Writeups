I used radare2 to debug this application.

Let's first input the binary into the debugger.

```bash
r2 ghost
```

Analyze all the flags

```aaa```

![image](https://user-images.githubusercontent.com/80063008/198257671-e14bf083-8654-4b22-bc03-5612ba488a25.png)

List all functions

```afl```

![image](https://user-images.githubusercontent.com/80063008/198257705-bbf7dcfa-d0dc-471c-acfd-417ad5dfa242.png)

Disassembling any of the functions above using the `pdf` command along with the memory location of the function that is displayed next to it, we get the hard-coded string that is XORed with `0x13`. In this case, we dissasemble the function we care about, the `get_flag` function.

```pdf@0x00001155```

![image](https://user-images.githubusercontent.com/80063008/198257751-30e224cc-f6d6-417a-a8f8-16965ed229ab.png)

This string can also be found by running strings and the XOR operation can be seen using Ghidra as well.

![image](https://user-images.githubusercontent.com/80063008/198257910-904db281-a7e0-4ab8-85a3-9bea764213df.png)

We can use CyberChef to apply the XOR operation and get the flag.

![image](https://user-images.githubusercontent.com/80063008/198257938-4794a12c-5bac-4124-9544-a65fecef18ec.png)

HTB{h4unt3d_by_th3_gh0st5_0f_ctf5_p45t!}
