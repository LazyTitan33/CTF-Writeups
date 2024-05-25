## Secret Info

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/dfa54ef7-0c3d-4fa5-94b7-42b6cce36f27)

## Enumeration

For this challenge, I built the docker using the provided source code. I logged into the administration panel to see where the file is located. Within the docker, the file was accessible publicly from:  

`/wp-content/uploads/2024/05/flag_secret_not_so_random_get_me_1337.png`

## Solution

Turns out that the same is valid for the challenge instance as well.

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/2df5d203-0bfd-49fb-a549-46d19185dff3)

`CTF{it_is_a_feature_by_cor_xd}`

Note: I didn't understand the point of this challenge. It felt lazy and a missed oppourtunity to do something with a potentially cool wordpress plugin.
