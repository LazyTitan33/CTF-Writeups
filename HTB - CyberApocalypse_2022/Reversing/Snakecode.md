Snakecode

The most struggle I had with this one was getting a tool installed properly and working properly to decompile the .pyc file.

```
pip install decompyle6
uncompyle6 chall.pyc > decompiled.py
```
The commands above are very straightfoward but depending on the state of your python and its libraries, you might get a lot of errors. My solution was to just use a fresh Ubuntu VM that I keep for testing.

The .pyc file decompiles to this:

```python
import marshal, types, time
ll = types.FunctionType(marshal.loads(('YwEAAAABAAAABQAAAEMAAABzNAAAAHQAAGoBAHQCAGoDAHQEAGQBAIMBAGoFAHwAAGoGAGQCAIMB\nAIMBAIMBAHQHAIMAAIMCAFMoAwAAAE50BAAAAHpsaWJ0BgAAAGJhc2U2NCgIAAAAdAUAAAB0eXBl\nc3QMAAAARnVuY3Rpb25UeXBldAcAAABtYXJzaGFsdAUAAABsb2Fkc3QKAAAAX19pbXBvcnRfX3QK\nAAAAZGVjb21wcmVzc3QGAAAAZGVjb2RldAcAAABnbG9iYWxzKAEAAAB0AQAAAHMoAAAAACgAAAAA\ncwcAAAA8c3RkaW4+dAoAAABsb2FkTGFtYmRhAQAAAHQAAAAA\n').decode('base64')), globals())
i0 = ll('eJxLZoACJiB2BuJiLiBRwsCQwsjQzMgQrAES9ythA5JFiXkp+bkajCB5kKL4+Mzcgvyikvh4DZAB\nCKKYHUjYFJekZObZlXCA2DmJuUkpiXaMEKMZGAC+nBJh\n')
i1 = ll('eJxLZoACJiB2BuJiLiBRwsCQwsjQzMgQrAES9ythA5LJpUXFqcUajCB5kKL4+Mzcgvyikvh4DZAB\nCKKYHUjYFJekZObZlXCA2DmJuUkpiXaMEKMZGADEORJ1\n')
f0 = ll('eJxLZmRgYABhJiB2BuJiXiBRw8CQxcCQwsjQzMgQrAGS8ssEEgwaIJUl7CAiMzc1v7QEIsAMJMoz\n8zTASkBEMUiJTXFJSmaeXQkHiJ2TmJuUkmgHVg5SAQBjWRD5\n')
f1 = ll('eJxLZmRgYIBhZyAu5gISNQwMWQwMzQwMwRogcT8wWcIKJNJTS5IzIFxmIFGemacBpBjARDE7kLAp\nLknJzLMr4QCxcxJzk1IS7cDKQSoAvuUPJw==\n')
f2 = ll('eJx1kL1uwkAQhOfOBsxPQZUmL+DOEnWUBghEQQbFIESVglUkY5ECX+lHoMz7Jrt7HCgSOWlGO/rm\n1tbtIwBBY1b9zdYYkEFlcRqiAQoWxaginDJhjcUBijNQy+O24jxgfzsHdTxOFB8DtoqPoK7HPcXn\ngCPFZ1BfcUGsdMA/lpc/fEqeUBq21Mp0L0rv/3grX/f5aELlbryVYzbXZnub7j42K5dcxslym7vu\nJby/zubrK1pMX9apPLOTraReqe9T3SlWd9ieakfl17OTb36OpFE/CDQDE5vHv7K/FKBNmA==\n')
f3 = ll('eJxVj00KAjEMhV+b8Q9040IZT9C9WxHEvRvBC1iFUhhk2sUIIwgexLWn1KQzI9qSl/DlhaZHDSDj\nII4tR3ix1IBVyK1GXitImt/0l1JDSSih1rAZfIZyI4x9BRIkeKA8SLeF1Dl9clIHG+c9OakdZ35O\nT/o+yiciZI2Hgvpt702Pt925Nx/HFZwSGbIYqaL87FS5aKSIgi5JbZR/F1WTrkZmk4QByypE64p1\nap6X4g8LaaoZ3zFGfzFVE/UBTuovhA==\n')
f4 = ll('eJw1zDsKgEAMBNCJilb2drZ7AEuxsbfxBOIHFFkWNqWdF3eyYJEXkgxZcwB/jazYkkdwUeAVCAcV\nW3F4MjTt7ISZyWVUS7KEsPtN7cW9e2ddLeKTIXk7gkSsSB91O/2g9uToLBELO0otH2W6Ez8=\n')
f5 = ll('eJxdjr0OwjAMhM9J+as6M7HTF0AsiKV7F54ACJUKVaiSjOnEi2MbISQGf4rtu3OuMwBSBVfDFQdG\nBhzwMAgNMsER1s58+wJ3Hlm4Ai/z33YGE+A1IrNljnBBtiLYT1ZSf2sr6lMt19u+ZPYQkGDJqA0j\nycfap7+lBT/C2bveJ/UkEQ7KqByTGMbPKNQSpojiPMTEzqNKup2aKlnShramopJW5g2ipyUM\n')
f6 = ll('eJxdjTEOglAQRB98iMbEKxhLbkBjaLSwsrHWBEUJCRKULTT5VFzc3W9nMS+zk93ZqwNS1UK1VQ17\nRQ0CVcQUsTvljO4vWjEmSIRP8A4PXn3MlHKOea4DlxyzWMsOjXUHK/bpVXb1TWy855kF2gN9SPo2\nDD9+At8Zdm4YZorNIFXTFTI335aPS1UWtie28QV3xx4p\n')
f7 = ll('eJxtjz8LwjAQxV/S1mrRxcnZKat/qyAuOrv0E4ilIJRS2hsUCg7OfmcvubZTIe/97nKPcHkEADpd\nWPWPjYCGj0Kj0fjIfHwVqiWIbzxbJ6SHEleQ1yf8ocQHFLSJqgKN+nTYVUUEGndNCiRG8UY3M7F7\nabb7TrAS7AVrQSw4CDaCreBo7CfJPvdy/nZeummZuyY3bHBWh2ynmtJncXaRLLaJem6HaqGiVlMV\n6Zn+Azn/L1k=\n')
f8 = ll('eJwljr0KAkEMhCf3o2hrIb7BlWIhFiKC1jYWViKHe+qKnHob0GKt7sVNcsV8ZDeTSc45gJ5oINqI\nwkkQgTvQAvRdgwmO0BK2xxl+uTUTxBwugUtxT8EZIiHKZ4o21dZE7FLRe4yD+nMLixlchvG+0KU7\nPxR6EVjhSVDoKazt86MqG6uasr5WrI3SucCNbJPEp685keIy576aqktThVs3r0kf48s8r4c9Ogaj\nL3SnIej8MrDz9aqLXJhPzwMNaURT4R/aUC0X\n')
a1 = ll('eJxLZmRgYIBhZyAuZgESKYwMwRpMQIZfCUhcWwNIMGiAmGB+DoQPIorZgYRNcUlKZp5dCQeInZOY\nm5SSaAdWDFIBALI0C1U=\n')
a2 = ll('eJxLZmRgYIBhZyAuZgESKYwMwRpMQIZfCUhcWQNIMGiAmGB+DoQPIorZgYRNcUlKZp5dCQeInZOY\nm5SSaAdWDFIBALBMC00=\n')
a3 = ll('eJw10EtLw0AUBeAzTWLqo74bML8gSyFdiotm40rEZF+kRyVtCGKmqzar/nHvHBDmfty5c+fBrB2A\niUVuUVkMG4MOnIARGIMJeAKm4BQ8Bc9UsfwcvABn/5VL8Aq81tINeAveKb/Hd47R4WDDTp5j7hEm\nR4fsoS4yu+7Vh1e8yEYu5V7WciffZCl/5UpW8l162cuF3Mq1fJSUY5uYhTZFRvfZF+EvfOCnU89X\ngdATGFLjafBs+2e1fJShY4jDomvcH1q4K9U=\n')
a4 = ll('eJxLZmRgYIBhZyAuZgESKYwMwRpMQIZfCUhcRQNIMGiAmGB+DoQPIorZgYRNcUlKZp5dCQeInZOY\nm5SSaAdWDFIBALCJC04=\n')
a5 = ll('eJxNzTELwjAQBeCXS4r6TzKJP6DUgruLq0s1S7BKIRkqJP/dd3Hp8D4ex3H3NAA6xjEXJo2kAHeH\nalAF1aI6FINg8BIsZxTZdM5lM2/95i2PXCNBPBCvzeubLOR4yvp2bX6bS3P+LyppR/qUQ/wMea99\nnt6PMA26l/SKxQ/XGxky\n')
a6 = ll('eJwlzLsKwkAQheF/L0afw2qr4AOENOnT2NpEgyDGENgtFHbfPTNrcT6G4cw8DHCQeMkgiWchw81T\nDMVSHMWTDdnytGTHu+Ea9G4MAkHPkxXaS9L1t/qrbtXlX1TiUehiml9rn046L9PnPk+99qJ+cewN\nxxM9\n')
a7 = ll('eJwlzLEKwjAQxvF/rhF9jk6Zig8gXdy7uLq0FqFYRUiGFpJ39y4O34/j+O4eDjhovOaqia2S4e4p\njiKUhuLJjiw8hex5Cbdgd0NQCHaeROnOydZbda9+q+u/aMSjcolpXj59Otm8ju9pHnvrRfvS8AMM\nqhM6\n')
a8 = ll('eJxLZmRgYABhJiB2BuJiPiBRw8CQwsgglsLEkM3EEKzBDBTyy2QFkplAzKABJkCaSkBEjgZcsJgd\nSNgUl6Rk5tmVcIDYOYm5SSmJdmDFIBUAVDAM/Q==\n')
a9 = ll('eJxLZmRgYIBhZyAuZgESKYwMwRpMQIZfCUhcQQNIMGiAmGB+DoQPIorZgYRNcUlKZp5dCQeInZOY\nm5SSaAdWDFIBAK+VC0o=\n')
m0 = ll('eJw1jTELwjAUhC9Jq/0VzhldBAfr4u7i6mYpFFSKCXRJp/7x3rsi5L5Avnsvrx0AS8PcmNQSGSg8\nDsWjBJQKS42nxwzMQSog09b/gsrs9AGP6LjhHr3tMfSn7TpH+yebfYtJHGXH7eknTpGAkPbEJeVu\n+F5V/Bw1Wpl0B7cCYGsZOw==\n')
m1 = ll('eJw1zUEKAjEMBdCfdMQreIRuRwU3Mhv3bjzCDAOCitCAm7rqxU1+cZGX0v408wbAvy5e5eQYUAUm\nqAnNHdASvsJLhSVUBpryoPG6Km5ZfPaah/hBnXXf29jbsbdDjl0W2Tdd6IN+6JwdkLJ1zsWW+2vi\n/HOMRIklkJ38AF2QGOk=\n')
m2 = ll('eJxNjj8LAjEMxV96fz+Fk0NHdT5c3F1cD5c7BEHlsAWXdrov7kuKICS/0LyXpFMP4JcnZrgSEUgM\nQXJIDVKLtcHokAWZKvsVUm0eGjr1rC3GCplBW/03Xpy2hM5bj4sXnjh7p4cUz30pO6+fiKouxtn6\ny8MehcH4MU7GtydgCB0xhDjfX8ey8mAzrYqyka18AW5IIKw=\n')

def snake(w):
    r = i0()
    c = i1()
    f0(w)
    d = (0, 1)
    p = [(5, 5)]
    pl = 1
    s = 0
    l = None
    while 1:
        p, d, pl, l, s, w, c, r = m2(p, d, pl, l, s, w, c, r)
        time.sleep(0.4)

    return


i1().wrapper(snake)
```

Running the script we get a nice little snake game. This was surprising to say the least. I ended up playing it a bit to see how big I could get. I noticed that the flag starts appearing character by character at certain points. Specifically, every 5 pallets, we get a character.

![image](https://user-images.githubusercontent.com/80063008/169346801-0e44e540-eee3-4f3e-89d9-4469aaddc853.png)

Using print statements and running the game after each one, I was able to figure out what each variable does and renamed them accordingly.

```python
def snake(w):
    random = i0()
    curses = i1()
    f0(w)
    position = (0, 1)
    xyPos = [(5, 5)]
    foodNo = 125
    movedCounter = 0
    foodPos = (1, 1)
    while 1:
        xyPos, position, foodNo, foodPos, movedCounter, w, curses, random = m2(xyPos, position, foodNo, foodPos, movedCounter, w, curses, random)
        time.sleep(0.4)

    return
```

I can control the food number, and its position. The first one, 0, is H… then the 5th one is T. Every 5th pallet is a letter. Changed foodNo until we got the full flag.

HTB{SuP3r_S3CRt_Sn4k3c0d3}
