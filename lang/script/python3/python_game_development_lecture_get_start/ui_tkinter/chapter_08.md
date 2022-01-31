# chapter 08

## after

```python
import tkinter
tmr = 0
def count_up():
    global tmr
    tmr = tmr + 1
    label["text"] = tmr
    root.after(1000, count_up)

root = tkinter.Tk()
label = tkinter.Label(font=("Times New Roman", 80))
label.pack()
root.after(1000, count_up)
root.mainloop()
```


---

## bind

```python
import tkinter
key = 0
def key_down(e):
    global key
    key = e.keycode
    print("KEY:"+str(key))

root = tkinter.Tk()
root.title("取得鍵碼")
root.bind("<KeyPress>", key_down)
root.mainloop()
```


---

## key

```python
import tkinter

key = 0
def key_down(e):
    global key
    key = e.keycode

def main_proc():
    label["text"] = key
    root.after(100, main_proc)

root = tkinter.Tk()
root.title("即時按鍵輸入處理")
root.bind("<KeyPress>", key_down)
label = tkinter.Label(font=("Times New Roman", 80))
label.pack()
main_proc()
root.mainloop()
```

->

```python
import tkinter

key = ""
def key_down(e):
    global key
    key = e.keysym

def main_proc():
    label["text"] = key
    root.after(100, main_proc)

root = tkinter.Tk()
root.title("即時按鍵輸入處理")
root.bind("<KeyPress>", key_down)
label = tkinter.Label(font=("Times New Roman", 80))
label.pack()
main_proc()
root.mainloop()
```

->

```python
import tkinter

key = ""
def key_down(e):
    global key
    key = e.keysym
def key_up(e):
    global key
    key = ""

cx = 400
cy = 300
def main_proc():
    global cx, cy
    if key == "Up":
        cy = cy - 20
    if key == "Down":
        cy = cy + 20
    if key == "Left":
        cx = cx - 20
    if key == "Right":
        cx = cx + 20
    canvas.coords("MYCHR", cx, cy)
    root.after(100, main_proc)

root = tkinter.Tk()
root.title("移動角色")
root.bind("<KeyPress>", key_down)
root.bind("<KeyRelease>", key_up)
canvas = tkinter.Canvas(width=800, height=600, bg="lightgreen")
canvas.pack()
img = tkinter.PhotoImage(file="mimi.png")
canvas.create_image(cx, cy, image=img, tag="MYCHR")
main_proc()
root.mainloop()
```


---

## 顯示迷宮

```python
import tkinter
root = tkinter.Tk()
root.title("顯示迷宮")
canvas = tkinter.Canvas(width=800, height=560, bg="white")
canvas.pack()
maze = [
    [1,1,1,1,1,1,1,1,1,1],
    [1,0,0,0,0,0,1,0,0,1],
    [1,0,1,1,0,0,1,0,0,1],
    [1,0,0,1,0,0,0,0,0,1],
    [1,0,0,1,1,1,1,1,0,1],
    [1,0,0,0,0,0,0,0,0,1],
    [1,1,1,1,1,1,1,1,1,1]
    ]
for y in range(7):
    for x in range(10):
        if maze[y][x] == 1:
            canvas.create_rectangle(x*80, y*80, x*80+80, y*80+80, fill="gray")
root.mainloop()
```


---

## 迷宮內移動

