# jsonnet

## install

```bash
[ubunut:~ ] # apt update
[ubunut:~ ] # apt install golang
[ubunut:~ ] # go get github.com/google/go-jsonnet/cmd/jsonnet
[ubunut:~ ] # install -m 755 go/bin/jsonnet /usr/local/bin/.
```


---

## run

```bash
# method 1
[ubunut:~ ] # echo "{key: 1+2}" > test.jsonnet
[ubunut:~ ] # jsonnet test.jsonnet 

# method 2
[ubunut:~ ] # jsonnet -e '{key: 1+2}'
```


---

## tutorial

### syntax

```jsonnet
/* A C-style comment. */
# A Python-style comment.
{
  cocktails: {
    // Ingredient quantities are in fl oz.
    'Tom Collins': {
      ingredients: [
        { kind: "Farmer's Gin", qty: 1.5 },
        { kind: 'Lemon', qty: 1 },
        { kind: 'Simple Syrup', qty: 0.5 },
        { kind: 'Soda', qty: 2 },
        { kind: 'Angostura', qty: 'dash' },
      ],
      garnish: 'Maraschino Cherry',
      served: 'Tall',
      description: |||
        The Tom Collins is essentially gin and
        lemonade.  The bitters add complexity.
      |||,
    },
    Manhattan: {
      ingredients: [
        { kind: 'Rye', qty: 2.5 },
        { kind: 'Sweet Red Vermouth', qty: 1 },
        { kind: 'Angostura', qty: 'dash' },
      ],
      garnish: 'Maraschino Cherry',
      served: 'Straight Up',
      description: @'A clear \ red drink.',
    },
  },
}
```

->

```json
{
  "cocktails": {
    "Manhattan": {
      "description": "A clear \\ red drink.",
      "garnish": "Maraschino Cherry",
      "ingredients": [
        {
          "kind": "Rye",
          "qty": 2.5
        },
        {
          "kind": "Sweet Red Vermouth",
          "qty": 1
        },
        {
          "kind": "Angostura",
          "qty": "dash"
        }
      ],
      "served": "Straight Up"
    },
    "Tom Collins": {
      "description": "The Tom Collins is essentially gin and\nlemonade.  The bitters add complexity.\n",
      "garnish": "Maraschino Cherry",
      "ingredients": [
        {
          "kind": "Farmer's Gin",
          "qty": 1.5
        },
        {
          "kind": "Lemon",
          "qty": 1
        },
        {
          "kind": "Simple Syrup",
          "qty": 0.5
        },
        {
          "kind": "Soda",
          "qty": 2
        },
        {
          "kind": "Angostura",
          "qty": "dash"
        }
      ],
      "served": "Tall"
    }
  }
}
```


### variable

```jsonnet
// A regular definition.
local house_rum = 'Banks Rum';

{
  // A definition next to fields.
  local pour = 1.5,

  Daiquiri: {
    ingredients: [
      { kind: house_rum, qty: pour },
      { kind: 'Lime', qty: 1 },
      { kind: 'Simple Syrup', qty: 0.5 },
    ],
    served: 'Straight Up',
  },
  Mojito: {
    ingredients: [
      {
        kind: 'Mint',
        action: 'muddle',
        qty: 6,
        unit: 'leaves',
      },
      { kind: house_rum, qty: pour },
      { kind: 'Lime', qty: 0.5 },
      { kind: 'Simple Syrup', qty: 0.5 },
      { kind: 'Soda', qty: 3 },
    ],
    garnish: 'Lime wedge',
    served: 'Over crushed ice',
  },
}
```

->

```json
{
  "Daiquiri": {
    "ingredients": [
      {
        "kind": "Banks Rum",
        "qty": 1.5
      },
      {
        "kind": "Lime",
        "qty": 1
      },
      {
        "kind": "Simple Syrup",
        "qty": 0.5
      }
    ],
    "served": "Straight Up"
  },
  "Mojito": {
    "garnish": "Lime wedge",
    "ingredients": [
      {
        "action": "muddle",
        "kind": "Mint",
        "qty": 6,
        "unit": "leaves"
      },
      {
        "kind": "Banks Rum",
        "qty": 1.5
      },
      {
        "kind": "Lime",
        "qty": 0.5
      },
      {
        "kind": "Simple Syrup",
        "qty": 0.5
      },
      {
        "kind": "Soda",
        "qty": 3
      }
    ],
    "served": "Over crushed ice"
  }
}
```


