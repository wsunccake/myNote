# gpio

## content

---

## Ohm's law

歐姆定律

```text
V = I x R

V: 電壓 / voltage,      volt
I: 電流 / current,      ampere
R: 電阻 / resistance,   ohm
```

```text
series circuit
    V_total =   V_1 +   V_2 + ...
  I R_total = I R_1 + I R_2 + ...
=>  R_total =   R_1 +   R_2 + ...

parallel circuit
        I_total =     I_1 +     I_2 + ...
    V / R_total = V / R_1 + V / R_2 + ...
=>  1 / R_total = 1 / R_1 + 1 / R_2 + ...
```

---

## mos

Metal-Oxide-Semiconductor

G-gate
S-source
D-drain

```text
pmos -> pnp (low volt to open)
   S           S
   |           |
G /  on      G | off
   |           |
   D           D

nmos -> npn (high volt to open)
   D           D
   |           |
G /  off     G | on
   |           |
   S           S
```

### pmos

### nmos

---

## gpio mode

```text
GPIO input mode  with high impedance state
GPIO input mode  with pull-up /pull-down state
GPIO output mode with open drain state
GPIO output mode with push pull state

```
