# OOP

同一件事的五種寫法：呼叫端只靠抽象（函式指標、interface、ABC、trait）呼叫 `doStuff`，具體型別由建立函式決定。

C 沒有類別，要自己把「資料 + 函式指標」放進 struct，呼叫時手動傳入物件。Java、Python、Go、Rust 由語言做派送；差別在實作是明示（`implements` / 繼承 / `impl Trait`）還是隱式（Go）。

---

## C

```c
#include <stdio.h>
#include <stdlib.h>

typedef struct Product {
    void (*doStuff)(struct Product *self);
    const char *name;
} Product;

static void productDoStuff(Product *self)
{
    printf("do stuff: %s\n", self->name);
}

Product *createProduct(void)
{
    Product *p = malloc(sizeof(*p));
    if (!p)
        return NULL;
    p->name = "product";
    p->doStuff = productDoStuff;
    return p;
}

void deleteProduct(Product *p)
{
    free(p);
}

int main(void)
{
    Product *p = createProduct();
    if (!p)
        return 1;
    p->doStuff(p);
    deleteProduct(p);
    return 0;
}
```

1. `doStuff` 是函式指標欄位，不是方法。編譯器不會自動加上 `this`，所以簽名要自己寫 `Product *self`，呼叫寫成 `p->doStuff(p)`。
2. `createProduct` 負責配置與填指標，相當於建構式。`deleteProduct` 只 `free` 這塊記憶體；欄位若再擁有別的資源，要在 `free` 之前自己釋放。
3. `malloc` 失敗會回傳 `NULL`。不檢查就對 `p->doStuff` 呼叫是未定義行為。
4. 函式指標的空括號 `void (*f)()` 在 C 裡是「參數個數不明」，不是「沒有參數」。沒有參數要寫 `void`。
5. 換另一種產品時，通常再準備一組函式，並在另一個 create 裡把指標指過去。這就是手動虛表；沒有繼承語法。

---

## Java

```java
interface Product {
    void doStuff();
}

class ConcreteProduct implements Product {
    @Override
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
    public static void main(String[] args) {
        Product p = new ConcreteCreator().createProduct();
        p.doStuff();
    }
}
```

1. `Product` 只規定能呼叫什麼。`ConcreteProduct` 用 `implements` 交出實作；`@Override` 讓簽章寫錯時編譯失敗。
2. `main` 的變數型別是 `Product`，不是 `ConcreteProduct`。後面換實作，只要 `createProduct` 仍回傳 `Product`，這行不用改。
3. `p.doStuff()` 依執行期的實際物件派送。介面方法預設就是 `public`，實作方法也必須是 `public`。
4. `ConcreteCreator` 把 `new ConcreteProduct()` 收在一處。這是簡單工廠，不是還要再繼承 Creator 的 Factory Method。
5. 物件由垃圾回收釋放，沒有對應 C 的 `deleteProduct`。

---

## Python

```python
from abc import ABC, abstractmethod

class Product(ABC):
    @abstractmethod
    def doStuff(self):
        pass

class ConcreteProduct(Product):
    def doStuff(self):
        print("do stuff")

def create_product() -> Product:
    return ConcreteProduct()

if __name__ == "__main__":
    p = create_product()
    p.doStuff()
```

1. `self` 就是 C 那個要手傳的物件，呼叫 `p.doStuff()` 時語言會把它補上。
2. `ABC` 加上 `@abstractmethod` 之後，`Product()` 會在執行期丟出 `TypeError`。子類別沒實作 `doStuff` 也不能被建立。
3. `-> Product` 只給型別檢查看。執行期 `create_product()` 回傳的仍是 `ConcreteProduct` 實例。
4. 沒有這層 ABC 時，只要物件有 `doStuff` 就能呼叫，不一定要繼承 `Product`。ABC 是刻意把這件事收緊。
5. 沒有介面關鍵字。抽象靠繼承；解構靠參考計數，一般情況不用手動 `free`。

---

## Go

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

func createProduct() Product {
	return &ConcreteProduct{}
}

func main() {
	p := createProduct()
	p.doStuff()
}
```

1. 沒有 `implements`。`*ConcreteProduct` 有 `doStuff` 方法，就滿足 `Product`。少一個方法、或接收者種類不對，指定給 `Product` 時編譯失敗。
2. 方法寫在指標接收者上時，實作介面的是 `*ConcreteProduct`，不是 `ConcreteProduct` 這個值。所以工廠回傳 `&ConcreteProduct{}`。
3. `createProduct` 的回傳型別是介面 `Product`。若寫成 `*ConcreteProduct`，呼叫端就重新依賴具體型別，介面等於沒用到。
4. `doStuff` 首字小寫，只在這個 package 內可見。要給別的 package 實作或呼叫，方法名必須大寫。
5. 介面值裡若放進 nil 指標，介面本身並不是 nil，呼叫仍會進來方法。這個例子的工廠不回傳 nil。

---

## Rust

```rust
trait Product {
    fn do_stuff(&self);
}

struct ConcreteProduct;

impl Product for ConcreteProduct {
    fn do_stuff(&self) {
        println!("do stuff");
    }
}

fn create_product() -> Box<dyn Product> {
    Box::new(ConcreteProduct)
}

fn main() {
    let p = create_product();
    p.do_stuff();
}
```

1. `trait` 是規格。`impl Product for ConcreteProduct` 是明示實作，接近 Java 的 `implements`。一個型別可以實作多個 trait。
2. `&self` 就是 C 要手傳的物件。呼叫 `p.do_stuff()` 時語言會補上。方法名用蛇形命名，對應其他語言的 `doStuff`。
3. `Box<dyn Product>` 把具體型別擦掉，經由虛表動態派送，和 C 的函式指標、Java 的介面變數同一類。`dyn Product` 大小不固定，不能直接當回傳值放在堆疊上，所以要放進 `Box`。
4. 若回傳寫成 `impl Product`，簽名一樣看不到 `ConcreteProduct`，但是靜態派送：編譯器知道實際型別並複製一份專用程式碼。一個函式用 `impl Trait` 回傳時，所有路徑必須是同一種具體型別。
5. `Box` 離開 scope 會 `drop`，沒有對應的 `deleteProduct`。這個 `ConcreteProduct` 沒有欄位，不需要自己寫 `Drop`。