### reference

```jsonnet
{
  'Tom Collins': {
    ingredients: [
      { kind: "Farmer's Gin", qty: 1.5 },
      { kind: 'Lemon', qty: 1 },
      { kind: 'Simple Syrup', qty: 0.5 },
      { kind: 'Soda', qty: 2 },
      { kind: 'Angostura', qty: 'dash' },
    ],
    garnish: 'Maraschino Cherry',
    served: 'Tall',
  },
  Martini: {
    ingredients: [
      {
        // Use the same gin as the Tom Collins.
        kind:
          $['Tom Collins'].ingredients[0].kind,
        qty: 2,
      },
      { kind: 'Dry White Vermouth', qty: 1 },
    ],
    garnish: 'Olive',
    served: 'Straight Up',
  },
  // Create an alias.
  'Gin Martini': self.Martini,
}
```

->

```json
{
  "Gin Martini": {
    "garnish": "Olive",
    "ingredients": [
      {
        "kind": "Farmer's Gin",
        "qty": 2
      },
      {
        "kind": "Dry White Vermouth",
        "qty": 1
      }
    ],
    "served": "Straight Up"
  },
  "Martini": {
    "garnish": "Olive",
    "ingredients": [
      {
        "kind": "Farmer's Gin",
        "qty": 2
      },
      {
        "kind": "Dry White Vermouth",
        "qty": 1
      }
    ],
    "served": "Straight Up"
  },
  "Tom Collins": {
    "garnish": "Maraschino Cherry",
    "ingredients": [
      {
        "kind": "Farmer's Gin",
        "qty": 1.5
      },
      {
        "kind": "Lemon",
        "qty": 1
      },
      {
        "kind": "Simple Syrup",
        "qty": 0.5
      },
      {
        "kind": "Soda",
        "qty": 2
      },
      {
        "kind": "Angostura",
        "qty": "dash"
      }
    ],
    "served": "Tall"
  }
}
```


### inner-reference

```jsonnet
{
  Martini: {
    local drink = self,
    ingredients: [
      { kind: "Farmer's Gin", qty: 1 },
      {
        kind: 'Dry White Vermouth',
        qty: drink.ingredients[0].qty,
      },
    ],
    garnish: 'Olive',
    served: 'Straight Up',
  },
}
```

->

```json
{
  "Martini": {
    "garnish": "Olive",
    "ingredients": [
      {
        "kind": "Farmer's Gin",
        "qty": 1
      },
      {
        "kind": "Dry White Vermouth",
        "qty": 1
      }
    ],
    "served": "Straight Up"
  }
}
```


### arithmetic

```jsonnet
{
  concat_array: [1, 2, 3] + [4],
  concat_string: '123' + 4,
  equality1: 1 == '1',
  equality2: [{}, { x: 3 - 1 }]
             == [{}, { x: 2 }],
  ex1: 1 + 2 * 3 / (4 + 5),
  // Bitwise operations first cast to int.
  ex2: self.ex1 | 3,
  // Modulo operator.
  ex3: self.ex1 % 2,
  // Boolean logic
  ex4: (4 > 3) && (1 <= 3) || false,
  // Mixing objects together
  obj: { a: 1, b: 2 } + { b: 3, c: 4 },
  // Test if a field is in an object
  obj_member: 'foo' in { foo: 1 },
  // String formatting
  str1: 'The value of self.ex2 is '
        + self.ex2 + '.',
  str2: 'The value of self.ex2 is %g.'
        % self.ex2,
  str3: 'ex1=%0.2f, ex2=%0.2f'
        % [self.ex1, self.ex2],
  // By passing self, we allow ex1 and ex2 to
  // be extracted internally.
  str4: 'ex1=%(ex1)0.2f, ex2=%(ex2)0.2f'
        % self,
  // Do textual templating of entire files:
  str5: |||
    ex1=%(ex1)0.2f
    ex2=%(ex2)0.2f
  ||| % self,
}
```

