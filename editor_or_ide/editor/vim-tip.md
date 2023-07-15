# vim tip

## content

- [motion](#motion)
- [open file](#open-file)
- [copy and move text](#copy-and-move-text)
- [window](#window)
- [tab page](#tab-page)
- [select all](#select-all)
- [search and replace pattern](#search-and-replace-pattern)
- [search from select mode](#search-from-select-mode)

---

## motion

- goto char on line (){char}
  - right / forward: (f), (t), (;)
  - left / backward: (F), (T), (,)
- goto line end ($)
- goto line head (0), (^)
- goto word
  - right / forward: (w), (W), (e), (E)
  - left / backward: (b), (B)
- goto file head (gg)
- goto file end (G)

---

## open file

- goto file (gf)
- goto file by horizontal window (CTRL-W_f)
- goto file by vertical window (CTRL-W_v)
- goto file by page tab (CTRL-W_gf)

---

## copy and move text

- yank
  - line (yy)
  - text (y){motion}
- put text (p), (P)
- delete and insert
  - (c){motion}
  - char (s), (cl)
  - line (S), (cc)

---

## window

- split open
  - horizontal (CTRL-W_s),(:sp)
  - vertical (CTRL-W_s),(:vs)
- close (CTRL-W_q), (:q)
- move
  - up (CTRL-W_k)
  - down (CTRL-W_j)
  - left (CTRL-W_h)
  - right (CTRL-W_l)
- resize
  - vertical increase (CTRL-W\_+)
  - vertical decrease (CTRL-W\_-)
  - horizontal decrease (CTRL-W\_<)
  - horizontal increase (CTRL-W\_>)
- one window (CTRL-W_o)

---

## tab page

- open (:tabe)
- close (:tabe)
- next tab (gt), (:tabn)
- previous tab (gT), (:tabp)

---

## select all

1. keyin (gg) on normal mode
2. normal mode to select mode (v)
3. keyin (G) on select mode

---

## search and replace pattern

1. normal mode to change word on insert mode (caw)
2. keyin word then enter
3. search next pattern (n)
4. replace pattern (.)

---

## search from select mode

1. normal mode to select mode (v)
2. select word to save (y)
3. search mode (/)
4. select register (ctrl + r)
5. select the unnamed register (")
