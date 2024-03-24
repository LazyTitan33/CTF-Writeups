# password-manager-is-a-must

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/c438f29b-3e20-45b0-9b6c-3b86015e27a5)

# Solution

Running strings on the provided dump, we can tell that it's a proc dump of the `keepass.exe` process.  

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/c60af534-41bb-484f-b008-1efbc58f44b4)

We can clone the [keepass-password-dumper](https://github.com/vdohney/keepass-password-dumper) locally and run it on the dump file to get the password from it:

```cmd
git clone https://github.com/vdohney/keepass-password-dumper
dotnet run File.dmp
```

As usual with this method, the first 2 characters are not exact but can be deduced:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/04ba0773-bc9b-403f-bb21-f6396613cdc7)

Password: `thesecretpass`

And we can now get the flag from the keepass file:  
![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/d7c82de5-f93e-48d8-9099-77de5245aea0)

`CTF{c112b162e0567cbc5ae20558511ab3932446a708bc40a97e88e3faac7c242423}`
