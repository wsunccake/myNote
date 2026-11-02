# oop

## c

```c
#include <stdio.h>
#include <stdlib.h>

typedef struct Product
{
    void (*doStuff)();
} Product;

void doStuff()
{
    printf("do stuff\n");
}

Product *createProduct()
{
    Product *p = (Product *)malloc(sizeof(struct Product));
    p->doStuff = &doStuff;
    return p;
}

void deleteProduct(Product *p)
{
    free(p);
}

int main()
{
    Product *p = createProduct();
    p->doStuff();
    deleteProduct(p);

    return 0;
}
```

## java

```java
interface Product {
    void doStuff();
}

class ConcreteProduct implements Product {
    public void doStuff() {
        System.out.println("do stuff");
    }
}

class ConcreteCreator {
    public Product createProduct() {
        return new ConcreteProduct();
    }
}

class Demo {
    public static void main(String[] args){
        Product p = new ConcreteCreator().createProduct();
        p.doStuff();
  }
}
```

## python3

```python
from abc import ABC
from abc import abstractmethod

class Product(ABC):
    @abstractmethod
    def doStuff(self):
        pass

class ConcreteProduct(Product):
    def doStuff(self):
        print("do stuff")

def create_product():
    return ConcreteProduct()

if __name__ == '__main__':
    p = create_product()
    p.doStuff()
```

## go

```go
package main

import "fmt"

type Product interface {
	doStuff()
}

type ConcreteProduct struct{}

func (c *ConcreteProduct) doStuff() {
	fmt.Printf("do stuff\n")
}

type ConcreteCreatorA struct{}

func createProduct() *ConcreteProduct {
	return &ConcreteProduct{}
}

func main() {
	p := createProduct()
	p.doStuff()
}
```
