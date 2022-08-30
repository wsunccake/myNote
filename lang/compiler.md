# compiler


## lexical analysis / lexer

lex, flex

```
    result  =           x   +           1       ;
    ^       ^           ^   ^           ^       ^
    id      operator    id  operator    number  operator

```


---

## syntactic analysis / parser

yacc, bison, antlr

```
            =
      /         \
    result        +
                /   \
               x      1
```


### BNF / Backus–Naur Form

```
Expression ::= Term (('+' | '-') Term )*

1 + 23, 45 - 6 - 7 - 8


Term ::=  Factor (('*' | '/') Factor )*

2 * 3, 4 * 5 / 2


Factor ::= NUMBER | '(' Expression ')'

2, (3 + 4), (5 * 6)
```


---

## semantic analysis

Virtual Machine

Code Generation

Optimizer

---

## ref

[手把手教你做一个 C 语言编译器](https://wizardforcel.gitbooks.io/diy-c-compiler/content/index.html)

[自己动手写编译器](https://pandolia.net/tinyc/index.html)

[一點都不深入的了解 Compiler、 Interpreter 和 VM](https://www.spreered.com/compiler_for_dummies/)

http://ccckmit.wikidot.com/cd:c