```python
import tkinter

key = ""
def key_down(e):
    global key
    key = e.keysym
def key_up(e):
    global key
    key = ""

mx = 1
my = 1
def main_proc():
    global mx, my
    if key == "Up" and maze[my-1][mx] == 0:
        my = my - 1
    if key == "Down" and maze[my+1][mx] == 0:
        my = my + 1
    if key == "Left" and maze[my][mx-1] == 0:
        mx = mx - 1
    if key == "Right" and maze[my][mx+1] == 0:
        mx = mx + 1
    canvas.coords("MYCHR", mx*80+40, my*80+40)
    root.after(300, main_proc)

root = tkinter.Tk()
root.title("在迷宮之內移動")
root.bind("<KeyPress>", key_down)
root.bind("<KeyRelease>", key_up)
canvas = tkinter.Canvas(width=800, height=560, bg="white")
canvas.pack()

maze = [
    [1,1,1,1,1,1,1,1,1,1],
    [1,0,0,0,0,0,1,0,0,1],
    [1,0,1,1,0,0,1,0,0,1],
    [1,0,0,1,0,0,0,0,0,1],
    [1,0,0,1,1,1,1,1,0,1],
    [1,0,0,0,0,0,0,0,0,1],
    [1,1,1,1,1,1,1,1,1,1]
    ]
for y in range(7):
    for x in range(10):
        if maze[y][x] == 1:
            canvas.create_rectangle(x*80, y*80, x*80+79, y*80+79, fill="skyblue", width=0)

img = tkinter.PhotoImage(file="mimi_s.png")
canvas.create_image(mx*80+40, my*80+40, image=img, tag="MYCHR")
main_proc()
root.mainloop()
```


---

## 迷宮遊戲

```python
import tkinter

key = ""
def key_down(e):
    global key
    key = e.keysym
def key_up(e):
    global key
    key = ""

mx = 1
my = 1
def main_proc():
    global mx, my
    if key == "Up" and maze[my-1][mx] == 0:
        my = my - 1
    if key == "Down" and maze[my+1][mx] == 0:
        my = my + 1
    if key == "Left" and maze[my][mx-1] == 0:
        mx = mx - 1
    if key == "Right" and maze[my][mx+1] == 0:
        mx = mx + 1
    if maze[my][mx] == 0:
        maze[my][mx] = 2
        canvas.create_rectangle(mx*80, my*80, mx*80+79, my*80+79, fill="pink", width=0)
    canvas.delete("MYCHR")
    canvas.create_image(mx*80+40, my*80+40, image=img, tag="MYCHR")
    root.after(300, main_proc)

root = tkinter.Tk()
root.title("塗滿迷宮的地板")
root.bind("<KeyPress>", key_down)
root.bind("<KeyRelease>", key_up)
canvas = tkinter.Canvas(width=800, height=560, bg="white")
canvas.pack()

maze = [
    [1,1,1,1,1,1,1,1,1,1],
    [1,0,0,0,0,0,1,0,0,1],
    [1,0,1,1,0,0,1,0,0,1],
    [1,0,0,1,0,0,0,0,0,1],
    [1,0,0,1,1,1,1,1,0,1],
    [1,0,0,0,0,0,0,0,0,1],
    [1,1,1,1,1,1,1,1,1,1]
    ]
for y in range(7):
    for x in range(10):
        if maze[y][x] == 1:
            canvas.create_rectangle(x*80, y*80, x*80+79, y*80+79, fill="skyblue", width=0)

img = tkinter.PhotoImage(file="mimi_s.png")
canvas.create_image(mx*80+40, my*80+40, image=img, tag="MYCHR")
main_proc()
root.mainloop()
```

->

```python
import tkinter
import tkinter.messagebox

key = ""
def key_down(e):
    global key
    key = e.keysym
def key_up(e):
    global key
    key = ""

mx = 1
my = 1
yuka = 0
def main_proc():
    global mx, my, yuka
    if key == "Up" and maze[my-1][mx] == 0:
        my = my - 1
    if key == "Down" and maze[my+1][mx] == 0:
        my = my + 1
    if key == "Left" and maze[my][mx-1] == 0:
        mx = mx - 1
    if key == "Right" and maze[my][mx+1] == 0:
        mx = mx + 1
    if maze[my][mx] == 0:
        maze[my][mx] = 2
        yuka = yuka + 1
        canvas.create_rectangle(mx*80, my*80, mx*80+79, my*80+79, fill="pink", width=0)
    canvas.delete("MYCHR")
    canvas.create_image(mx*80+40, my*80+40, image=img, tag="MYCHR")
    if yuka == 30:
        canvas.update()
        tkinter.messagebox.showinfo("恭喜！", "所有地板都塗色了！")
    else:
        root.after(300, main_proc)

root = tkinter.Tk()
root.title("塗滿迷宮的地板")
root.bind("<KeyPress>", key_down)
root.bind("<KeyRelease>", key_up)
canvas = tkinter.Canvas(width=800, height=560, bg="white")
canvas.pack()

maze = [
    [1,1,1,1,1,1,1,1,1,1],
    [1,0,0,0,0,0,1,0,0,1],
    [1,0,1,1,0,0,1,0,0,1],
    [1,0,0,1,0,0,0,0,0,1],
    [1,0,0,1,1,1,1,1,0,1],
    [1,0,0,0,0,0,0,0,0,1],
    [1,1,1,1,1,1,1,1,1,1]
    ]
for y in range(7):
    for x in range(10):
        if maze[y][x] == 1:
            canvas.create_rectangle(x*80, y*80, x*80+79, y*80+79, fill="skyblue", width=0)

img = tkinter.PhotoImage(file="mimi_s.png")
canvas.create_image(mx*80+40, my*80+40, image=img, tag="MYCHR")
main_proc()
root.mainloop()
```

