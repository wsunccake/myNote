# stack

```
            A + (B * C)
infix:      A+(B*C)
postfix:    ABC*+
prefix:     +A*BC
```


---

## tree traversal

inorder:    left -> root -> right

postorder:  left -> right -> root

preorder:   root -> left -> right


```
    A + (B * C)

    ->

     +
   /   \
  A     *
       / \
      B   C

inorder:    A + B * C

postorder:  A B C * +

preorder:   + A * B C
```
