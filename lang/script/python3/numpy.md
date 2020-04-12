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

## logic gate

```python
import numpy as np

def and_gate(x1, x2, b=-0.7):
    x = np.array([x1, x2])
    w = np.array([0.5, 0.5])
    y = np.sum(x * w) + b

    if y <= 0:
        return 0
    else:
        return 1

print(f'0 and 0 => {and_gate(0, 0)}')
print(f'1 and 0 => {and_gate(1, 0)}')
print(f'0 and 1 => {and_gate(0, 1)}')
print(f'1 and 1 => {and_gate(1, 1)}')


def nand_gate(x1, x2, b=0.7):
    x = np.array([x1, x2])
    w = np.array([-0.5, -0.5])
    y = np.sum(x * w) + b
    if y <= 0:
        return 0
    else:
        return 1

print(f'0 nand 0 => {nand_gate(0, 0)}')
print(f'1 nand 0 => {nand_gate(1, 0)}')
print(f'0 nand 1 => {nand_gate(0, 1)}')
print(f'1 nand 1 => {nand_gate(1, 1)}')


def or_gate(x1, x2, b=-0.2):
    x = np.array([x1, x2])
    w = np.array([0.5, 0.5])
    y = np.sum(x * w) + b
    if y <= 0:
        return 0
    else:
        return 1

print(f'0 or 0 => {or_gate(0, 0)}')
print(f'1 or 0 => {or_gate(1, 0)}')
print(f'0 or 1 => {or_gate(0, 1)}')
print(f'1 or 1 => {or_gate(1, 1)}')


def xor_gate(x1, x2):
    s1 = nand_gate(x1, x2)
    s2 = or_gate(x1, x2)
    y = and_gate(s1, s2)
    return y

print(f'0 xor 0 => {xor_gate(0, 0)}')
print(f'1 xor 0 => {xor_gate(1, 0)}')
print(f'0 xor 1 => {xor_gate(0, 1)}')
print(f'1 xor 1 => {xor_gate(1, 1)}')
```