->

```python
import tkinter
import tkinter.messagebox

key = ""
def key_down(e):
    global key
    key = e.keysym
def key_up(e):
    global key
    key = ""

mx = 1
my = 1
yuka = 0
def main_proc():
    global mx, my, yuka
    if key == "Shift_L" and yuka > 1:
        canvas.delete("PAINT")
        mx = 1
        my = 1
        yuka = 0
        for y in range(7):
            for x in range(10):
                if maze[y][x] == 2:
                    maze[y][x] = 0
    if key == "Up" and maze[my-1][mx] == 0:
        my = my - 1
    if key == "Down" and maze[my+1][mx] == 0:
        my = my + 1
    if key == "Left" and maze[my][mx-1] == 0:
        mx = mx - 1
    if key == "Right" and maze[my][mx+1] == 0:
        mx = mx + 1
    if maze[my][mx] == 0:
        maze[my][mx] = 2
        yuka = yuka + 1
        canvas.create_rectangle(mx*80, my*80, mx*80+79, my*80+79, fill="pink", width=0, tag="PAINT")
    canvas.delete("MYCHR")
    canvas.create_image(mx*80+40, my*80+40, image=img, tag="MYCHR")
    if yuka == 30:
        canvas.update()
        tkinter.messagebox.showinfo("恭喜！", "所有地板都塗色了！")
    else:
        root.after(300, main_proc)

root = tkinter.Tk()
root.title("塗滿迷宮的地板")
root.bind("<KeyPress>", key_down)
root.bind("<KeyRelease>", key_up)
canvas = tkinter.Canvas(width=800, height=560, bg="white")
canvas.pack()

maze = [
    [1,1,1,1,1,1,1,1,1,1],
    [1,0,0,0,0,0,1,0,0,1],
    [1,0,1,1,0,0,1,0,0,1],
    [1,0,0,1,0,0,0,0,0,1],
    [1,0,0,1,1,1,1,1,0,1],
    [1,0,0,0,0,0,0,0,0,1],
    [1,1,1,1,1,1,1,1,1,1]
    ]
for y in range(7):
    for x in range(10):
        if maze[y][x] == 1:
            canvas.create_rectangle(x*80, y*80, x*80+79, y*80+79, fill="skyblue", width=0)

img = tkinter.PhotoImage(file="mimi_s.png")
canvas.create_image(mx*80+40, my*80+40, image=img, tag="MYCHR")
main_proc()
root.mainloop()
```


```python
import tkinter

pnum = 0
def photograph():
    global pnum
    canvas.delete("PH")
    canvas.create_image(400, 300, image=photo[pnum], tag="PH")
    pnum = pnum + 1
    if pnum >= len(photo):
        pnum = 0
    root.after(7000, photograph)

root = tkinter.Tk()
root.title("數位相框")
canvas = tkinter.Canvas(width=800, height=600)
canvas.pack()
photo = [
tkinter.PhotoImage(file="cat00.png"),
tkinter.PhotoImage(file="cat01.png"),
tkinter.PhotoImage(file="cat02.png"),
tkinter.PhotoImage(file="cat03.png")
]
photograph()
root.mainloop()
```
