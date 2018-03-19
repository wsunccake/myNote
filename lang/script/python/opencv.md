# opencv

```bash
centos:~ # yum install opencv
centos:~ # pip install numpy opencv-python
```

```python
import cv2

img = cv2.imread('./hello.jpg', cv2.IMREAD_GRAYSCALE) 
print(img.shape)
cv2.imwrite('test.jpg', img)

centos:~ # python hello.py
```