->

```json
{
  "concat_array": [
    1,
    2,
    3,
    4
  ],
  "concat_string": "1234",
  "equality1": false,
  "equality2": true,
  "ex1": 1.6666666666666665,
  "ex2": 3,
  "ex3": 1.6666666666666665,
  "ex4": true,
  "obj": {
    "a": 1,
    "b": 3,
    "c": 4
  },
  "obj_member": true,
  "str1": "The value of self.ex2 is 3.",
  "str2": "The value of self.ex2 is 3.",
  "str3": "ex1=1.67, ex2=3.00",
  "str4": "ex1=1.67, ex2=3.00",
  "str5": "ex1=1.67\nex2=3.00\n"
}
```


### function

```jsonnet
// Define a local function.
// Default arguments are like Python:
local my_function(x, y=10) = x + y;

// Define a local multiline function.
local multiline_function(x) =
  // One can nest locals.
  local temp = x * 2;
  // Every local ends with a semi-colon.
  [temp, temp + 1];

local object = {
  // A method
  my_method(x): x * x,
};

{
  // Functions are first class citizens.
  call_inline_function:
    (function(x) x * x)(5),

  call_multiline_function: multiline_function(4),

  // Using the variable fetches the function,
  // the parens call the function.
  call: my_function(2),

  // Like python, parameters can be named at
  // call time.
  named_params: my_function(x=2),
  // This allows changing their order
  named_params2: my_function(y=3, x=2),

  // object.my_method returns the function,
  // which is then called like any other.
  call_method1: object.my_method(3),

  standard_lib:
    std.join(' ', std.split('foo/bar', '/')),
  len: [
    std.length('hello'),
    std.length([1, 2, 3]),
  ],
}
```

->

```json
{
  "call": 12,
  "call_inline_function": 25,
  "call_method1": 9,
  "call_multiline_function": [8, 9],
  "len": [
    5,
    3
  ],
  "named_params": 12,
  "named_params2": 5,
  "standard_lib": "foo bar"
}
```


```jsonnet
// This function returns an object. Although
// the braces look like Java or C++ they do
// not mean a statement block, they are instead
// the value being returned.
local Sour(spirit, garnish='Lemon twist') = {
  ingredients: [
    { kind: spirit, qty: 2 },
    { kind: 'Egg white', qty: 1 },
    { kind: 'Lemon Juice', qty: 1 },
    { kind: 'Simple Syrup', qty: 1 },
  ],
  garnish: garnish,
  served: 'Straight Up',
};

{
  'Whiskey Sour': Sour('Bulleit Bourbon',
                       'Orange bitters'),
  'Pisco Sour': Sour('Machu Pisco',
                     'Angostura bitters'),
}
```

->

```json
{
  "Pisco Sour": {
    "garnish": "Angostura bitters",
    "ingredients": [
      {
        "kind": "Machu Pisco",
        "qty": 2
      },
      {
        "kind": "Egg white",
        "qty": 1
      },
      {
        "kind": "Lemon Juice",
        "qty": 1
      },
      {
        "kind": "Simple Syrup",
        "qty": 1
      }
    ],
    "served": "Straight Up"
  },
  "Whiskey Sour": {
    "garnish": "Orange bitters",
    "ingredients": [
      {
        "kind": "Bulleit Bourbon",
        "qty": 2
      },
      {
        "kind": "Egg white",
        "qty": 1
      },
      {
        "kind": "Lemon Juice",
        "qty": 1
      },
      {
        "kind": "Simple Syrup",
        "qty": 1
      }
    ],
    "served": "Straight Up"
  }
}
```


---

## ref

[jsonnet](https://jsonnet.org/)

[jsonnet](https://knowledge.zhaoweiguo.com/build/html/protocol/others/jsonnet.html)
