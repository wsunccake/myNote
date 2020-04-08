# numpy

```python
import numpy as np

# 1D
np1 = np.array([1, 2, 3])
np2 = np.array([4, 5, 6])

print(np1.ndim, np1.shape, np1.dtype)
print('np1:', np1)
print('np1[2]: ', np1[2])
print('np1[-1]: ', np1[-1])
print('np1[[0, 2]]: ', np1[[0, 2]])
print('np1 + np2 = ', np1 + np2)

# 2D
np2_1 = np.array([[1, 2], [3, 4], [5, 6], [7, 8]])

print('np2_1: ', np2_1)
print('np2_1[0]: ', np2_1[0])
print('np2_1[0, -1]: ', np2_1[[0, -1]])
print('np2_1[0][1]: ', np2_1[0][1])
```
