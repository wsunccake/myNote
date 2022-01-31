# chapter 06

## window

```python
import tkinter
root = tkinter.Tk()
root.mainloop()
```

->

```python
import tkinter
root = tkinter.Tk()
root.title("第一個視窗")
root.geometry("800x600")
root.mainloop()
```


---

## text

```python
import tkinter
root = tkinter.Tk()
root.title("第一個標籤")
root.geometry("800x600")
label = tkinter.Label(root, text="標籤的字串", font=("System", 24))
label.place(x=200, y=100)
root.mainloop()
```

->

```python
import tkinter
import tkinter.font
root = tkinter.Tk()
print(tkinter.font.families())
```


---

## button

```python
import tkinter
root = tkinter.Tk()
root.title("第一個按鈕")
root.geometry("800x600")
button = tkinter.Button(root, text="按鈕的字串", font=("Times New Roman", 24))
button.place(x=200, y=100)
root.mainloop()
```

->

```python
import tkinter

def click_btn():
    button["text"] = "點選按鈕了"

root = tkinter.Tk()
root.title("第一個按鈕")
root.geometry("800x600")
button = tkinter.Button(root, text="請點選按鈕", font=("Times New Roman", 24), command=click_btn)
button.place(x=200, y=100)
root.mainloop()
```

---

## 圖片

```python
import tkinter
root = tkinter.Tk()
root.title("第一張畫布")
canvas = tkinter.Canvas(root, width=400, height=600, bg="skyblue")
canvas.pack()
root.mainloop()
```

->

```python
import tkinter
root = tkinter.Tk()
root.title("第一次顯示圖片")
canvas = tkinter.Canvas(root, width=400, height=600)
canvas.pack()
gazou = tkinter.PhotoImage(file="iroha.png")
canvas.create_image(200, 300, image=gazou)
root.mainloop()
```


---

## 抽籤遊戲

```python
import tkinter
root = tkinter.Tk()
root.title("抽籤遊戲")
root.resizable(False, False)
canvas = tkinter.Canvas(root, width=800, height=600)
canvas.pack()
gazou = tkinter.PhotoImage(file="miko.png")
canvas.create_image(400, 300, image=gazou)
root.mainloop()
```

->

```python
import tkinter
root = tkinter.Tk()
root.title("抽籤遊戲")
root.resizable(False, False)
canvas = tkinter.Canvas(root, width=800, height=600)
canvas.pack()
gazou = tkinter.PhotoImage(file="miko.png")
canvas.create_image(400, 300, image=gazou)
label = tkinter.Label(root, text="？？", font=("Times New Roman", 120), bg="white")
label.place(x=380, y=60)
button = tkinter.Button(root, text="抽籤", font=("Times New Roman", 36), fg="skyblue")
button.place(x=360, y=400)
root.mainloop()
```

->

```python
import tkinter
import random

def click_btn():
    label["text"]=random.choice(["大吉", "中吉", "小吉", " 凶 "])
    label.update()

root = tkinter.Tk()
root.title("抽籤遊戲")
root.resizable(False, False)
canvas = tkinter.Canvas(root, width=800, height=600)
canvas.pack()
gazou = tkinter.PhotoImage(file="miko.png")
canvas.create_image(400, 300, image=gazou)
label = tkinter.Label(root, text="？？", font=("Times New Roman", 120), bg="white")
label.place(x=380, y=60)
button = tkinter.Button(root, text="抽籤", font=("Times New Roman", 36), command=click_btn, fg="skyblue")
button.place(x=360, y=400)
root.mainloop()
```


```python
import tkinter
root = tkinter.Tk()
root.title("在畫布繪製圖形")
root.geometry("500x400")
cvs = tkinter.Canvas(root, width=500, height=400, bg="white")
cvs.pack()
cvs.create_text(250, 25, text="字串", fill="green", font=("Times New Roman", 24))
cvs.create_line(30, 30, 70, 80, fill="navy", width=5)
cvs.create_line(120, 20, 80, 50, 200, 80, 140, 120, fill="blue", smooth=True)
cvs.create_rectangle(40, 140, 160, 200, fill="lime")
cvs.create_rectangle(60, 240, 120, 360, fill="pink", outline="red", width=5)
cvs.create_oval(250-40, 100-40, 250+40, 100+40, fill="silver", outline="purple")
cvs.create_oval(250-80, 200-40, 250+80, 200+40, fill="cyan", width=0)
cvs.create_polygon(250, 250, 150, 350, 350, 350, fill="magenta", width=0)
cvs.create_arc(400-50, 100-50, 400+50, 100+50, fill="yellow", start=30, extent=300)
cvs.create_arc(400-50, 250-50, 400+50, 250+50, fill="gold", start=0, extent=120, style=tkinter.CHORD)
cvs.create_arc(400-50, 350-50, 400+50, 350+50, outline="orange", start=0, extent=120, style=tkinter.ARC)
cvs.mainloop()
```
