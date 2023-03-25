This challenge gives us an `alien.h5` file. Running the `file` command on it we can see it's an Hierarchical Data Format:

![image](https://user-images.githubusercontent.com/80063008/227542927-23f410fe-e24b-486a-864b-621191ab29b0.png)

We can parse these in python using the h5py library:

```bash
pip install h5py
```

First let's output the keys:

```python
#!/usr/bin/python3

import h5py

# Open the HDF5 file
with h5py.File('alien.h5', 'r') as f:
    # Print the name of the groups in the file
    print(list(f.keys()))
```

![image](https://user-images.githubusercontent.com/80063008/227543239-dbf3cb00-95a4-4403-87bc-fa4586ba0b17.png)

Next lets print what's in these keys:

```python
import h5py

# Open the H5 file
filename = 'alien.h5'
with h5py.File(filename, 'r') as f:
    model_weights_group = f['model_weights']
    print("Model weights group members:")
    print(model_weights_group.keys())

    optimizer_weights_group = f['optimizer_weights']
    print("Optimizer weights group members:")
    print(optimizer_weights_group.keys())
```
A lot of output is given however a few parts drew my attention. These look like Base64.

![image](https://user-images.githubusercontent.com/80063008/227543983-6d43c1eb-c51f-480b-9bae-4cd23dbe4513.png)

I took the longer string and removed the new lines and decoded it:

![image](https://user-images.githubusercontent.com/80063008/227544984-f2edd634-e5ef-42a0-928b-d6a61de9b2be.png)

I can see the beginning of HTB{ that is Base64 encoded. I added the other two parts smaller parts to it and got the full flag:

![image](https://user-images.githubusercontent.com/80063008/227545271-6a2fdf9a-7d90-44aa-b92b-2fd7eaf46850.png)

HTB{n0t_so_h4rd_to_und3rst4nd}


