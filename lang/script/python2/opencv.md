# opencv

```bash
centos:~ # yum install opencv
centos:~ # pip install numpy opencv-python
```

```python
import cv2

img = cv2.imread('./hello.jpg', cv2.IMREAD_GRAYSCALE) 
print(img.shape)

# save image
cv2.imwrite('test.jpg', img)

# gray scale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# brightness
img += 20

# show image
cv2.imshow('image',img)
cv2.waitKey(0)
cv2.destroyAllWindows()

centos:~ # python hello.py
```
