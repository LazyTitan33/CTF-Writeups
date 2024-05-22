### Challenge Description

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/cabf4dcd-cb39-4b2c-8226-097dfb4ac48c)

## Solution

The challenge provides a simple text file with what looks to be an AWS IAM role id: `AROAXYAFLIG2BLQFIIP34`. A bit of research led us to [this](https://hackingthe.cloud/aws/enumeration/enumerate_principal_arn_from_unique_id/) helpful article.

From our own AWS portal, we go to IAM role and create a custom trust policy in which we set the principal AWS to the provided role id.  

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/8797cd35-86de-4bed-924f-b7273341d9bd)

We can save this with whatever name we want. Then we access the role and look at the Trust Relationships. We will see that the `arn` we need was populated:  

![image](https://github.com/LazyTitan33/CTF-Writeups/assets/80063008/defeb2e7-c1d1-4c45-a046-436a9a7e0362)

`HTB{arn:aws:iam::532587168180:role/vault101}`
