# chapter 07

## place

```python
import tkinter
root = tkinter.Tk()
root.title("第一個文字輸入欄位")
root.geometry("400x200")
entry = tkinter.Entry(width=20)
entry.place(x=10, y=10)
root.mainloop()
```

->

```python
import tkinter

def click_btn():
    txt = entry.get()
    button["text"] = txt

root = tkinter.Tk()
root.title("第一個文字輸入欄位")
root.geometry("400x200")
entry = tkinter.Entry(width=20)
entry.place(x=20, y=20)
button = tkinter.Button(text="取得字串", command=click_btn)
button.place(x=20, y=100)
root.mainloop()
```


---

## pack

```python
import tkinter

def click_btn():
    text.insert(tkinter.END, "怪物出現了！")

root = tkinter.Tk()
root.title("輸入多列文字")
root.geometry("400x200")
button = tkinter.Button(text="訊息", command=click_btn)
button.pack()
text = tkinter.Text()
text.pack()
root.mainloop()
```


---

## check button

```python
import tkinter
root = tkinter.Tk()
root.title("使用勾選按鈕")
root.geometry("400x200")
cbtn = tkinter.Checkbutton(text="勾選按鈕")
cbtn.pack()
root.mainloop()
```

->

```python
import tkinter
root = tkinter.Tk()
root.title("預設為勾選的狀態")
root.geometry("400x200")
cval = tkinter.BooleanVar()
cval.set(True)
cbtn = tkinter.Checkbutton(text="勾選按鈕", variable=cval)
cbtn.pack()
root.mainloop()
```

->

```python
import tkinter

def check():
    if cval.get() == True:
        print("已勾選")
    else:
        print("未勾選")

root = tkinter.Tk()
root.title("取得勾選狀態")
root.geometry("400x200")
cval = tkinter.BooleanVar()
cval.set(False)
cbtn = tkinter.Checkbutton(text="勾選按鈕", variable=cval, command=check)
cbtn.pack()
root.mainloop()
```


---

## message box

```python
import tkinter
import tkinter.messagebox

def click_btn():
    tkinter.messagebox.showinfo("資訊", "點選按鈕了")

root = tkinter.Tk()
root.title("第一個訊息方塊")
root.geometry("400x200")
btn = tkinter.Button(text="測試", command=click_btn)
btn.pack()
root.mainloop()
```


---

## cat game

```python
import tkinter

root = tkinter.Tk()
root.title("貓咪相似度診斷程式")
root.resizable(False, False)
canvas = tkinter.Canvas(root, width=800, height=600)
canvas.pack()
gazou = tkinter.PhotoImage(file="sumire.png")
canvas.create_image(400, 300, image=gazou)
button = tkinter.Button(text="診斷", font=("Times New Roman", 32), bg="lightgreen")
button.place(x=400, y=480)
text = tkinter.Text(width=40, height=5, font=("Times New Roman", 16))
text.place(x=320, y=30)
root.mainloop()
```

->

```python
import tkinter

root = tkinter.Tk()
root.title("貓咪相似度診斷程式")
root.resizable(False, False)
canvas = tkinter.Canvas(root, width=800, height=600)
canvas.pack()
gazou = tkinter.PhotoImage(file="sumire.png")
canvas.create_image(400, 300, image=gazou)
button = tkinter.Button(text="診斷", font=("Times New Roman", 32), bg="lightgreen")
button.place(x=400, y=480)
text = tkinter.Text(width=40, height=5, font=("Times New Roman", 16))
text.place(x=320, y=30)

bvar = [None]*7
cbtn = [None]*7
ITEM = [
"喜歡高處",
"看到球就想玩",
"嚇一跳的時候，頭髮會立起來",
"喜歡造型像老鼠的玩具",
"對味道很敏感",
"喜歡啃魚骨",
"晚上特別有精神"
]
for i in range(7):
    bvar[i] = tkinter.BooleanVar()
    bvar[i].set(False)
    cbtn[i] = tkinter.Checkbutton(text=ITEM[i], font=("Times New Roman", 12), variable=bvar[i], bg="#dfe")
    cbtn[i].place(x=400, y=160+40*i)
root.mainloop()
```

->

```python
import tkinter

def click_btn():
    pts = 0
    for i in range(7):
        if bvar[i].get() == True:
            pts = pts + 1
    text.delete("1.0", tkinter.END)
    text.insert("1.0", "勾選的個數是" + str(pts))

root = tkinter.Tk()
root.title("貓咪相似度診斷程式")
root.resizable(False, False)
canvas = tkinter.Canvas(root, width=800, height=600)
canvas.pack()
gazou = tkinter.PhotoImage(file="sumire.png")
canvas.create_image(400, 300, image=gazou)
button = tkinter.Button(text="診斷", font=("Times New Roman", 32), bg="lightgreen", command=click_btn)
button.place(x=400, y=480)
text = tkinter.Text(width=40, height=5, font=("Times New Roman", 16))
text.place(x=320, y=30)

bvar = [None]*7
cbtn = [None]*7
ITEM = [
"喜歡高處",
"看到球就想玩",
"嚇一跳的時候，頭髮會立起來",
"喜歡造型像老鼠的玩具",
"對味道很敏感",
"喜歡啃魚骨",
"晚上特別有精神"
]
for i in range(7):
    bvar[i] = tkinter.BooleanVar()
    bvar[i].set(False)
    cbtn[i] = tkinter.Checkbutton(text=ITEM[i], font=("Times New Roman", 12), variable=bvar[i], bg="#dfe")
    cbtn[i].place(x=400, y=160+40*i)
root.mainloop()
```

->

```python
import tkinter

KEKKA = [
"你的前世是貓咪的可能性趨近於零。",
"你只是很普通的人類。",
"沒有什麼特別之處。",
"有些地方很像貓咪。",
"個性很像貓咪。",
"個性非常像貓咪。",
"前世有可能是貓咪。",
"外表是人類，內在卻是貓咪。"
]
def click_btn():
    pts = 0
    for i in range(7):
        if bvar[i].get() == True:
            pts = pts + 1
    nekodo = int(100*pts/7)
    text.delete("1.0", tkinter.END)
    text.insert("1.0", "＜診斷結果＞\n貓咪相似度是" + str(nekodo) + "％喲。\n" + KEKKA[pts])

root = tkinter.Tk()
root.title("貓咪相似度診斷程式")
root.resizable(False, False)
canvas = tkinter.Canvas(root, width=800, height=600)
canvas.pack()
gazou = tkinter.PhotoImage(file="sumire.png")
canvas.create_image(400, 300, image=gazou)
button = tkinter.Button(text="診斷", font=("Times New Roman", 32), bg="lightgreen", command=click_btn)
button.place(x=400, y=480)
text = tkinter.Text(width=40, height=5, font=("Times New Roman", 16))
text.place(x=320, y=30)

bvar = [None]*7
cbtn = [None]*7
ITEM = [
"喜歡高處",
"看到球就想玩",
"嚇一跳的時候，頭髮會立起來",
"喜歡造型像老鼠的玩具",
"對味道很敏感",
"喜歡啃魚骨",
"晚上特別有精神"
]
for i in range(7):
    bvar[i] = tkinter.BooleanVar()
    bvar[i].set(False)
    cbtn[i] = tkinter.Checkbutton(text=ITEM[i], font=("Times New Roman", 12), variable=bvar[i], bg="#dfe")
    cbtn[i].place(x=400, y=160+40*i)
root.mainloop()
```
