# locator / selector

---

## content

- [basic](#basic)
- [jquery](#jquery)
- [css](#css)
- [xpath](#xpath)
- [demo portal](#demo-portal)
- [ref](#ref)

---

## basic

```html
<!DOCTYPE html>
<html>
  <head>
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.7.1/jquery.min.js"></script>
    <script>
      $(document).ready(function () {
        $("#intro").css("background-color", "yellow");
      });
    </script>
  </head>
  <body>
    <h1>Welcome to My Homepage</h1>

    <p class="intro" id="name">My name is Donald.</p>
    <p>I live in Duckburg.</p>
    <a href="example.html">example</a>
  </body>
</html>
```

`tag`, `element`: <p>I live in Duckburg.</p>

`id`: <p class="intro" id="name">My name is Donald.</p>

`class`: <p class="intro" id="name">My name is Donald.</p>

`attribute`: <a href="example.html">example</a>

---

## jquery

```js
// selector                example
all document               $("*")
element / tag              $("p")
id                         $("#name")
class                      $(".intro")
attribute                  $("[href]")

// combime
$(form > div > div )
$(form, div)

$("[type=file]")
$("[href!='default.htm']")
$("[href$='.jpg']")
$("[title|='Tomorrow']")
$("[title^='Tom']")
$("[title~='hello']")
$("[title*='hello']")
```

```js
$()     document.querySelector()
$$()    document.querySelectorAll()
```

---

## css

```js
// selector                example
all document               $$("*")
element / tag              $$("p")
id                         $$("#name")
class                      $$(".intro")
attribute                  $$("[href]")

// combine
$$(".form-label.w-100")     // <x class="cls1 cls">
$$("input.form-control")    // <element class=>

$$(div, p)                  // <div>, <p>
$$(div > p)                  // <div><p>... </p></div>
$$(div + p)
$$(div ~ p)

$$([target="_blank"])
$$([title~="flower"])
$$([lang|="en"])
$$(a[href^="https"])
$$(a[href$=".pdf"])
$$(a[href*="w3schools"])
```

---

## xpath

```js
expression      example
root path       $x("/")
relative path   $x("//")
node            $x("//p")
attribute       $x("//a/@href")
current         .
parent          ..

// attribute
$x("//p/class")
$x("//p[@class]")
$x("//p[@class='title']")
$x("//p[text()='word']")

$x("./*")
$x(".//*")
```

### basic XPath Syntax

```
/ - Selects from the root node
// - Selects nodes anywhere in the document
. - Represents the current node
.. - Represents the parent of the current node
```

### selector

```
element - Selects all elements with the given name
@attribute - Selects the value of the specified attribute
* - Selects all child elements
text() - Selects the text within an element
[predicate] - Adds a condition to filter nodes
```

### predicate

```
[name='value'] - Selects nodes with the specified attribute value
[position()] - Selects nodes based on their position
[last()] - Selects the last node of a given type
[contains(@attribute, 'value')] - Selects nodes with attribute values containing 'value'
[not(predicate)] - Negates a condition
```

### axe

```
ancestor:: - Selects all ancestors
ancestor-or-self:: - Selects ancestors and the current node
child:: - Selects all children
descendant:: - Selects all descendants
descendant-or-self:: - Selects descendants and the current node
following:: - Selects all following nodes
following-sibling:: - Selects following siblings
parent:: - Selects the parent node
preceding:: - Selects all preceding nodes
preceding-sibling::- Selects preceding siblings
self:: - Selects the current node
```

### operator

```
= - Equal to
!= - Not equal to
< - Less than
<= - Less than or equal to
> - Greater than
>= - Greater than or equal to
and - Logical AND
or - Logical OR
not - Logical NOT
```

### function

```
name() - Returns the name of the current node
count(nodes) - Returns the number of nodes in the node-set
concat(string1, string2) - Concatenates two strings
substring(string, start, length) - Returns a substring
contains(string, substr) - Checks if a string contains a substring
normalize-space(string) - Removes leading/trailing whitespace and collapses spaces
```

### example

```
/bookstore/book - Selects all book elements in the root bookstore
//title[text()='XPath'] - Selects title elements with text 'XPath' anywhere in the document
//*[@id='myId'] - Selects elements with the attribute id equal to 'myId'
/bookstore/book[position()=1] - Selects the first book element
//div[@class='highlight']//p - Selects p elements within div with class 'highlight'
//a[contains(@href, 'example.com')] - Selects a elements with 'example.com' in the href attribute
```

---

## demo portal

[Web Form](https://www.selenium.dev/selenium/web/web-form.html)
[Orange HRM](https://opensource-demo.orangehrmlive.com/web/index.php/auth/login)
[Practice Test Automation WebSite](https://practice.expandtesting.com/)

---

## ref

[Category: Selectors](https://api.jquery.com/category/selectors/)
[【爬蟲必備基礎】⭐ 通宵爆肝兩萬字 xpath 教學 ⭐ 學不會找我！](https://tw511.com/a/01/39029.html)
